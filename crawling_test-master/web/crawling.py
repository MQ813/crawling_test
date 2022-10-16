from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests, time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from common.job import meas_run_time

# @meas_run_time
# def get_soup(url):
def get_source(url, selenium=True):
    if selenium:
        options = Options()
        options.headless = True
        options.add_argument('headless')
        options.add_argument("disable-gpu")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
                                                            'geolocation': 2, 'notifications': 2,
                                                            'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2,
                                                            'mixed_script': 2, 'media_stream': 2, 'media_stream_mic': 2,
                                                            'media_stream_camera': 2, 'protocol_handlers': 2,
                                                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                            'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                            'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                                            'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
        options.add_experimental_option('prefs', prefs)
        caps = DesiredCapabilities().CHROME
        caps['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
        caps["pageLoadStrategy"] = "eager"
        # caps["pageLoadStrategy"] = "none"

        driver = webdriver.Chrome('./web/chromedriver.exe', chrome_options=options, desired_capabilities=caps)
        driver.get(url)
        page_source = driver.page_source
        driver.close()
    else:
        page_source = requests.get(url).text
    return page_source
    # return BeautifulSoup(str(page_source), "html.parser")

def get_soup(page_source):
    return BeautifulSoup(str(page_source), "html.parser")


