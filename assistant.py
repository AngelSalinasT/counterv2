from baseNode import Node

class Assistant(Node):
    def __init__(self):
        super().__init__(node_type= str)

    #fuction to manage flow of the node
    def handle_node_assistant(self):
        """Handles communication with a connected node."""
        while True:
            try:
                if self.main_server_status == 0: #in 0 state the node is trying to connect
                    self.connect()
                elif self.main_server_status == 1: #in 1 state the node is receiving data
                    self.send_data_thread.start()
                    self.wait_for_response()                    
                elif self.main_server_status == 2:#in 3 state the node is disconnecting
                    self.disconnect()
            except self.socket.timeout:
                print(f'¨[{self.type}] Tiempo de espera agotado.')
            except (self.socket.error, OSError) as e:
                print(f'{self.type} Error de socket: {e}')