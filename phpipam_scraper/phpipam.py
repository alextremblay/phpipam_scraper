from time import time
import cookielib
import os
import getpass

import requests  # External module requests
from bs4 import BeautifulSoup  # External module BeautifulSoup4


cookie_file = os.path.expanduser('~/.local/phpipam_auth_cookie')
device_url_partial = '/app/tools/devices/devices-print.php'
auth_url_partial = '/app/login/login_check.php'


class IPAM(object):

    def __init__(self, hostname='default'):
        if hostname is 'default':
            if not os.path.exists('phpipam.cfg'):
                self.setup_config()  # Sets and saves the base url string
            else:
                with open('phpipam.cfg') as config:
                    self.base_url = config.read()
        else:
            self.base_url = hostname
        self.device_url = self.base_url + device_url_partial
        self.auth_url = self.base_url + auth_url_partial
        self.session = requests.Session()

    def setup_config(self):
        print('PHPIPAM configuration not found! Please enter the URL for your PHPIPAM installation')
        print('Example: http://ipam.yourcompanyaddress.com or http://yourwebsite.com/phpipam')
        self.base_url = raw_input('PHPIPAM URL:').rstrip('/')
        with open('phpipam.cfg', 'w') as config:
            config.write(self.base_url)
        print('Configuration saved successfully!')

    def get_device_list(self, keyword):
        self.session.cookies = cookielib.LWPCookieJar()
        self._get_auth_cookie()
        search = {'ffield': 'hostname', 'fval': keyword, 'direction': 'hostname|asc'}
        resp = self.session.post(self.device_url, search)
        soup = BeautifulSoup(resp.content, 'html.parser')
        device_table = soup.find('table', id='switchManagement')
        result = []
        for row in device_table.find_all('tr'):  # Get all table rows
            columns = row.find_all('td')  # Get all cells in each table row
            if len(columns) > 0:  # Ignore empty rows at start or end of range
                hostname = columns[0].a
                ip_address = columns[1]
                # Only rows that have an <a> tag in the first column are devices. Rows that have a blank field
                # instead of an ip address in column[1] are of no interest to us.
                if len(ip_address) > 0 and hostname:
                    result.append((hostname.text, ip_address.text))
        return result

    def _get_auth_cookie(self):
        if os.path.isfile(cookie_file):
            return self._get_auth_cookie_from_file()
        else:
            return self._get_new_cookie()

    def _get_auth_cookie_from_file(self):
        cj = self.session.cookies
        # Read the contents of the cookie file into the cookie jar
        cj.load(cookie_file)

        # if the file had no cookies in it, then the cookie jar will have 0 length
        if len(cj) > 0:  # Cookie jar has cookies in it

            # Cookie jars are wierd. you can't look up a specific cookie by name, so you have to iterate over the whole
            # jar and manually search for the cookie you're looking for. This will pull the cookie out of the jar into
            # a list
            auth_cookie = [c for c in cj if c.name == 'phpipam']

            # Pull the auth cookie out of the list
            auth_cookie = auth_cookie[0]

            if auth_cookie.is_expired():

                self._get_new_cookie()

            else:

                # Update the expiry time on the cookie
                auth_cookie.expires += 1800

                # Put the updated auth cookie back into the cookie jar
                cj.set_cookie(auth_cookie)

        else:  # Cookie jar has no cookies in it

            self._get_new_cookie()

    def _get_new_cookie(self):
        cj = self.session.cookies
        auth = dict()
        auth['ipamusername'] = raw_input('PHPIPAM Username:')
        auth['ipampassword'] = getpass.getpass('PHPIPAM Password:')
        response = requests.post(self.auth_url, data=auth)
        if 'Invalid username' in response.content:
            raise Exception('PHPIPAM error: Invalid username or password')
        token = response.cookies['phpipam']
        expires = time() + 1800
        attr = {'version': 0, 'port': None, 'port_specified': None, 'domain': '', 'domain_specified': False,
                'domain_initial_dot': None, 'path': '/', 'path_specified': False, 'secure': None, 'discard': None,
                'comment': '', 'comment_url': '', 'rest': {}}
        auth_cookie = cookielib.Cookie(name='phpipam', value=token, expires=expires, **attr)
        cj.set_cookie(auth_cookie)
        if not os.path.exists(os.path.expanduser('~/.local')):
            os.mkdir(os.path.expanduser('~/.local'), 0755)
        cj.save(cookie_file)