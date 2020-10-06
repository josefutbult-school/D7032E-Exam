from multiprocessing import Process, Lock

from IO.HostIO import HostIO
from Networking.HostNetworking import HostNetworking
from FileParser.SettingsParser import SettingsParser
from Player.Player import Player


def player_paralell_process(player, boogle_instance, parse_lock):
    while True:
        with parse_lock:
            player.parse_move(boogle_instance.check_move(player.get_id(), player.get_move()))


def run_parallel_game(boogle_instance, players):
    parse_lock = Lock()
    processes = [Process(target=player_paralell_process, args=(player, boogle_instance, parse_lock))
                 for player in players]

    for process in processes:
        process.start()

    HostIO.get_input("Press any key to end\n")

    for process in processes:
        process.terminate()


def host_turnbased_process(boogle_instance, players):
    while True:
        for player in players:
            for other_player in players:
                if other_player is not player:
                    other_player.write_player(f'it is player {player.get_id()}\'s turn.')
            player.parse_move(boogle_instance.check_move(player.get_id(), player.get_move()))


def run_turnbased_game(boogle_instance, players):
    game_process = Process(target=host_turnbased_process, args=(boogle_instance, players))
    game_process.start()
    HostIO.get_input("Press any key to end\n")
    game_process.terminate()


def on_client_connect(key):
    HostIO.print(f"player {key} joined", direct_continue=True)
    HostNetworking.player_write(key, f"Welcome player {key}\n")


def run_game(boogle_class, paralell_run, mockup=False):
    Player.mockup = mockup
    if not mockup:
        HostIO.print("Waiting for players", direct_continue=True, clear_screen=True)
        HostNetworking.connect_to_clients(number_of_connections=SettingsParser.get_setting('number_players'),
                                          on_connect=on_client_connect)
        HostIO.print("All players registered. Begin game.")

    HostIO.clear()
    players = [Player(i) for i in range(SettingsParser.get_setting("number_players"))]
    boogle_instance = boogle_class()
    if paralell_run:
        run_parallel_game(boogle_instance=boogle_instance, players=players)
    else:
        run_turnbased_game(boogle_instance=boogle_instance, players=players)

    if not mockup:
        HostNetworking.close()
