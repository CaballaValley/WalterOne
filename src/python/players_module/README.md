# Players setup
Follow the next steps to use the Skeleton player as a template for your player.

## Clone the repository

```commandline
git clone https://github.com/CaballaValley/WalterOne.git 
```

## Install dependencies
```commandline
cd WalterOne/src/python/players_module
python -m pip install -e .
```

## .env file
We have added a `.env_example` file to the root of the project. You need to copy it and rename it to `.env`.

```commandline
cp .env_example .env
```
Then you need to fill the variables with the correct values:
```commandline
WALTERONE_HOST=192.168.1.83:8000
WALTERONE_MATCH=2

WALTERONE_USERNAME<<<YourUsername>>>>
WALTERONE_PASSWORD=<<<YourPassword>>>
```

This file is going to be used in the next steps.

## Skeleton test
You have an example of what a player should look like in `players_module/walterplayers/skeleton_player.py`.

If you configured the environment variables in the `.env` file correctly, you can run the tests with the following command:

```commandline
python walterplayers/skeleton_player.py --env .env
```
You must see the following output:

```commandline
> python  walterplayers/skeleton_player.py --env .env

Loading .env
2023-10-19 13:48:07.768557 - Executing Action: Action.STOP with arguments: None
2023-10-19 13:48:07.768596 - Executed Action: Action.STOP, Error: False, Response: None
2023-10-19 13:48:08.006258 - Executing Action: Action.STOP with arguments: None
2023-10-19 13:48:08.006284 - Executed Action: Action.STOP, Error: False, Response: None
2023-10-19 13:48:08.241134 - Executing Action: Action.STOP with arguments: None
2023-10-19 13:48:08.241181 - Executed Action: Action.STOP, Error: False, Response: None
2023-10-19 13:48:08.493913 - Executing Action: Action.STOP with arguments: None
2023-10-19 13:48:08.493991 - Executed Action: Action.STOP, Error: False, Response: None
2023-10-19 13:48:08.737436 - Executing Action: Action.STOP with arguments: None
2023-10-19 13:48:08.737531 - Executed Action: Action.STOP, Error: False, Response: None
```

## ¡¡¡ IMPORTANT !!!
```
If your output is not the same as the one shown above, you must review the configuration of the `.env` file.
```
