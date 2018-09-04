from . import scan_target_ip
from . import login_form_with_url
from . import search_from_db
from . import config_edit
from . import take_screenshot
import threading


def login_page(target_ip):
    return login_form_with_url.checkCreds(target_ip)


def search_db(manufactor, Product, Revision, Protocol, Username, Password, Access, Validated):
    return search_from_db.get_output(manufactor, Product, Revision, Protocol, Username, Password, Access, Validated)


def add_value(manufactor, Product, Revision, Protocol, Username, Password, Access, Validated):
    return search_from_db.insert_data(manufactor, Product, Revision, Protocol, Username, Password, Access, Validated)


def founded_sites_output(host, port, source_type, get_result_of_login_scan):
    return search_from_db.get_founded_sites(host, port, source_type, get_result_of_login_scan)


def scan_target(target):
    scan = threading.Thread(
        target=scan_target_ip.scan_with_ip(target), args=target)
    scan.start()


def scan_login_forms(target):
    scan = threading.Thread(
        target=login_form_with_url.checkCreds(target), args=target)
    scan.start()


def edit_settings(db_host, db_port, db_name, db_username, db_password):
    return(config_edit.edit_config(db_host, db_port, db_name, db_username, db_password))


def gather_screenshot(target_url):
    take_screenshot_start = threading.Thread(
        target=take_screenshot.get_screenshot(target_url),  args=target_url)
    take_screenshot_start.start()


def founded_screenshots():
    return take_screenshot.get_filenames_of_screenshots()
