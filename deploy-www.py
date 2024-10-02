import os

# Get user input
project_location = input("Enter the location of the project directory: ")
project_name = input("Enter the Project name: ")
inner_project_name = input("Enter the name of the inner Django project directory: ")
domain_name = input("Enter the domain name: ")
cmbs = input("Enter `client_max_body_size`: ")
username = input("Enter the username: ")

# Create Gunicorn service file
gunicorn_service = f"""[Unit]
Description=gunicorn daemon for {project_name}
After=network.target

[Service]
User={username}
Group=www-data
WorkingDirectory={project_location}
ExecStart={project_location}/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:{project_location}/{project_name}.sock {inner_project_name}.wsgi:application

[Install]
WantedBy=multi-user.target
"""

# Create and save Gunicorn service file
with open(f"{project_location}/{project_name}.service", "w") as f:
    f.write(gunicorn_service)

# Create Nginx server block
nginx_block = f"""
server {{
    server_name {domain_name};
    client_max_body_size {cmbs};
    location = /favicon.ico {{ access_log off; log_not_found off; }}
    location /static/ {{
        root {project_location};
    }}
    location /media/ {{
        root {project_location};
    }}
    access_log /var/log/nginx/{project_name}-access.log;
    error_log /var/log/nginx/{project_name}-error.log;
    location / {{
        include proxy_params;
        proxy_pass http://unix:{project_location}/{project_name}.sock;
    }}

    listen 80; # managed by Certbot

}}

server {{
    if ($host = {domain_name}) {{
        return 301 https://{domain_name}/;
    }} # managed by Certbot
    if ($host = www.{domain_name}) {{
        return 301 https://{domain_name}/;
    }} # managed by Certbot
    
    server_name {domain_name} www.{domain_name};

    listen 80;
    return 404; # managed by Certbot


}}

"""

# Create and save Nginx server block
with open(f"{project_location}/{project_name}", "w") as f:
    f.write(nginx_block)

# Restart Nginx and Gunicorn
os.system(f"sudo mv {project_location}/{project_name}.service /etc/systemd/system/")
os.system(f"sudo mv {project_location}/{project_name} /etc/nginx/sites-enabled/")

os.system("sudo systemctl daemon-reload")
os.system(f"sudo systemctl start {project_name}.service")
os.system(f"sudo systemctl enable {project_name}.service")
os.system("sudo systemctl restart nginx")


print(f"\033[1;32;40m \n This Program had deployed {project_name} on {domain_name} \n If there is any error make sure to check the readme.MD Troubleshooting part.")