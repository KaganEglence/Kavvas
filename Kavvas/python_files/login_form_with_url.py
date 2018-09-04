import base64
import urllib3
import mysql.connector as mariadb
import re
from bs4 import BeautifulSoup as beatsop
import socket
import OpenSSL
import ssl
import requests
from Wappalyzer import Wappalyzer, WebPage
from random import randint
from netaddr import IPNetwork
from configparser import ConfigParser


user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111']


def parseURL(url, protocol):

    htmlSource = ''
    if url.startswith('http') is False:
        url = protocol + '://' + url
    try:

        sock = urllib3.urlopen(url, timeout=3)
        htmlSource = sock.read()
        sock.close()
    except urllib3.URLError as e:
        raise Exception("There was an error: {}".format(e))
    except Exception as e:
        raise Exception("There was an error: {}".format(e))
    return htmlSource


def checkValidUrl(url):
    error = False
    try:
        response = urllib3.urlopen(url, timeout=3)
    except urllib3.URLError as e:
        error = True
        if isinstance(e.reason, socket.timeout):
            pass

    except socket.timeout as e:
        error = True
    except Exception as e:
        error = True

    if error:
        return e.getcode()
    else:
        return response.getcode()


def handleCategoryMatch(data, http_object):

    logintype = data['login_type']
    creds1 = data['defaultCreds']

    origTarget = http_object.remote_system
    target = origTarget + data['defaultPath'][0]

    if logintype[0] == 'http_post':
        redirect = False
        try:
            req = urllib3.Request(origTarget)
            opener = urllib3.build_opener(SmartRedirectHandler())
            rsp = opener.open(req)
            code = rsp.getcode()

            if code == 301 or code == 302:

                target = rsp.geturl()
                redirect = True

        except urllib3.URLError as e:
            raise Exception("There was an error: {}".format(e))

        htmlSource = parseURL(origTarget, '')
        inputs = getInputFields(htmlSource)
        if inputs[1] is not None:
            target = updateTarget(http_object.remote_system, inputs[1])
        inputs = inputs[0]

    for x in creds1:
        seperated = re.split(',\s*', x)

    for y in seperated:
        creds = y.split(':')
        username = creds[0]
        password = creds[1]

        if logintype[0] == 'http_auth':
            check = httpAuth(target, username, password)

            if check:
                http_object.default_creds = "Default creds are valid: {}".format(
                    y)
                http_object.category = "successfulLogin"
                http_object._remote_login = target
                break
        elif logintype[0] == 'http_post':

            if inputs is not None:
                postData = getPostData(inputs, username, password)

                if loginPost(origTarget, target, postData, data):
                    http_object.default_creds = "Default creds are valid: {}".format(
                        y)
                    http_object.category = "successfulLogin"
                    http_object._remote_login = target
                    break
                else:
                    http_object.category = "identifiedLogin"

        else:
            pass
    return http_object


def checkLoginForm(html_data):
    try:
        html_proc = beatsop(html_data, "html.parser")

        loginForm = False
        checkLoginForm.new_directory_for_target = None

        forms = html_proc.findAll('form')
        if forms:
            for x in forms:
                if x.findAll('input', {'type': 'password'}) != []:
                    loginForm = True
            return loginForm
        elif html_proc.findAll('a'):

            for one_redirect_link in html_proc.findAll('a'):
                if 'login' in one_redirect_link.get('href') or 'admin' in one_redirect_link.get('href'):
                    checkLoginForm.new_directory_for_target = one_redirect_link.get(
                        'href')

                    return checkLoginForm.new_directory_for_target

    except Exception as e:
        pass


def getInputFields(html_data):

    try:
        html_proc = beatsop(html_data, "html.parser")
        postData = {}
        inputs = []
        allInputs = ['', '']
        action = None

        forms = html_proc.findAll('form')
        for x in forms:
            if x.findAll('input', {'type': 'password'}) != []:
                inputs = x.findAll('input')

                action = x.get('action')

        allInputs[0] = inputs
        allInputs[1] = action
        return allInputs
    except Exception as e:
        pass


