# CTF_challenge

This repository is a Dockerized Django and flask application containing XEE and SQLI vulnerability challenges.

That includes 3 flags.

Flag1: After solving XEE challenge and viewing the file : /etc/passwd

Flag2: Login page to the flask app: path -> /etc/hosts

Flag3: After solving the SQLi challenge and entering the login page.


# Quick Start Using Docker


To access the challenges, you need docker and docker-compose installed. 

Clone the repository

$ git clone https://github.com/MaryamMozaffari97/vulx_challenge.git

Open the main directory of the project (where docker-compose.yml file exists)

## Run this command:

$docker-compose up --build -d

Access the challenges with this URL: http://localhost:80
