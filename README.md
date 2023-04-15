# It is very important to have docker-desktop installed preferably on Windows
The Zscaler can restrict the installation of docker-desktop,
talk to Javi or enrique to have permission to installation.

# Ikm backend repository, Windows installation 🙌 
Install python and pip > 3.5 in windows, pip is included with the installation of python
https://www.python.org/downloads/ 

## 1. Clone the backend repository 
Create a folder with the name IKMWEB and inside of the folder,
clone the repository https://github.com/AntProRo/ikmback.git

## 2. Install dependencies
Open the terminal and then go to the path of the folder ikmback then type this line
pip install - r requirements.txt

# Ikm frontend repository, Windows installation 🙌 
install node.js >= 17 in windows
https://nodejs.org/es

## 1. Clone the frontend repository
Inside of the folder IKMWEB,
clone the repository https://github.com/AntProRo/ikmfront.git

## 2. Install dependencies
Open the terminal and then go to the path of the folder ikmfront then type this line
npm install

# Docker database setUp 🙌 
https://apx365-my.sharepoint.com/:u:/g/personal/anrodriguez_apexsystems_com/ETfu3M5vw-BGkSb_B6tUoWMBxh9NHoqU0bDWV8NdILYYAg
Copy the file Docker-compose.yml to the root of IKMWEB folder

IKMWEB├── ikmfront
      ├── ikmback
      ├── Docker-compose.yml

## 1. Build images
Here we will know, if the backend and frontend dependencies are installed correctly
but the most important step is  build the database.

open the terminal and go inside of the folder IKMWEB and type
1. docker-compose build
--- if is completed ----
2. docker-compose up

## The application must run successfully the frontend, backend and database containers
✅ The browser will open automatically the localHost: http://localhost:3000/
      
# How to edit the project and see the changes❓❓
Kill with ctrl C or stop all the containers then 
(in docker-desktop app ), run only the db-1 container 

## 1. Run the backend application
Open terminal and go inside of the folder ikmback and type this line.
python manage.py runserver 

--- ✅ happy code ---

## 2. Run the frontend application
Open terminal and go inside of the folder ikmfront and type this line.
npm start

--- ✅ happy code ---