from master import Master
import socket
import threading

class Worker(Master):
    def __init__(self):
        super().__init__()

        #fuction to manage flow of the node
    def handle_node_worker(self):
        """Handles communication with a connected node."""
        while True:
            try:
                if self.main_server_status == 0:
                    self.wait_for_node_connections_thread.start()
                    input("Press enter to continue")
                elif self.main_server_status == 1:
                    self.receive_data_thread.start()
                elif self.main_server_status == 2:
                    self.disconnect()

            except TimeoutError as e:
                print(f'¨[{self.node_type}] Tiempo de espera agotado.')
            except OSError as e:
                print(f'{self.node_type} Error de: {e}')