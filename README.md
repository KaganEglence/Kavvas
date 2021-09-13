<h1 align="center"> This project is no longer supported </h1>

<p align="center">
    <img width=20% src="images/logo.png">
  </a>
</p>


<h1 align="center"> Kavvas </h1>
<div align="center">
Kavvas is scanner for misconfigured web applications. Shortly, it scans given target IP range for web applications, attempt login and get screenshots of pages.
It can be managed easily with web interface.
</div>
<br>



<p align="center"><img width=50% height=auto src="https://github.com/KaganEglence/Kavvas/blob/master/images/Kavvas.gif"></p>


# Capabilities


* Network Scan  
  * Performs basic network scans for live hosts.


* Web Scan
  * Detects web pages and performs source code scan for identify possible login pages.


* Identify Login Pages  
  * Identify components on websites. Can uncover the most components used on website.


* Attempt Login to Target
  * If target have identified as login page, detects website components and attempt login with these components default passwords in database.


* Taking Screenshot
  * Gathers screenshots from websites on target ip range.


* Monitoring on Web Service  
  *  Gathered screenshots can be view on web interface easily.



# Prerequirements
* [Python3](https://www.python.org/downloads/)
* [Mysql](https://dev.mysql.com/doc/refman/8.0/en/linux-installation.html)
* [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)


#  Installing

**1)** Setup Virtualenv and Django

    git clone https://github.com/KaganEglence/Kavvas.git
    chmod +x install.sh
    ./install.sh


**2)** Database Settings

    mysql -u username -p -e "create database custom_db_name"
    mysql -u username -p custom_db_name < db/Kavvas.sql

**3)** Starting Web Service

    source Kavvas_env/bin/active
    python3 manage.py runserver

**4)** Setup Database Config From Web

    http://127.0.0.1:8000/settings/






# Usage:

#### #Settings

<p align="center"><img width=auto src="https://github.com/KaganEglence/Kavvas/blob/master/images/settings.png"></p>

Creating config file for database connection.

* **Host:** Database Address(i.e., 1.2.3.0)  
* **Port:** Database Port(i.e., 3306.)  
* **Name:** Database Name for connection.(e.g., custom_db_name or Kavvas.)  
* **Username:** Database Username.(e.g., root, Kavvas_User.)




#### #Panels Info

<p align="center"><img width=auto src="https://github.com/KaganEglence/Kavvas/blob/master/images/panels_info.png"></p>

Knowledge database for known Web Applications.
You can add new values to database or read saved values from database.  This values using for trying to login founded and identified panels.

While all fields empty it will returns all values from database. (i.e., username:admin, password:admin)



#### #Scanner

<p align="center"><img width=auto src="https://github.com/KaganEglence/Kavvas/blob/master/images/scanner.png"></p>


This page scans given targets for Web Applications.  
Target could be a "single ip" or subnet.(e.g., "1.2.3.0" , "1.2.3.0/24" , "1.2.3.0/16"...)


#### #Login Page Scanner

<p align="center"><img width=auto src="https://github.com/KaganEglence/Kavvas/blob/master/images/login_page_scan.png"></p>

Starts to attempt login for founded targets. Results can be seen in the "Founded Sites" part. Target could be a "single ip" or subnet.(e.g., "1.2.3.0" , "1.2.3.0/24" , "1.2.3.0/16"...)


#### #Founded Sites

<p align="center"><img width=auto src="https://github.com/KaganEglence/Kavvas/blob/master/images/founded_sites.png"></p>

Gets results of scans from database.

* **Target Ip:** Get results by specific target.(e.g., 1.2.3.0, 1.2.3.0/24 or null for all results.)  
* **Target Port:** Get results by specific port.(e.g., 80, 446, 8000 or null for all results.  
* **Source Scan:** Get results by source scan. For identified login pages, this value should be True.  
* **Result of Login Scan:** The results of attempts to log in.
  *	**Successful Logged:** The login page was found with login information and logged in.  
  * **Login Page Found:** Login page founded but tried creds not valid.


* **Take Screenshot:** Optionally starts to get screenshots of results. Screenshots can be seen in the "Screenshots" part.




#### #Screenshots

<p align="center"><img width=auto src="https://github.com/KaganEglence/Kavvas/blob/master/images/screenshots.png"></p>

If "Take Screenshots" part selected in the "Founded Sites", results can be seen in here.



## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Python3](https://www.python.org/) - Language
* [Bootstrap](https://getbootstrap.com/) - HTML, CSS, and JS library.


## Security
* **The input parameters have not been tested. Possible injection attacks are currently on.** *

## Author

* **Kağan Eğlence** - [Github](https://github.com/KaganEglence/)



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