def updateTarget(target, action):
    if "http://" in action or "https://" in action:
        target = action
    elif action.startswith('/') and target.endswith('/') is False:
        target = '{}{}'.format(target, action)
    elif target.endswith('/') and action.startswith('/') is False:
        target = '{}{}'.format(target, action)
    elif target.endswith('/') and action.startswith('/'):
        target = '{}{}'.format(target[:-1], action)
    else:
        target = '{}{}{}'.format(target, '/', action)
    return target


def getPostData(inputs, uname, pword):
    postData = {}
    try:
        if inputs != []:
            for y in inputs:
                if 'name' in str(y) or 'user' in str(y) or 'usr' in str(y):
                    if y['type'] == 'text' or y['type'] == 'email':
                        if 'name' in str(y):
                            postData[y['name']] = uname
                        elif 'user' in str(y):
                            postData[y['user']] = uname
                        elif 'usr' in str(y):
                            postData[y['usr']] = uname
                    elif y['type'] == 'password':
                        postData[y['name']] = pword
                    elif y['type'] == 'hidden':
                        if 'value' in str(y):
                            try:
                                postData[y['name']] = y['value'].encode(
                                    'utf-8')
                            except:
                                pass
                        else:
                            postData[y['name']] = ""
                    else:
                        if 'value' in str(y):
                            try:
                                postData[y['name']] = y['value'].encode(
                                    'utf-8')
                            except:
                                pass
                        else:
                            postData[y['name']] = ""
        return postData

    except:
        pass


def loginPost(url, postData, stillTrying=False):

    failChecks = [
        'fail', 'error', 'invalid', 'failed', 'incorrect',
        'try entering it again', 'bad user name', 'bad password',
        'name="password"']
    try:
        result = False

        useragent = user_agents[randint(1, 4)]
        client = requests.session()
        rsp = client.get(url, timeout=3, verify=False)

        if 'csrftoken' in client.cookies:
            csrftoken = client.cookies['csrftoken']
            postData["csrfmiddlewaretoken"] = csrftoken
            headers = {'Referer': url}
            cookies = {'csrftoken': csrftoken}
        else:
            csrftoken = client.cookies['csrf']
            postData["csrfmiddlewaretoken"] = csrftoken
            headers = {'Referer': url}
            cookies = {'csrftoken': csrftoken}

        rsp = requests.post(url, data=postData,
                            cookies=cookies, timeout=3, verify=False)
        content = rsp.text

        client.close()

        if stillTrying is False:
            if rsp.getcode() != 401 or rsp.status_code != 403 and "403" not in content and "401" not in content:

                result = True

            else:

                result = False

        else:
            if any(x in content.lower() for x in failChecks) or rsp.status_code == 401:
                result = False
            else:
                result = True

    except Exception as e:
        raise e
        if isinstance(e.reason, socket.timeout):
            raise Exception("There was an error with {}".format(e))
            result = False

    except socket.timeout as e:
        raise Exception("There was an error with {}".format(e))
        result = False
    except Exception as e:
        raise Exception("There was an error: {}".format(e))

    return result


def httpAuth(target, username, password):

    header = {}
    creds = '{}{}{}'.format(username, ':', password)

    success = False
    try:
        base64string = base64.encodestring(
            '%s:%s' % (username, password)).replace('\n', '')
        header["Authorization"] = "Basic {}".format(base64string)
        request = urllib3.Request(target, "", header)

        request.get_method = lambda: "GET"
        result = urllib3.urlopen(request)
        success = True
    except:
        success = False
    return success


def getAllCreds(dataFile):
    file = open(dataFile, 'r').readlines()
    passwords = []
    listStart = False

    for line in file:
        if listStart:
            if line == '\n' or line == '' or line == '\r\n':
                break
            else:
                passwords.append(line.rstrip())
        if line.startswith("### still trying"):
            listStart = True
    return passwords


