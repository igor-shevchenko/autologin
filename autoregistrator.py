from ConfigParser import SafeConfigParser
from time import sleep
import requests

CONFIG_FILENAME = 'settings.ini'
SECTION_NAME = 'auth'
DELAY_SECONDS = 5


class LoginStatus:
    SUCCESS, LOGGED, WRONGPASS, CONNECTION_ERROR, UNKNOWN = range(5) # enum imitation


class Authorizer:
    def login(self, username, password):
        try:
            r = requests.post('https://webauth.susu.ac.ru/login.html', data={
                'buttonClicked': '4',
                'err_flag': '0',
                'err_msg': '',
                'info_flag': '0',
                'info_msg': '',
                'redirect_url': '',

                'username': username,
                'password': password
            })
        except requests.ConnectionError:
            return LoginStatus.CONNECTION_ERROR
        return self._get_state(r)

    def _get_state(self, response):
        text = response.text
        if 'You can now use all our regular network services over the wireless network.' in text:
            return LoginStatus.SUCCESS
        if 'Web Authentication Failure' in text:
            return LoginStatus.LOGGED
        if 'You are connected to wireless network':
            return LoginStatus.WRONGPASS
        return LoginStatus.UNKNOWN


class SettingsProvider:
    def __init__(self):
        self.config = SafeConfigParser()
        self.config.read(CONFIG_FILENAME)

        if not self.config.has_section(SECTION_NAME):
            self.config.add_section(SECTION_NAME)

    def get_option(self, name):
        if self.config.has_option(SECTION_NAME, name):
            return self.config.get(SECTION_NAME, name)
        return self.prompt_and_save(name)

    def prompt_and_save(self, name, default=None):
        if default:
            input_value = raw_input('%s (leave empty for "%s"): ' % (name, default)).strip() or default
        else:
            input_value = raw_input('%s: ' % name).strip()
        self.config.set(SECTION_NAME, name, input_value)
        with open(CONFIG_FILENAME, 'wb') as configfile:
            self.config.write(configfile)
        return input_value


class Application:
    def start(self):
        authorizer = Authorizer()
        settings = SettingsProvider()
        username = settings.get_option('username')
        password = settings.get_option('password')

        prev_login_result = None
        while True:
            login_result = authorizer.login(username, password)
            if login_result == LoginStatus.SUCCESS:
                print 'Logged in'
            elif login_result == LoginStatus.WRONGPASS:
                print 'Wrong username or password'
                username = settings.prompt_and_save('username', username)
                password = settings.prompt_and_save('password', password)
                continue  # don't wait before next request
            # compare to previous result to avoid flooding console with error messages
            elif login_result == LoginStatus.CONNECTION_ERROR != prev_login_result:
                print 'Connection error'
            elif login_result == LoginStatus.UNKNOWN != prev_login_result:
                print 'Unknown login result'
            prev_login_result = login_result
            sleep(DELAY_SECONDS)

if __name__ == '__main__':
    Application().start()