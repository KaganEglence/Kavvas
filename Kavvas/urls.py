from django.conf.urls import url
from Kavvas import views

urlpatterns = [
    url(r'^$', views.HomePageView , name = 'index'),
    url(r'^index/$', views.HomePageView , name = 'index'),
    url(r'^scanner/$', views.ScannerPageView , name='scanner'),
    url(r'^screenshots/$', views.ScreenshotPageView, name='screenshots'),
    url(r'^panels_info/', views.PanelsInfoPageView, name='panels_info'),
    url(r'^help/$', views.HelpPageView, name = 'help'),
    url(r'^settings/$', views.SettingsPageView, name = 'settings'),
    url(r'^founded_sites/$', views.FoundedSitesPageView, name = 'founded_sites'),
    url(r'^login_page_scan/$', views.LoginPageScanView, name = 'login_page_scan'),
]
