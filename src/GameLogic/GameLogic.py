from multiprocessing import Process, Lock
from multiprocessing.managers import BaseManager
from time import sleep

from IO.HostIO import HostIO
from IO.PlayerIO import PlayerIO
from Networking.HostNetworking import HostNetworking
from FileParser.SettingsParser import SettingsParser
from Player.Player import Player


class GameLogic:
    @staticmethod
    def player_parallel_process(player, boogle_instance, parse_lock, generous_boggle, board_size, moves=None):
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
                if moves is None:
                    move = PlayerIO.get_move(player_id)
                elif not len(moves[player_id]):
                    # If the game is mocked up, we only wants player one to go through the defined
                    # moves and then all players should be inactive until game termination
                    return
                else:
                    if player_id:
                        sleep(0.1 * player_id)
                    move = moves[player_id].pop(0)

                PlayerIO.clear_player(player_id)
                with parse_lock:
                    PlayerIO.write_player(player_id, player.parse_move(boogle_instance.check_move(player_id,
                                                                                                  move,
                                                                                                  generous_boggle),
                                                                       boogle_instance.get_points(move)))
        except KeyboardInterrupt:
            return

    @staticmethod
    def on_client_connect(key):
        HostIO.print(f"player {key} joined", direct_continue=True)
        HostNetworking.player_write(key, f"Welcome player {key}\n")

    @staticmethod
    def generate_game(boogle_class, moves=None, predefined_boggle_instance=None):
        if predefined_boggle_instance is None:
            BaseManager.register('boogle_class', boogle_class)
        else:
            BaseManager.register('boogle_class', type(predefined_boggle_instance))
        BaseManager.register('Player', Player)
        base_manager = BaseManager()
        base_manager.start()
        if predefined_boggle_instance is None:
            boggle_instance = base_manager.boogle_class(
                number_of_boards=int(SettingsParser.get_setting('number_players')),
                board_size=int(SettingsParser.get_setting('board_size')))
        else:
            boggle_instance = predefined_boggle_instance

        players = [base_manager.Player(i) for i in range(int(SettingsParser.get_setting("number_players")))]
        parse_lock = Lock()

        processes = [Process(target=GameLogic.player_parallel_process,
                             args=(player,
                                   boggle_instance,
                                   parse_lock,
                                   SettingsParser.get_setting('generous_boggle'),
                                   boggle_instance.get_board_size(),
                                   moves))
                     for player in players]
        processes.append(Process(target=boggle_instance.game_paralell_process))

        for process in processes:
            process.start()

        return boggle_instance, base_manager, players, processes

    @staticmethod
    def terminate_game(boggle_instance, base_manager, players, processes, mockup):
        result = '\n'
        winner = players[0]
        for player in players:
            result += f"Final score for player {player.get_id()} is {player.get_points()}\n"
            if player.get_points() > winner.get_points():
                winner = player
        winner_id = winner.get_id()
        winner_points = winner.get_points()
        result += f"The winner is player {winner_id}\n{boggle_instance.get_game_end_info()}\n"

        for player in players:
            PlayerIO.write_player(player.get_id(), result)

        for process in processes:
            process.terminate()

        base_manager.shutdown()

        if not mockup:
            HostNetworking.close()

        return winner_id, winner_points

    @staticmethod
    def run_game(boggle_class, mockup=False, moves=None, predefined_boggle_instance=None):
        if SettingsParser.get_setting('number_players') < 2:
            if not mockup:
                HostIO.print("To few player for a game. The minimal number of players are 2.", clear_screen=True)
                HostIO.get_input("Press any key to end\n")
            return -1

        PlayerIO.mockup = mockup
        if not mockup:
            HostIO.print(f"The game is {boggle_class.get_name()}!\nWaiting for players", direct_continue=True,
                         clear_screen=True)
            HostNetworking.connect_to_clients(number_of_connections=SettingsParser.get_setting('number_players'),
                                              on_connect=GameLogic.on_client_connect)
            HostIO.print("All players registered. Begin game.")

        HostIO.clear()

        boggle_instance, \
        base_manager, \
        players, \
        processes = GameLogic.generate_game(boggle_class, moves, predefined_boggle_instance)

        try:
            for i in range(SettingsParser.get_setting('game_time'), 0, -1):
                HostIO.print(f'Time left: {i}', clear_screen=True, direct_continue=True)
                sleep(1)
        except KeyboardInterrupt:
            HostIO.print("\nTerminated")

        return GameLogic.terminate_game(boggle_instance, base_manager, players, processes, mockup)
