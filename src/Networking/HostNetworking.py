import socket
from IO.HostIO import HostIO
from Networking.adress import IP, PORT


# This class is in charge of the network communication to clients. Note that as all network related activity is
# taken care of here, it lets the programmer easily swap this class out for another means of communication.
class HostNetworking:
    connections = []
    server_socket = None

    @staticmethod
    def open_socket():
        HostNetworking.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HostNetworking.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        HostNetworking.server_socket.bind((IP, PORT))
        HostNetworking.server_socket.listen(1)

    @staticmethod
    def connect_to_clients(number_of_connections, on_connect, args=None):
        try:
            HostNetworking.open_socket()

            while len(HostNetworking.connections) < number_of_connections:
                connection, _ = HostNetworking.server_socket.accept()
                HostNetworking.connections.append(connection)
                if args is not None:
                    on_connect(len(HostNetworking.connections) - 1, args)
                else:
                    on_connect(len(HostNetworking.connections) - 1)

        except PermissionError:
            HostIO.print("Unable to bind to socket. Permission denied. Try running as sudo")
            exit(6)

    @staticmethod
    def close():
        for connection in HostNetworking.connections:
            connection.close()

        HostNetworking.connections = []

        # noinspection PyStatementEffect
        HostNetworking.server_socket.close

    @staticmethod
    def player_write(key, message):
        HostNetworking.connections[key].send(message.encode('ascii'))

    def player_read(key, message=None):
        if not message is None:
            HostNetworking.player_write(key, message)

        return HostNetworking.connections[key].recv(1024).decode().rstrip()
