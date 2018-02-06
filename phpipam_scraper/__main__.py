"""

"""

__version__ = '1.1.2'

import os
import click
from click_shell import shell
from tabulate import tabulate
from .phpipam import IPAM, get_config, delete_config

ipam = None

@shell(prompt='phpipam>',
       intro="Welcome to the phpIPAM Scraper shell utility version " + __version__ + ". type a command to begin, type "
             "'?' or 'help' for a list of supported commands, or type 'quit' or 'exit' to quit",
       help="A command-line tool for retrieving device information (Description, Hostname, IP Address) from a "
            "phpIPAM installation")
@click.pass_context
@click.option('-u', '--username')
@click.option('-p', '--password')
def cli(ctx, username, password):
    global ipam
    if username or password:
        ipam = IPAM(username, password)


@cli.group(help='Commands to retrieve info from phpIPAM. Must be called with a subcommand.')
def get():
    pass


@get.command(help="Search the 'IP Addresses' section of phpIPAM's search page for a given keyword")
@click.argument('keyword')
def search(keyword):
    global ipam
    if ipam is None:
        ipam = IPAM()
    results = ipam.get_from_search(keyword)
    click.echo(tabulate(results, headers='keys'))


@get.command(help="Search phpIPAM's Devices page for a given keyword")
@click.argument('keyword')
def device(keyword):
    global ipam
    if ipam is None:
        ipam = IPAM()
    results = ipam.get_from_devices(keyword)
    click.echo(tabulate(results, headers='keys'))


@get.command(help="Search all available sources in phpIPAM for a given keyword")
@click.argument('keyword')
def combined(keyword):
    global ipam
    if ipam is None:
        ipam = IPAM()
    results = ipam.get_all(keyword)
    click.echo(tabulate(results, headers='keys'))


@cli.group(name='config', help="Commands for working with this tool's stored configuration. Must be called "
                               "with a subcommand.")
def conf():
    pass


@conf.command(name='run-setup', help="Re-runs the configuration setup script "
                                     "to generate a new config file")
def run_setup():
    delete_config()
    get_config()


@conf.command(name='get-url', help="Show the currently configured phpIPAM URL "
                                   "to connect to.")
def get_url():
    config = get_config()
    click.echo(config.url)
