# SecHand

SecHand is a web application that aims to promote the circulation of second-hand trading information among the locals. It provides a platform for students to post their pre-owned items online anytime when they have a product that is idled. 

## Technology Stack

SecHand is build based on the following technology:

- Frontend:
    - Frameworks: Vue.js
    - Styling: Bootstrap
- Backend:
    - API: Django
- Database:
    - Primary Database: Heroku PostgreSQL
    - Testing Database: Azure PostgreSQL
    - ORM: Django built-in ORM
- Deployment:
    - Hosting:
        - Frontend Web: Vercel
        - Backend Server: Heroku
    - Continuous Integration/Continuous Deployment (CI/CD): Github Action

*For additional informations about the technology stack we used, please refer to Specifications*

## Getting Started

### Versions

SecHand is developed using the following version of technologies:
```
    - Node.js: 20.11.0
    - Django: 5.0.1
        - Python 3.12.1
    - Vue: 3.4.19
```

### Installation and Run

#### (0) Install Python and Node.js

- Before starting install any dependencies, make sure you installed Python and Node.js on your computer. 
    - Although it is recommended to install the same version we have, any higher version of Python should works.
    - Check the following website to install [Python](https://www.python.org/downloads/), and [Node.js](https://nodejs.org/en)
- You should also make sure that package managers like `pip` and `npm` are also installed.

#### (1) Setup the virtural environment.

- ***If you don't want to install and enable virtural environment, Jump to Step 3.***
    
    ---

- If you have installed either Node/Python/Django on your computer with different versions and don't want to install another version of these due to your personal project dependencies, you can use a virtural environment to install the necessary packages that required by SecHand.
    - To create a vertural environment, under the root folder of SecHand, uses the following command:
        - For Windows
            ```cmd
            python -m venv <virtural env name>
            ```
        - For Mac
            ```cmd
            python3 -m venv <virtural env name>
            ```
            For example, use:
            ```cmd
            python -m venv venv_3_12_1
            or
            python3 -m venv venv_3_12_1
            ```
            to represent a virtural environment with python version 3.12.1
    - *We'll use folder name *venv_3_12_1* in the following README file*.

#### (2) Start the virtural environment

- After created a virtural environment for this, you can use the following command to start it:
    - For Windows
        ```cmd
        .\venv_3_12_1\Scripts\activate
        ```
    - For Mac
        ```cmd
        source venv_3_12_1/bin/activate
        ```
- This will start the virtural env and create a virtural env mark, you may find it inside your terminal. 
- To exit from the virtural environment, use:
    ```cmd
    deactivate
    ```
    or if the above doesn't work and you are running on Mac, try:
    ```cmd
    source venv_3_12_1/bin/deactivate
    ```

#### (3) Install Django backend dependencies

- To install necessary dependencies, first you need to navigate to the root folder of the backend server, use:
    ```cmd
    cd sechand_backend
    ```
    
- In `sechand_backend`, where requirements.txt is located, run:
    ```cmd
    pip install -r requirements.txt
    ```
    
- If you see the `psycopg2` error when starting the backend, then try to manually install it again, try:
    ```cmd
    pip install psycopg2-binary==2.9.9
    ```
    *We've noticed that this error likely happends on MAC machine, but currently we have no clue what leads to this issue.*

#### (4) Run the Django backend
##### (4.1) Database model migrations

- If any models has been changed since last migration, use the following command to migrate them to the database. 
- Under the backend directory (\sechand_backend) where manage.py is located. Run the following commands to migrate the database:

    ```cmd
    python manage.py makemigrations
    ```
    then
    ```cmd
    python manage.py migrate
    ```

##### (4.2) Run the Django backend
- Under the same directory (\sechand_backend), run the following command to start the backend server:
    ```cmd
    python manage.py runserver
    ```
- Now If everything works correctly, you should see the server is up and running, prompting:
    ```
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    <Server start time>
    <Django version>, using settings sechand_backend.settings
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
    ```
- The server is now running on: http://localhost:8000

#### (5) Install Vue frontend dependencies
- After the backend has successfully up and running, next step is to start the front end of SecHand.
- Go to the frontend directory (\sechand). Run the following command to install dependencies used by frontend:
    ```cmd
    npm install
    ```
- A `node_modules` folder will be created and all dependencies will be installed in there.

#### (6) Run the Vue frontend

- Use the following command to start the frontend:
    ```cmd
    npm run dev
    ```

- Now If everything works correctly, you should see Django is up and running, prompting:
    ```
    ...
    Local:   http://localhost:5173/
    Network: use --host to expose
    press h + enter to show help
    ```

- The frontend should now running on: http://localhost:5173/

## Developing
- **Remember NOT INCLUDE any cache file to the repo, add them to .gitignore** 

- If you are developing on SecHand and setting up the environment, please refer to the **Installation** section of this file.

### Backend Development
- Use `pip freeze > requirements.txt` to populate requirements file.
- Note that due to properties of Django, **everytime**, if you make **any changes to the database model**, remember to migrate the model, or you won't see it in the database. Migration commands see ***Section 4.1***.
    - If you saw some red warning message related to database model after launching the backend, you should also consider making a migration.
- When creating and editing models, you might encounter issues like migrations did not work; or after you accidently deleted Database table(but you are not supposed to do that), consider the following solutions:
    - Completely delete all migration files like "0001_initial.py"(don't delete the folder)
    - Make sure the models.py file contains the correct model you want it to be, then try makemigrations again
        ```cmd
        python manage.py makemigrations
        ```
        This will let Django recreate the fist migration file 0001_initial.py.
    - Then use the following command to see equivalent SQL commands:
        ```cmd
        python manage.py sqlmigrate <Django app name> 0001
        ```
        And the following command will be displayed
        ```
        BEGIN;
        --
        -- Create model <model name>
        --
        CREATE TABLE "<table name>" (...);
        ...
        COMMIT;
        ```
        Use the SQL command above, to manually create new table inside your database.
### Global configuration

*The content of this section will be completed during developing cycle*

### Running tests

#### Run Backend tests
- Tests will run on another cloud database: **Azure PostgreSQL**, rather than production database.
- We use `unitest` for testing backend server, focusing on:
    - Model creation
    - Serializer functionality
    - API endpoint functionality

- Test files are located at:
    - `/sechand_backend/post/tests` and `/sechand_backend/user/tests`

- To run tests, navigate to `/sechand_backend` and run:
    ```cmd
    python manage.py test --settings=sechand_backend.settings_test
    ```
    this will let Django to detect all tests and run all of them.