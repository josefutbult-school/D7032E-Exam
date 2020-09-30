from IO.HostIO import HostIO
from Networking.HostNetworking import HostNetworking
from FileParser.SettingsParser import SettingsParser
from FileParser.DictionaryParser import DictionaryParser
from Player.Player import Player


def on_client_connect(key):
    HostIO.print(f"player {key} joined", direct_continue=True)
    HostNetworking.player_write(key, f"Welcome player {key}\n")


def run_game(args):
    HostIO.print("Waiting for players", direct_continue=True, clear_screen=True)
    HostNetworking.connect_to_clients(number_of_connections=SettingsParser.get_setting('number_players'),
                                      on_connect=on_client_connect)
    HostIO.print("All players registered. Begin game.")
    HostIO.clear()
    players = [Player(i) for i in range(SettingsParser.get_setting("number_players"))]
    boogle_instance = args()
    while True:
        for player in players:
            move = player.get_move()
            HostIO.print(f"{player} wrote {move}", direct_continue=True)
            if boogle_instance.check_move(move):
                HostIO.print("Sucess", direct_continue=True)
                player.successful_move()
            else:
                HostIO.print("Fail", direct_continue=True)
                player.unsucessful_move()

        if HostIO.get_input("End") == 'y':
            break
    HostNetworking.close()
