from django.shortcuts import render
from .python_files import all_scripts_for_djago
from django.http import HttpResponse
import mysql.connector as mariadb
import netaddr


def HomePageView(request):
    return render(request, 'index.html')


def ScannerPageView(request):
    if request.POST:
        try:
            all_scripts_for_djago.scan_target(
                target=request.POST['post_target'])
            scan_response = {"Scan Started...": ""}
            return render(request, 'scanner.html', {'Scan_response': scan_response, })

        except netaddr.core.AddrFormatError:
            scan_response = {"Invalid Target": ""}
            return render(request, 'scanner.html', {'Scan_response': scan_response, })
    else:
        return render(request, 'scanner.html', context=None)


def ScreenshotPageView(request):
    if request:
        screenshot_files = all_scripts_for_djago.founded_screenshots()

        return render(request, 'screenshots.html', {'screenshot_files': screenshot_files, })

    else:
        return render(request, 'screenshots.html')


def PanelsInfoPageView(request):
    try:
        if request.GET:
            outputs = all_scripts_for_djago.search_db(manufactor=request.GET['get_Manufactor'], Product=request.GET['get_Product'], Revision=request.GET['get_Revision'], Protocol=request.GET[
                                                      'get_Protocol'], Username=request.GET['get_Username'], Password=request.GET['get_Password'], Access=request.GET['get_Access'], Validated=request.GET['get_Validated'])

            return render(request, 'panels_info.html', {'outputs': outputs, })

        elif request.POST:

            add_response = all_scripts_for_djago.add_value(manufactor=request.POST['post_Manufactor'], Product=request.POST['post_Product'], Revision=request.POST['post_Revision'], Protocol=request.POST[
                                                           'post_Protocol'], Username=request.POST['post_Username'], Password=request.POST['post_Password'], Access=request.POST['post_Access'], Validated=request.POST['post_Validated'])
            add_response = {"Value Added": add_response}
            return render(request, 'panels_info.html', {'added_value': add_response, })

        else:
            return render(request, 'panels_info.html')
    except mariadb.errors.InterfaceError:
        return render(request, 'database_error.html')


def HelpPageView(request):
    return render(request, 'help.html', context=None)


def SettingsPageView(request):
    if request.POST:
        try:
            all_scripts_for_djago.edit_settings(db_host=request.POST['db_host'], db_port=request.POST['db_port'],
                                                db_name=request.POST['db_name'], db_username=request.POST['db_username'], db_password=request.POST['db_password'])
            scan_response = {"Config Files Edit...": ""}
            return render(request, 'settings.html', {'Scan_response': scan_response, })

        except Exception as e:
            raise Exception

    else:
        return render(request, 'settings.html', context=None)

    return render(request, 'settings.html', context=None)


def LoginPageScanView(request):
    if request.POST:
        try:
            all_scripts_for_djago.scan_login_forms(
                target=request.POST['post_target'])
            scan_response = {"Scan Started...": ""}
            return render(request, 'login_page_scan.html', {'Scan_response': scan_response, })

        except mariadb.errors.InterfaceError:
            return render(request, 'database_error.html')

        except netaddr.core.AddrFormatError:
            scan_response = {"Invalid Target": ""}
            return render(request, 'login_page_scan.html', {'Scan_response': scan_response, })
    else:
        return render(request, 'login_page_scan.html', context=None)


def FoundedSitesPageView(request):
    try:
        if request.GET:
            screenshot_choice = request.GET.get("screenshot_choice")
            if screenshot_choice is not None:
                if screenshot_choice == "on":
                    founded_outputs = all_scripts_for_djago.founded_sites_output(
                        host=request.GET['get_host'], port=request.GET['get_port'], source_type=request.GET['get_source_type'], get_result_of_login_scan=request.GET['get_result_of_login_scan'])
                    for one_output in founded_outputs[1:]:
                        all_scripts_for_djago.gather_screenshot(
                            str(one_output[2]))

                    return render(request, 'founded_sites.html', {'founded_outputs': founded_outputs, })

                else:
                    founded_outputs = all_scripts_for_djago.founded_sites_output(
                        host=request.GET['get_host'], port=request.GET['get_port'], source_type=request.GET['get_source_type'], get_result_of_login_scan=request.GET['get_result_of_login_scan'])

                    return render(request, 'founded_sites.html', {'founded_outputs': founded_outputs, })
            else:
                founded_outputs = all_scripts_for_djago.founded_sites_output(
                    host=request.GET['get_host'], port=request.GET['get_port'], source_type=request.GET['get_source_type'], get_result_of_login_scan=request.GET['get_result_of_login_scan'])

                return render(request, 'founded_sites.html', {'founded_outputs': founded_outputs, })
        else:
            return render(request, 'founded_sites.html')
    except mariadb.errors.InterfaceError:
        return render(request, 'database_error.html')