def parseURLs(input):
    file = open(input, 'r').readlines()
    urls = []
    listStart = False

    for line in file:
        if listStart:
            if line == '\n' or line == '' or line == '\r\n':
                break
            else:
                urls.append(line.rstrip())
        if line.startswith("###URL"):
            listStart = True
    return urls


def findLogins(http_object, creds, urls):

    validUrls200 = []
    validUrls401 = []
    origTarget = http_object.remote_system
    result = False
    for url in urls:
        target = http_object.remote_system + url
        if checkValidUrl(target) == 200:
            validUrls200.append(target)
        elif checkValidUrl(target) == 401:
            validUrls401.append(target)

    if validUrls401 != []:
        for cred in creds:
            httpAuth(validUrls401[0], cred[0], cred[1])

    if validUrls200 != []:
        for validURL in validUrls200:
            target = validURL
            if result is True:
                break
            source = parseURL(validURL, '')
            if checkLoginForm(source):
                http_object._remote_login = target
                inputs = getInputFields(source)
                if inputs[1] is not None:
                    target = updateTarget(origTarget, inputs[1])
                inputs = inputs[0]
                if inputs is not None:
                    for cred in creds:
                        tempCred = cred.split(':')
                        postData = getPostData(
                            inputs, tempCred[0], tempCred[1])
                        if loginPost(target, target, postData, "", True):
                            http_object.default_creds = "Default creds are valid: {}".format(
                                tempCred)
                            result = True
                            http_object.category = "successfulLogin"
                            http_object._remote_login = target
                            break
                        else:
                            http_object.category = "identifiedLogin"
    return http_object


def getSource(url):
    redirected_url = ""
    source_code = ""
    try:
        requests.packages.urllib3.disable_warnings()
        getsource_response = requests.get(url, verify=False, timeout=2)
        getsource_response_status_code = str(getsource_response.status_code)
        if(getsource_response_status_code == "200"):
            getSource.redirected_url = getsource_response.url
            source_code = getsource_response.text
            return {'source_code': source_code, 'response': getsource_response}
        else:
            getSource.redirected_url = ""
    except (OpenSSL.SSL.Error, ssl.SSLError, requests.Timeout, socket.timeout, requests.exceptions.ConnectionError, requests.exceptions.TooManyRedirects, requests.exceptions.TooManyRedirects, requests.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.SSLError, requests.packages.urllib3.exceptions.ProtocolError, requests.exceptions.ChunkedEncodingError) as sslerror:

        try:
            getsource_response = requests.get(url, timeout=2)
            getSource.redirected_url = getsource_response.url

            getsource_response_status_code = str(
                getsource_response.status_code)
            if(getsource_response_status_code == "200"):
                source_code = getsource_response.text
                return {'source_code': source_code, 'response': getsource_response}

            else:
                getSource.redirected_url = ""
        except (ConnectionResetError, TimeoutError, ConnectionRefusedError, requests.exceptions.ConnectionError, socket.timeout, requests.exceptions.TooManyRedirects, requests.Timeout, requests.exceptions.ReadTimeout, ssl.SSLError, requests.exceptions.SSLError, requests.packages.urllib3.exceptions.ProtocolError, requests.exceptions.ChunkedEncodingError):
            getSource.redirected_url = ""
            pass
    except (ConnectionResetError, TimeoutError, ConnectionRefusedError, socket.timeout) as e:
        getSource.redirected_url = ""

        pass


def search_app_creds(search_string):
    search_string = "django"
    sql_command = "select Username,Password from panel_credentials WHERE Manufactor like lower('%" + search_string + "%') \
                                                      or Product like lower('%" + search_string + "%')    \
                                                      or Revision like lower('%" + search_string + "%')   \
                                                      or Protocol like lower('%" + search_string + "%')   \
                                                      or Username like lower('%" + search_string + "%')   \
                                                      or Password like lower('%" + search_string + "%')   \
                                                      or Access like lower('%" + search_string + "%')     \
                                                      or Validated like lower('%" + search_string + "%');"

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

    search_app_creds.results = cursor.fetchall()

    cursor.close()
    mariadb_connection.close()


