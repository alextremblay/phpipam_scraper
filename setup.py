from setuptools import setup
from setuptools.command.install import install
import os
import sys
import ConfigParser


class ExtendedInstall(install):
    def run(self):
        install.run(self)
        print('phpIPAM Scraper setup: Please enter the URL for your phpIPAM installation')
        print('Example: http://ipam.yourcompanyaddress.com or http://yourwebsite.com/phpipam')
        url = raw_input('phpIPAM URL:').rstrip('/')
        if sys.platform == 'win32':
            paths = [
                os.path.join(os.getenv('LOCALAPPDATA'), 'phpipam', 'phpipam.cfg')
                ]
        else:
            paths = [
                os.path.join('/', 'usr', 'local', 'phpipam.cfg'),
                os.path.expanduser('~/.local/phpipam.cfg')
                ]
        config = ConfigParser.ConfigParser()
        config.add_section('phpipam')
        config.set('phpipam', 'url', url)
        for path in paths:
            try:
                with open(path, 'w') as f:
                    config.write(f)
            except IOError:
                pass


setup(
    name='phpipam_scraper',
    version='0.5',
    cmdclass={'install': ExtendedInstall},
    description='A python library to retrieve device IPs from a PHPipam installation',
    long_description='''This package contains a python module for use by other scripts, and a commandline tool to
    quickly retrieve the names and IP addresses of devices which match a keyword argument''',
    url='https://github.com/alextremblay/phpipam_scraper',
    author='Alex Tremblay',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',

        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['phpipam_scraper'],
    install_requires=['requests', 'beautifulsoup4', 'tabulate'],
    entry_points={
        'console_scripts': [
            'phpipam = phpipam_scraper.__main__:main'
        ]
    }
)
