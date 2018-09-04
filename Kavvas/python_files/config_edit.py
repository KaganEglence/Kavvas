import configparser
import os


def edit_config(db_host, db_port, db_name, db_username, db_password):
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        config['database'] = {'host': '', 'port': '',
                              'db_name': '', 'user': '', 'password': ''}

        config.write(open('config.ini', 'w'))

    config = configparser.ConfigParser()
    config.read('config.ini')
    config['database']['host'] = str(db_host)
    config['database']['port'] = db_port
    config['database']['db_name'] = db_name
    config['database']['user'] = db_username
    config['database']['password'] = db_password

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
