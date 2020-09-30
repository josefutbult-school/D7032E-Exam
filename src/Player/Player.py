from IO.HostIO import HostIO
from Networking.HostNetworking import HostNetworking


class Player():
    def __init__(self, id):
        self.id = id
        self.points = 0

    def get_move(self):
        move = HostNetworking.player_read(self.id, "Insert word: ")
        print(move)
        return move

    def get_id(self):
        return self.id

    def successful_move(self):
        HostNetworking.player_write(self.id, "Sucess\n")
        self.points += 1

    def unsucessful_move(self):
        HostNetworking.player_write(self.id, "Fail\n")

    def __str__(self):
        return f"Player {self.id}"
