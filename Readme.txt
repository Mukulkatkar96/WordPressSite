*WordPress Site Manager
The WordPress Site Manager is a tool designed to simplify the process of creating, managing, and deleting WordPress sites using Docker and Docker Compose.
Follow the steps below to effectively manage your WordPress sites.

-Prerequisites
Docker and Docker Compose are required for this tool to function. Make sure they are installed and running on your system. If using an AWS EC2 instance, ensure that Docker is started and enabled after installation.

Getting Started

*Run the following command to create a new WordPress site:

1. python3 ./wp_site_manager.py create Your_site_name


2. Change into the directory of the created site:
cd sites/Your_site_name

Start the site's containers using Docker Compose:
docker-compose up -d


3. To access the site, use the following Docker run command:

docker run -d -p 8001:80 --name my-wordpress wordpress
(Note: If using an AWS EC2 instance, ensure that inbound rules allow traffic on port 8001 and access with local public_ip:8001)


*Enabling and Disabling Sites

4. To enable a site and start its containers, run:
python3 wp_site_manager.py enable Your_site_name


5. To disable a site and stop its containers, run:
python3 wp_site_manager.py disable Your_site_name


6. Deleting a Site

To completely delete a site, including its containers and files, run:
python3 wp_site_manager.py delete Your_site_name



Feel free to replace "Your_site_name" with the actual name of the site you're working with. This README provides a clear overview of the tool's functionalities and the necessary steps to follow for different operations.
