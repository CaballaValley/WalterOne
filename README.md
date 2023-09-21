# WalterOne
API rest server for battle royal IA tournament


# Deploy

## With docker
'''
docker-compose build && docker-compose up
'''

## Locally
'''
./deploy/local/startup_local.sh
'''

# System initialization:
## Create django user

## Locally

Install virtual environment and requirements:
```commandline
python -m venv .env
source .env/bin/activate
python -m pip install -r config/dependencies/requirements.txt
```

In order to create django superuser, execute command:
```commandline
python manage.py createsuperuser
```
An step by step inputs are required, follow it!

### with docker
Using docker you need to access web container
```commandline
docker-compose exec web bash
```
Then, just follow `Locally` guide setup on previous point.

## Connect to server via web:

* REST API doc endpoint: [http://127.0.0.1:8000](http://127.0.0.1:8000)

# Web vies:

* Matches view: if you want to open [match 2 view](http://127.0.0.1:8000/web/2/zones/)

# Execute tests:
Start up your project using docker. Then you can run tests inside `walterone-web-1` container: 
```commandline
docker exec -u 0 -it walterone-web-1 python manage.py test
```

# Voice commands installation and usage

You need to install `python3.9` from [death snakes ppa](https://askubuntu.com/questions/1413421/how-to-install-older-version-of-python-in-ubuntu-22-04). 

You need install following packages:
```commandline
sudo apt install python3.9 python3.9-dev python3.9-venv python3.9-distutils
```

Then, you need install psycopg2 and driver dependencies:
```commandline
sudo apt install libpq-dev psycopg2
```

There are are some dependencies that need to be installed manually:
```commandline
sudo apt install libasound-dev portaudio19-dev libportaudio2 ffmpeg
```

Now, time to create virtualenv and install python dependencies
```commandline
virtualenv -p python3.9 .env
source .env/bin/activate

python -m pip install -r config/dependencies/voice_commands_requirements.txt
```


# Players setup

Since we have a module to manage players, we need to install `walterplayers` module:
```commandline
cd src/python/players_module
python -m pip install -e .
```
