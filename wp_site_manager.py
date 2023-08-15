#!/usr/bin/env python3

import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIGS_DIR = os.path.join(BASE_DIR, "configs")
SITES_DIR = os.path.join(BASE_DIR, "sites")

def check_dependencies():
    try:
        subprocess.run(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        subprocess.run(["docker-compose", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError:
        print("Docker or docker-compose is not installed. Please install them before proceeding.")
        sys.exit(1)

def create_wordpress_site(site_name):
    # Modify /etc/hosts
    hosts_entry = f"127.0.0.1    {site_name}\n"
    hosts_path = "/etc/hosts" if sys.platform.startswith("linux") else "C:/Windows/System32/drivers/etc/hosts"
    with open(hosts_path, "a") as hosts_file:
        hosts_file.write(hosts_entry)
    
    # Create site directory
    site_dir = os.path.join(SITES_DIR, site_name)
    os.makedirs(site_dir, exist_ok=True)

    # Create docker-compose.yml for LEMP stack
    with open(f"{CONFIGS_DIR}/docker-compose-lemp.yml", "r") as compose_template:
        compose_content = compose_template.read().replace("{SITE_NAME}", site_name)
    
    with open(f"{site_dir}/docker-compose.yml", "w") as compose_file:
        compose_file.write(compose_content)
    
    print(f"Great! Your new WordPress site '{site_name}' is ready to be set up.")
    print(f"Navigate to {site_dir} and run 'docker-compose up -d' to start the site.")

def enable_wordpress_site(site_name):
    site_dir = os.path.join(SITES_DIR, site_name)
    if os.path.exists(site_dir):
        subprocess.run(["docker-compose", "-f", f"{site_dir}/docker-compose.yml", "up", "-d"])
        print(f"WordPress site '{site_name}' is now enabled. Your site is up and running!")
    else:
        print(f"The WordPress site '{site_name}' does not exist.")

def disable_wordpress_site(site_name):
    site_dir = os.path.join(SITES_DIR, site_name)
    if os.path.exists(site_dir):
        subprocess.run(["docker-compose", "-f", f"{site_dir}/docker-compose.yml", "down"])
        print(f"WordPress site '{site_name}' is now disabled. Containers are stopped.")
    else:
        print(f"The WordPress site '{site_name}' does not exist.")

def delete_wordpress_site(site_name):
    site_dir = os.path.join(SITES_DIR, site_name)
    if os.path.exists(site_dir):
        subprocess.run(["docker-compose", "-f", f"{site_dir}/docker-compose.yml", "down", "-v"])
        os.remove(f"{site_dir}/docker-compose.yml")
        print(f"WordPress site '{site_name}' has been deleted, including containers and files.")
    else:
        print(f"The WordPress site '{site_name}' does not exist.")

def main():
    if len(sys.argv) < 2:
        print("Usage: wp_site_manager.py [check|create|enable|disable|delete] [sitename]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        check_dependencies()
    elif command == "create":
        if len(sys.argv) != 3:
            print("Usage: wp_site_manager.py create [sitename]")
            sys.exit(1)
        site_name = sys.argv[2]
        create_wordpress_site(site_name)
    elif command == "enable":
        if len(sys.argv) != 3:
            print("Usage: wp_site_manager.py enable [sitename]")
            sys.exit(1)
        site_name = sys.argv[2]
        enable_wordpress_site(site_name)
    elif command == "disable":
        if len(sys.argv) != 3:
            print("Usage: wp_site_manager.py disable [sitename]")
            sys.exit(1)
        site_name = sys.argv[2]
        disable_wordpress_site(site_name)
    elif command == "delete":
        if len(sys.argv) != 3:
            print("Usage: wp_site_manager.py delete [sitename]")
            sys.exit(1)
        site_name = sys.argv[2]
        delete_wordpress_site(site_name)
    else:
        print("Unknown command.")
        sys.exit(1)

if __name__ == "__main__":
    main()
