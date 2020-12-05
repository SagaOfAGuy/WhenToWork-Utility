# WhenToWork Utility

Script for automating schedule and paystub retrieval for **only those that have a valid When2Work account**. This command-line utility allows you to automate your browser and screenshot work schedules and team work schedules in PNG format. 

## Installation
Install pipenv if not installed on system, assuming pip3 is installed:

```bash
pip3 install pipenv
```
Now that pipenv is installed, navigate to this project's directory, or wherever you've installed it:

```bash
cd /path/to/When2Work
```
Execute the following Pipenv command to install the dependencies needed for this project found within the Pipfile, which is found within the project directory: 
```bash
pipenv install
```

If Pipenv isn't installing properly, edit the Pipfile, and change the python version in the Pipfile:
```bash
# Find Python3 version
python3 --version

# Edit this part of the Pipfile to whatever python version you have. In the example below, the python version is 3.9. 
python_version = "3.9"
```

## Configuring Credentials for When2Work login

First, navigate to the directory where you downloaded the project:
```bash 
cd /path/to/When2Work
```
Create a file named "creds.env" to store credentials: 
```bash 
touch creds.env
```
Use your favorite text editor to edit the file you just created: 
```bash 
nano creds.env
```
Create two environment variables, and set them equal to your  credentials
```bash
WHEN2WORK_USER="usernamegoeshere"
WHEN2WORK_PASS="passwordgoeshere"
```

## Usage
```bash
# If you want to get screenshots of your personal schedule
python3 When2Work.py self

# If you want to get screenshots of team schedule
python3 When2Work.py team 
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
