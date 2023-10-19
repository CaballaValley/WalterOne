# Players setup

## .env file
We have added a `.env_example` file to the root of the project. You need to copy it and rename it to `.env`. 
Then, you need to fill the variables with the correct values.

```commandline
cp .env_example .env
```
Then you need to fill the variables with the correct values.

This file is going to be used in the next steps.

## Skeleton test
You have an example of what a player should look like in `players_module/tests/test_players.py`.

If you configured the environment variables in the `.env` file correctly, you can run the tests with the following command:

```commandline
python players_module/walterplayers/skeleton.py
```
You must see the following output:

```commandline
python  walterplayers/skeleton_player.py --env .env                                                                     130 ↵ soto@renata
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
If you are using a virtual environment, you must activate it before running the tests.
```
