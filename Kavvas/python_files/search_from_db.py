import mysql.connector as mariadb
from configparser import ConfigParser


def get_output(manufactor=None, Product=None, Revision=None, Protocol=None, Username=None, Password=None, Access=None, Validated=None):

    input_forms = {"manufactor": manufactor,
                   "Product": Product,
                   "Revision": Revision,
                   "Protocol": Protocol,
                   "Username": Username,
                   "Password": Password,
                   "Access": Access,
                   "Validated": Validated}

    sql_command = "select * from panel_credentials"
    counter = 0
    for i in input_forms.keys():

        if input_forms[i] != '':
            counter += 1
            if counter <= 1:
                sql_command = sql_command + " WHERE " + \
                    str(i) + "='" + str(input_forms[i]) + "'"
            else:
                sql_command = sql_command + " and " + \
                    str(i) + "='" + str(input_forms[i]) + "'"

    config = ConfigParser()
    config.read('config.ini')

    db_host = config['database']['host']
    db_port = config['database']['port']
    db_name = config['database']['db_name']
    db_username = config['database']['user']
    db_password = config['database']['password']

    mariadb_connection = mariadb.connect(
        host=db_host, port=db_port, user=db_username, password=db_password, database=db_name)
    cursor = mariadb_connection.cursor()

    cursor.execute(sql_command)

    results = cursor.fetchall()

    results.insert(0, ["id", "Manufactor", "Product", "Revision",
                       "Protocol", "Username", "Password", "Access", "Validated"])

    cursor.close()
    mariadb_connection.close()
    return results


def insert_data(manufactor=None, Product=None, Revision=None, Protocol=None, Username=None, Password=None, Access=None, Validated=None):

    config = ConfigParser()
    config.read('config.ini')

    db_host = config['database']['host']
    db_port = config['database']['port']
    db_name = config['database']['db_name']
    db_username = config['database']['user']
    db_password = config['database']['password']

    mariadb_connection = mariadb.connect(
        host=db_host, port=db_port, user=db_username, password=db_password, database=db_name)
    cursor = mariadb_connection.cursor()

    cursor.execute("INSERT INTO panel_credentials (Manufactor, Product, Revision , Protocol , Username , Password , Access , Validated) VALUES ( %s , %s , %s , %s , %s , %s , %s , %s)",
                   (manufactor, Product, Revision, Protocol, Username, Password, Access, Validated))

    mariadb_connection.commit()
    mariadb_connection.close()

    add_result = "Value Added"

    return add_result


def get_founded_sites(host=None, port=None, source_scan=None, web_page_title=None):

    input_forms = {"host": host,
                   "port": port,
                   "login_page_result": source_scan,
                   "login_result": web_page_title
                   }

    sql_command = "select * from founded_sites"
    counter = 0
    for i in input_forms.keys():
        if input_forms.values() == ['', '', '', '']:
            pass
        else:
            if input_forms[i] != '':
                counter += 1
                if counter <= 1:
                    sql_command = sql_command + " WHERE " + \
                        str(i) + "='" + str(input_forms[i]) + "'"
                else:
                    sql_command = sql_command + " and " + \
                        str(i) + "='" + str(input_forms[i]) + "'"

    config = ConfigParser()
    config.read('config.ini')

    db_host = config['database']['host']
    db_port = config['database']['port']
    db_name = config['database']['db_name']
    db_username = config['database']['user']
    db_password = config['database']['password']

    mariadb_connection = mariadb.connect(
        host=db_host, port=db_port, user=db_username, password=db_password, database=db_name)
    cursor = mariadb_connection.cursor()

    cursor.execute(sql_command)

    results = cursor.fetchall()

    results.insert(0, ["id", "Host", "Target Url", "Port",
                       "Source Code Result", "Login Page Result"])

    cursor.close()
    mariadb_connection.close()
    return results
