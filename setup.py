from setuptools import setup

setup(
    name = 'phpipam_scraper',
    version = '0.4',
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
    packages = ['phpipam_scraper'],
    install_requires=['requests', 'beautifulsoup4', 'tabulate'],
    entry_points = {
        'console_scripts': [
            'phpipam = phpipam_scraper.__main__:main'
        ]
})