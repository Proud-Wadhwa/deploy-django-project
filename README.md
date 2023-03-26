# A script to deploy django projects on ubuntu & debian.
  1. To deploy a django project on non-www or subdomain, you can use the specific file deploy.py which helps in this function. This file will deploy django project on provided domain/sub-domain.
  2. To Deploy a django project on www.domain.com you can use a specific file deploy-www.py.

## How to setup project?
  1. Cloning the project and setting up the db.
  2. Virtualenv - venv, This should be your virtualenvironment name because this is set static in py file.
  3. Install Requirements along with gunicorn to deploy this project.

## Basic Operations to use both files.
  1. `Enter the location of the project directory:` - Refers to the project location of project you want to deploy. E.g. `/home/user/project`.
  2. `Enter the Project name:` - Refers to the project name which will be the sock, service and nginx file name. E.g. `project`.
  3. `Enter the name of the inner Django project directory:` - Enter the main project name of the django project which is located inside the main directory or with the manage.py. E.g. `inner_project`.
  4. `Enter the domain name:` - Asks the domain/subdomain name to deploy the django project on. E.g. `example.com`.
  5. `Enter the username:` - Asks the username of the server to add it into gunicorn config. E.g. `user`.
  

**That's It all over**, Now the file will execute necessary commands and make your project live on provided domain.

## Troubleshooting
  1. 502 Bad Gateway: Nginx gives error in this case when the gunicorn file is not working properly. Use `sudo systemctl status project_name.service` this command will show you the error. Majorily the error could be of not installing gunicorn in venv or not finding any other module. This can be also occur due to wrong path, project name or inner project name.
  2. 404 Not Found: Maybe you've entered wrong path, project name or inner project name. To solve this delete gunicorn and nginx files and re-run deploy py file.
    a) Gunicorn Service file path - `/etc/systemd/system/project_name.service`
    b) Nginx Config. File Path - `/etc/nginx/sites-enabled/project_name`
    
  **Note: These files can be vary according to system/os. This is of debian and ubuntu**
 