def get_db_output(host=None):
    sql_command = """select page_url from founded_sites WHERE host='%s';""" % str(
        host)

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

    get_db_output.results = [''.join(x)
                             for x in cursor.fetchall() if "," not in x]

    cursor.close()
    mariadb_connection.close()


def insert_result_db(login_result, target):

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

    cursor.execute("UPDATE founded_sites SET login_result='%s' WHERE page_url='%s' " % (
        login_result, target))

    mariadb_connection.commit()
    mariadb_connection.close()


def identifier(identifier_response):
    wappalyzer = Wappalyzer.latest()
    webpage = WebPage.new_from_response(identifier_response)
    apps = wappalyzer.analyze(webpage)
    return apps


def checkCreds(target_for_scan, new_url=None):
    identifier_1 = False
    targets_for_scanning = []
    for target in IPNetwork(target_for_scan):
        if new_url == None:
            get_db_output(host=str(target))
            targets_for_scanning = get_db_output.results
        elif new_url == True:
            targets_for_scanning.append(target)
        for target_1 in targets_for_scanning:
            output_get_source = getSource(target_1)
            source_code = output_get_source['source_code']
            getsource_response = output_get_source['response']
            for app in identifier(getsource_response):
                search_app_creds(str(app))
                for info_app in search_app_creds.results:
                    creds = info_app[0] + ":" + info_app[1]

                    try:
                        if source_code is not None and '401 Unauthorized' not in source_code:
                            if identifier_1 is False:
                                check_result = checkLoginForm(source_code)
                                if check_result != None and check_result != True:
                                    if "http" in check_result:
                                        new_target = str(check_result)
                                    elif target_1.endswith("/") != True and check_result.startswith("/") == True:
                                        new_target = str(
                                            target_1) + str(check_result)
                                    elif target_1.endswith("/") != True and check_result.startswith("/") == False:
                                        new_target = str(
                                            target_1) + "/" + str(check_result)
                                    elif target_1.endswith("/") == True and check_result.startswith("/") == True:
                                        new_target = str(
                                            target_1) + str(check_result[1:])
                                    elif target_1.endswith("/") == True and check_result.startswith("/") == False:
                                        new_target = str(
                                            target_1) + str(check_result)

                                    checkCreds(new_target, new_url=True)
                                if check_result == True:

                                    inputs = getInputFields(source_code)
                                    if inputs[1] is not None:
                                        target = updateTarget(
                                            target, inputs[1])
                                    inputs = inputs[0]
                                    if inputs is not None:

                                        tempCred = creds.split(':')
                                        postData = getPostData(
                                            inputs, tempCred[0], tempCred[1])
                                        if loginPost(
                                                target_1,
                                                postData, True):
                                            #                                            login_result = "Successful " + tempCred[0] + ":" + tempCred[1]
                                            login_result = "Successful Logged" + \
                                                tempCred[0] + ":" + tempCred[1]
                                            insert_result_db(
                                                login_result, target_1)
                                        else:
                                            pass

                                else:
                                    continue
                        elif '401 Unauthorized' in source_code:
                            for cred in creds:
                                tempCred = cred.split(':')
                                if httpAuth(
                                        target[0], tempCred[0], tempCred[1]):
                                    #                                    login_result = "Successful " + tempCred[0] + ":" + tempCred[1]
                                    login_result = "Successful Logged" + \
                                        tempCred[0] + ":" + tempCred[1]
                                    insert_result_db(login_result, target_1)
                                    break

                    except Exception as e:
                        result_false = "Login Page Found"
                        insert_result_db(result_false, target_1)
                        pass
                    return info_app
