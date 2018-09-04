from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import string
import itertools


def correct_filename(filename):
    corrected_filename = ""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    for c in filename:
        if c in valid_chars:
            corrected_filename += c
        else:
            corrected_filename += "_"
    corrected_filename = corrected_filename.replace("___", "_")
    return corrected_filename


def get_screenshot(target_url):

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36")

    driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=[
                                 '--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false'], service_log_path=os.path.devnull)
    driver.set_window_size(1024, 768)
    driver.get(target_url)
    time.sleep(5)
    file_name = str("./Kavvas/static/img/screenshots/") + \
        str(correct_filename(target_url)) + ".png"
    driver.save_screenshot(file_name)
    driver.quit


def get_filenames_of_screenshots():
    dir_listing = os.listdir('./Kavvas/static/img/screenshots/')
    files = [file.replace("_.png", "") for file in dir_listing]
    return files
