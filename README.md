# Deployment Process

## Pre-requisites

1. Install git

    > sudo apt install git

2. Make sure python3 is installed

    > python3 -V

    _**Note**: Python3 version should be 3.10, but if other version is installed, then same version need to be reflected in pyproject.toml file._

3. Install poetry

    Before going into installing poertry, install few required dependencies

    > sudo apt install python3-distutils python3-dev build-essential python3-venv libssl-dev libffi-dev

    > curl -sSL https://install.python-poetry.org | python3 -

    Update PATH in bashrc/zshrc

    > export PATH="$PATH:$HOME/.local/bin"

## Setup

1. Clone the repository

    > git clone https://github.com/pratikGhodke1/greythr-automation.git

2. Update poetry setting to create venv folder in project directory.

    > poetry config --local virtualenvs.in-project true

3. Install python dependencies
    > poetry install

4. Install google chrome
    > wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

    > sudo dpkg -i google-chrome-stable_current_amd64.deb


# Service Setup

1.  Create service file

    > sudo nano /etc/systemd/system/autohr.service

2.  Add service configuration. Remember to update User (3 placed)

    ```
    [Unit]
    Description=Automated GreytHR application to signIn and singOuts.
    After=network.target

    [Service]
    User=pratik_ghodke
    WorkingDirectory=/home/pratik_ghodke/greythr-automation/
    ExecStart=/home/pratik_ghodke/greythr-automation/.venv/bin/gunicorn --bind 0.0.0.0:5000 "wsgi:application"
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

3. Change the timezone to IST
   
    > sudo timedatectl set-timezone Asia/Kolkata

    > export TZ="Asia/Kolkata"
    > > __Note__: _Some times there will conflict between the /etc/localtime and /etc/timezone files, just add "Asia/Kolkata" in /etc/timezone._

4. Test and check timezone
   
    > timedatectl

5. Add `FERNET_KEY` environment variable

5.  Reload daemon service

    > sudo systemctl daemon-reload

6.  Start AutoHR service

    > sudo systemctl start autohr

7.  Check AutoHR service status
    > sudo systemctl status autohr

# Usage

1. Register yourself

    ```
    POST /api/v1/employee
    {
        "eid": "S123",
        "password": "greythr_password",
        "name": "your_name"
    }
    ```

    Upon registering you will be automatically signed in after 9:00AM and signed out after 7:30PM withing 1 hour past that.

2. To manually sign in and sign out

    > GET /api/v1/employee/punch/s123

3. Delete your entry from the application
    > DELETE /api/v1/employee/s123

## Other Endpoints

-   GET / - Welcome Message
-   GET /api/v1/employee - Instructions on how to register
