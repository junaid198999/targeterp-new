# Ubold Django - Vertical Layout #

### Getting Started ###

Follow below steps to setup Django and associated stacks:
  
- Make sure to have python3, pip3 and virtual environment installed on your system
- Install all dependencies using command `pip install -r requirements/local.txt`
- Create database and run migrations using command `python manage.py migrate`

You can refer to django-cookiecutter project's [
](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html) for more detailed steps.

Follow below steps to setup frontend related stuff (Live reloading, SASS compilation, etc):
  
 - Make sure to have node and npm installed on your system
 - Install node and npm on your system
 - Install gulp globally using command `npm install -g gulp-cli` & `npm install -g gulp`
 - Install local dependencies using command `npm install`
 - Now you can just run command `gulp` to start server with live reloading and saas compilation enabled.


**Following are the available commands:**
 - `gulp` - The base app will run as it would with the usual `manage.py  runserver` but with live reloading and Sass compilation enabled. When changing your Sass files, they will be automatically recompiled and change will be reflected in your browser without refreshing.
 -  `python manage.py createsuperuser` - create a superuser
 - `pytest` - Runs tests with py.test
 - `coverage run -m pytest & coverage html  & open htmlcov/index.html` - Runs tests and check for coverage

