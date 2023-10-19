"""
This is a demo player that does nothing. It is used as a template for new players.
"""
import os.path

from dotenv import load_dotenv

from walterplayers.base_player import BasePlayer
from walterplayers.constants import Action


class MyPlayer(BasePlayer):
    """ This is a demo player that does nothing. It is used as a template for
    new players. """

    def choose_action(self, find_response):
        return Action.STOP, None


def get_args():
    """ Get arguments from command line """
    import argparse

    parser = argparse.ArgumentParser(description='Demo player')
    parser.add_argument(
        '--env-file',
        type=str,
        default='.env',
        help='Env file to load environment variables from'
    )

    return parser.parse_args()


def main():
    """ Main function """
    args = get_args()

    # check if .env file exists
    if not os.path.exists(args.env_file):
        raise Exception(f"Environment file {args.env_file} does not exist")

    print(f"Loading {args.env_file}")
    load_dotenv(args.env_file)

    player = MyPlayer()
    player.run()


if __name__ == "__main__":
    main()
