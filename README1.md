# Sechand - A second-hand dealing web application

## 1. Environment

**OS: Windows 10**

**IDE: VSCode**

**Browser: Edge**

## 2. Tech Stack

### (1) Frontend:

**Framework: vue3 (v 3.4.15)**

**JavaScript node.js v 20.11.0**

### (2) Backend:

**Framework: Django (v 5.0)**

**Python: v 3.12.1**

### (3) Database:

**Engine: MySQL8.0**

### 3. Run Locally

#### (0) Make sure you have a up-to-date version of [Node.js](https://nodejs.org/en), [MySQL8.0](https://dev.mysql.com/downloads/) and [Python3.12](https://www.python.org/downloads/) installed before setting up.

#### (1) Setup the database.

##### (1.1) Make sure the mysql service is on (for Windows computers, I go to task manager --> service --> mysql80 --> right click and start, or you may [Start MySQL from the Windows Command Line](https://dev.mysql.com/doc/refman/8.0/en/windows-install-archive.html).

Please be aware of your local user name, local user password and local port number.


##### (1.2) Create a new database called "sechand". I suggest you use a [MySQL Workbench](https://www.mysql.com/products/workbench/). You can either run the command or use the GUI to manipulate the database.

```sql
create DATABASE sechand
```

##### (1.3) Configure the connection between Django and MySQL. You can change any of these settings in /sechand_backend/sechand_backend/settings.py line 89 to 98 into your settings. My settings are as following:

Database name: **Sechand**

Local user name: **root**

Local user password: **123456**

Local port: **3306**

##### (1.4) Go to the backend directory (/sechand_backend/sechand_backend/) in a console. Run the following commands to migrate the database:

```cmd
python3.12 manage.py makemigrations
```

```cmd
python3.12 manage.py migrate
```


#### (2) You need a few Python packages before launching teh backend server. Run the following commands to ensure that they are installed for Python3.12.

```cmd
python3.12 -m pip install django
```

```cmd
python3.12 -m pip install pymysql
```

```cmd
python3.12 -m pip install mysqlclient
```

#### (3) Go to the backend directory (/sechand_backend/sechand_backend/) in a console and run the following command to start the backend server.


```cmd
python3.12 manage.py runserver
```

Now the frontend server is running on port: http://localhost:8000.

#### (4) Go to the frontend directory (/sechand) in a console. I inculde the modules in the folder so you do not need to install any dependencies. However, to make sure everything needed exists, run the command:

```cmd
npm install
```

#### (5) Run the following command to start the frontend server.

```cmd
npm run dev
```

Now the backend server is running on port: http://localhost:5173

#### (6) Open  the following link in a browser to start the web app.

[Sechand](http://localhost:5173 )

##### (7) The pages are temporarily designed for only (2520 * 1440) display so it is strongly recommanded to zoom in or zoom out the pages to a proper size if you use a display with other sizes (e.g. 80% for a 1920 * 1080 screen).