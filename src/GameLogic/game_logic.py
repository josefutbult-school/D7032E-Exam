from multiprocessing import Process, Lock, Manager
from multiprocessing.managers import BaseManager

from IO.HostIO import HostIO
from IO.PlayerIO import PlayerIO
from Networking.HostNetworking import HostNetworking
from FileParser.SettingsParser import SettingsParser
from Player.Player import Player


def player_parallel_process(player, boogle_instance, parse_lock):
    player_id = player.get_id()
    while True:
        PlayerIO.write_player_gameboard(player_id,
                                        boogle_instance.get_board_string(player_id),
                                        boogle_instance.get_game_info(player_id))
        move = PlayerIO.get_move(player_id)
        PlayerIO.clear_player(player_id)
        with parse_lock:
            player.parse_move(boogle_instance.check_move(player_id, move), boogle_instance.get_points(move))


def on_client_connect(key):
    HostIO.print(f"player {key} joined", direct_continue=True)
    HostNetworking.player_write(key, f"Welcome player {key}\n")


def run_game(boogle_class, generous_boggle, mockup=False):
    PlayerIO.mockup = mockup
    if not mockup:
        HostIO.print(f"The game is {boogle_class.get_name()}!\nWaiting for players", direct_continue=True, clear_screen=True)
        HostNetworking.connect_to_clients(number_of_connections=SettingsParser.get_setting('number_players'),
                                          on_connect=on_client_connect)
        HostIO.print("All players registered. Begin game.")

    HostIO.clear()

    BaseManager.register('boogle_class', boogle_class)
    BaseManager.register('Player', Player)
    manager = BaseManager()
    manager.start()
    boogle_instance = manager.boogle_class(number_of_boards=SettingsParser.get_setting('number_players'),
                                           board_size=SettingsParser.get_setting('board_size'))
    players = [manager.Player(i) for i in range(int(SettingsParser.get_setting("number_players")))]
    parse_lock = Lock()

    processes = [Process(target=player_parallel_process, args=(player, boogle_instance, parse_lock))
                 for player in players]

    for process in processes:
        process.start()

    HostIO.get_input("Press any key to end\n")

    for player in players:
        PlayerIO.write_player(player.get_id(), f"\nFinal score is {player.get_points()}")

    for process in processes:
        process.terminate()

    if not mockup:
        HostNetworking.close()
