# Sechand

This is a web application that aims to promote the circulation of second-hand trading information among the locals. In this project, we focus on the JHU community.

## Installing / Getting started

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

## Developing

Detailed and step-by-step documentation for setting up local development. For example, a new team member will use these instructions to start developing the project further. 

```shell
commands here
```

You should include what is needed (e.g. all of the configurations) to set up the dev environment. For instance, global dependencies or any other tools (include download links), explaining what database (and version) has been used, etc. If there is any virtual environment, local server, ..., explain here. 

Additionally, describe and show how to run the tests, explain your code style and show how to check it.

If your project needs some additional steps for the developer to build the project after some code changes, state them here. Moreover, give instructions on how to build and release a new version. In case there's some step you have to take that publishes this project to a server, it must be stated here. 
