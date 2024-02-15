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
    - Primary Database: PostgreSQL
    - ORM: Django built-in ORM
- Deployment:
    - Hosting: Heroku
    - Continuous Integration/Continuous Deployment (CI/CD): Github Action

*For additional informations about the technology stack we used, please refer to Issue #2*

## Getting Started

### Versions

SecHand is developed using the following version of technologies:
```
    - Node.js: 20.11.0
    - Django: 5.0.1
        - Python 3.12.1
    - Vue: 3.4.19
```

### Installation

#### (0) Install Python and Node.js

- Before starting install any dependencies, make sure you installed Python and Node.js on your computer. 
    - Although it is recommended to install the same version we have, any higher version of Python should works.
    - Check the following website to install [Python](https://www.python.org/downloads/), and [Node.js](https://nodejs.org/en)
- You should also make sure that package managers like `pip` and `npm` are also installed.

#### (1) Setup the virtural environment.

- If you have installed either Node/Python/Django on your computer with different versions, and do not wish to install another version of these due to your personal project dependencies. We recommened using a virtural environment to install the necessary packages.
    - To create a vertural environment, under the root folder of SecHand, uses the following command:
        ```cmd
        python -m venv <virtural env name>
        ```
        For example, use:
        ```cmd
        python -m venv venv_3_12_1 
        ```
        to represent a virtural environment with python version 3.12.1

#### (2) Start the virtural environment

- After created a virtural environment for this, you can use the following command to start it:
    ```cmd
    .\venv_3_12_1\Scripts\activate
    ```
- This will start the virtural env and create a mark before your terminal prompt. 
- To exit from the virtural environment, use:
    ```cmd
    deactivate
    ```

#### (3) Install Django backend dependencies

- To install necessary dependencies, navigate to the root folder of the project, where requirements.txt is located, and run:
    ```cmd
    pip install -r .\requirements.txt
    ```
    
#### (4) Run the Django backend
##### (4.1) Database model migrations

- If any models has been changed since last migration, use the following command to migrate them to the database. 
- Under the backend directory (\sechand_backend). Run the following commands to migrate the database:

    ```cmd
    python .\manage.py makemigrations
    ```

    ```cmd
    python .\manage.py migrate
    ```

##### (4.2) Run the Django backend
- Under the same backend directory (\sechand_backend), run the following command to start the backend server:
    ```cmd
    python .\manage.py runserver
    ```
- Now If everything works correctly, you should see Django is up and running, prompting:
    ```
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    <Server start time>
    <Django version>, using settings <settings file path>
    Starting development server at <server running location>
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
    Local:   <running location>
    Network: use --host to expose
    press h + enter to show help
    ```

- The frontend should now running on: http://localhost:5173/

#### (7) Open  the following link in a browser: [Sechand](http://localhost:5173 )

## Developing

If you are developing on SecHand and setting up the environment, please refer to the **Installation** section of this file.

### Global configuration

*The content of this section will be completed during developing cycle*

### Running tests

*The content of this section will be completed during developing cycle*
