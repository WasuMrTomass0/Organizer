# ![organizer_logo](data/organizer_logo.png)

Organiser is an app created to keep track of stored items in boxes or containers.
The main idea of this app is to take a photo of an item, throw it to the container, label it in an app and quickly find it when it is needed again.

App is made of 3 elements:
- location - general description of a place, for example: garage, attic
- container - specific container labeled with integer ID
- item - stored item that can be found by name look up (may contain image, description adn quantity info)

## Demo

TBD

## Runnning

### MySQL Database

You must have an access to MySQL database. I am using [MariaDB](https://mariadb.org/).
It can be installed on almost all devices. Create user, password and database.
Store database's secrets in `data/secrets.json`.
Use `data/secrets.json.template` as a template - remember to remove `.template` suffix.

Example `data/secrets.json`:
```json
{
    "username": "YOUR_USERNAME",
    "password": "YOUR_PASSWORD",
    "host": "localhost",
    "port": 3306,
    "database": "YOUR_DB_NAME"
}
```
Data must match `organizer_database/environment` section from `docker-compose.yaml`

### Running

To run this project locally follow steps:
1. Install requirements `pip install -r requirements.txt`
2. Run main file `python src/main.py` from project's driectory

### Docker

Running this project with docker is easy.
You need to:
1. Create database service
2. Create nicegui service
3. Unpack `Organizer` project in nicegui's volume
4. Create docker containers

#### Step 1 & 2

`docker-compose.yaml` file for step 1 and 2:
```yaml
---
version: "3.0"

services:
  organizer_database:
    container_name: organizer_database
    image: mariadb
    restart: unless-stopped
    command: --transaction-isolation=READ-COMMITTED --log-bin=binlog --binlog-format=ROW
    volumes:
      - /opt/organizer/db:/var/lib/mysql # Left is your local path used as database's volume
    environment: # Set credentials - must match data/secrets.json
      - MARIADB_ROOT_PASSWORD=YOUR_ROOT_PASSWORD
      - MARIADB_USER=YOUR_USERNAME
      - MARIADB_PASSWORD=YOUR_PASSWORD
      - MARIADB_DATABASE=YOUR_DB_NAME
    ports:
      - 3306:3306 # if 3306 port is taken, change only left value to you liking

  organizer_server:
    container_name: organizer_server
    image: zauberzeug/nicegui:latest
    restart: unless-stopped
    ports:
        - 8080:8080 # if 8080 port is taken, change only left value to you liking
    environment:
        - PUID=1000 # change this to your user id
        - PGID=1000 # change this to your group id
    volumes:
        - /opt/organizer/server:/app # Left is your local path used as nicegui's volume
```

Path `/opt/organizer` is just an example. It can be any local path you choose.

#### Step 3

Copy project from github to `/opt/organizer/server` and **unpack it**. 
To achieve this run `git clone git@github.com:WasuMrTomass0/Organizer.git ./` in `/opt/organizer/server`.

Example file tree is:
```ascii
opt/
└─ organizer/
   └─ server/
      ├─ data/
      ├─ doc/
      ├─ src/
      ├─ main.py
      └─ requirements.txt
```

### Step 4

Create docker containers with `sudo docker-compose up -d`. 
Open web page with your machine's ip and port selected in `docker-compose.yaml`.
