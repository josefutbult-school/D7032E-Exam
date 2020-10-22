from multiprocessing import Process, Lock, Manager
from multiprocessing.managers import BaseManager
from time import sleep

from IO.HostIO import HostIO
from IO.PlayerIO import PlayerIO
from Networking.HostNetworking import HostNetworking
from FileParser.SettingsParser import SettingsParser
from Player.Player import Player


def player_parallel_process(player, boogle_instance, parse_lock, generous_boggle, board_size):
    try:
        player_id = player.get_id()
        # TODO: There seems to be some problem with the initialization of the
        #  boogle_instance before the thread starts.
        #  This should work for now
        sleep(.1)
        while True:
            with parse_lock:
                board = None
                try:
                    board = boogle_instance.get_board_string(board_id=player_id)
                except:
                    pass

                PlayerIO.write_player_gameboard(player_id,
                                                board,
                                                boogle_instance.get_game_info(player_id),
                                                board_size)
            move = PlayerIO.get_move(player_id)
            PlayerIO.clear_player(player_id)
            with parse_lock:
                player.parse_move(boogle_instance.check_move(player_id, move, generous_boggle),
                                  boogle_instance.get_points(move))
    except KeyboardInterrupt:
        return


def on_client_connect(key):
    HostIO.print(f"player {key} joined", direct_continue=True)
    HostNetworking.player_write(key, f"Welcome player {key}\n")


def generate_game(boogle_class):
    BaseManager.register('boogle_class', boogle_class)
    BaseManager.register('Player', Player)
    manager = BaseManager()
    manager.start()
    boogle_instance = manager.boogle_class(number_of_boards=int(SettingsParser.get_setting('number_players')),
                                           board_size=int(SettingsParser.get_setting('board_size')))
    players = [manager.Player(i) for i in range(int(SettingsParser.get_setting("number_players")))]
    parse_lock = Lock()

    processes = [Process(target=player_parallel_process,
                         args=(player,
                               boogle_instance,
                               parse_lock,
                               SettingsParser.get_setting('generous_boggle'),
                               boogle_instance.get_board_size()))
                 for player in players]

    for process in processes:
        process.start()

    return manager, players, processes


def terminate_game(manager, players, processes, mockup):
    result = '\n'
    winner = players[0]
    for player in players:
        result += f"Final score for player {player.get_id()} is {player.get_points()}\n"
        if player.get_points() > winner.get_points():
            winner = player
    winner_id = winner.get_id()
    result += f"The winner is player {winner_id}\n"

    for player in players:
        PlayerIO.write_player(player.get_id(), result)

    for process in processes:
        process.terminate()

    manager.shutdown()

    if not mockup:
        HostNetworking.close()

    return winner_id


def run_game(boogle_class, mockup=False):
    if SettingsParser.get_setting('number_players') < 2:
        HostIO.print("To few player for a game. The minimal number of players are 2.", clear_screen=True)
        HostIO.get_input("Press any key to end\n")
        return -1

    PlayerIO.mockup = mockup
    if not mockup:
        HostIO.print(f"The game is {boogle_class.get_name()}!\nWaiting for players", direct_continue=True,
                     clear_screen=True)
        HostNetworking.connect_to_clients(number_of_connections=SettingsParser.get_setting('number_players'),
                                          on_connect=on_client_connect)
        HostIO.print("All players registered. Begin game.")

    HostIO.clear()
    manager, players, processes = generate_game(boogle_class)

    try:
        for i in range(SettingsParser.get_setting('game_time'), 0, -1):
            HostIO.print(f'Time left: {i}', clear_screen=True, direct_continue=True)
            sleep(1)
    except KeyboardInterrupt:
        HostIO.print("\nTerminated")

    return terminate_game(manager, players, processes, mockup)
