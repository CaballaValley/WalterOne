# WalterOne
API rest server for battle royal IA tournament


# Deploy

## With docker
Copy the dev env config to the docker-compose path. 
```
cp config/.env.dev ./.env
```
Now you can update config editing `.env` file, for example change `$APP_PORT` if this port is beeing used in your host.


Time to build and run:
```
docker-compose build && docker-compose up
```

## Locally
```
./deploy/local/startup_local.sh
```
