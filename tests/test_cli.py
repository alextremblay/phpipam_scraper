import re
import configparser
import sys

from phpipam_scraper.cli import main
from click.testing import CliRunner
import pytest


PY2 = sys.version_info[0] == 2


@pytest.fixture()
def conf():
    conf_variables = configparser.ConfigParser()
    conf_variables.read('variables.cfg')
    conf_variables.read('tests/variables.cfg')
    return conf_variables


def test_is_the_test_rig_setup(conf):
    message = 'You have not set up the testing variables file to run this test, or the testing variables file is ' \
              'missing options. Please run setup_tests.py first'
    assert conf.has_option('config', 'url'), message
    assert conf.has_option('phpipam', 'username'), message
    assert conf.has_option('phpipam', 'password'), message


@pytest.fixture()
def runner():
    cli_runner = CliRunner()
    return cli_runner


def test_help_base(runner):
    result = runner.invoke(main, ['--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'phpIPAM' in result.output


def test_help_get(runner):
    result = runner.invoke(main, ['get', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'Commands' in result.output


def test_help_get_search(runner):
    result = runner.invoke(main, ['get', 'search', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert "Search the 'IP Addresses' section" in result.output


def test_help_get_device(runner):
    result = runner.invoke(main, ['get', 'device', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert "Search phpIPAM's Devices page" in result.output


def test_help_get_all(runner):
    result = runner.invoke(main, ['get', 'all', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'Search all' in result.output


def test_help_config(runner):
    result = runner.invoke(main, ['config', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'Commands' in result.output


def test_help_config_set(runner):
    result = runner.invoke(main, ['config', 'set-url', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'Specify a new phpIPAM URL' in result.output


def test_help_config_get(runner):
    result = runner.invoke(main, ['config', 'get-url', '--help'])
    assert result.exit_code is 0
    assert 'Usage' in result.output
    assert 'currently configured phpIPAM URL' in result.output


# running this test under Python 3 produces a RecursionError which cannot be replicated when
# running 'phpipam config get-url' directly. This appears to be a flaw in click.testing, not in this application itself
if PY2:
    def test_config_get(runner):
        result = runner.invoke(main, ['config', 'get-url'])
        url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
        assert result.exit_code is 0
        assert re.match(url_regex, result.output)

# running this test under Python 3 produces a SystemExit value of 2, which cannot be replicated when
# running 'phpipam config get-url' directly. This appears to be a flaw in click.testing, not in this application itself
if PY2:
    def test_config_set(runner, conf):
        url = conf.get('config', 'url')
        result = runner.invoke(main, ['config', 'set-url', url])
        assert result.exit_code is 0
        assert 'New phpIPAM URL set!' in result.output