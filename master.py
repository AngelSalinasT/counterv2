from baseNode import Node
import socket
import threading
import time

class Master(Node):
    def __init__(self):
        super().__init__(node_type= str)
        self.health_check_thread = threading.Thread(target=self.check_node_health, daemon=True)
        self.wait_for_node_connections_thread = threading.Thread(target=self.wait_for_node_connections, daemon=True)
        #Address and port of the server
        self.server_host = 'localhost' #value default
        self.server_port = 7000 #value default


    def check_node_health(self):
        """Periodically checks the health of the node."""
        while self.status == 'Active':
            try:
                self.socket.send(b'')  # Dummy send to check connection
                response = self.socket.recv(1024)  # Dummy read
                if not response:
                    raise ConnectionError("No response; node might be inactive.")
                print(f"[{self.type}] {self.address}:{self.port} is healthy.")
            except Exception as e:
                print(f"[{self.type}] Health check failed: {e}")
                self.circuit_breaker()
                break

    def circuit_breaker(self):
        """Deactivates the node and closes its socket."""
        with self.lock:
            self.status = 'Inactive'
            self.socket.close()
            print(f"[{self.type}] {self.address}:{self.port} deactivated due to inactivity.")
    
    def wait_for_node_connections(self):
        """Sets up the server to listen for incoming connections from nodes."""
        print(f"[{self.node_type}] Starting server on {self.server_host}:{self.server_port}")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.server_host, self.server_port))
        server_socket.listen(5)
        print(f"[{self.node_type}] started and listening on {self.server_host}:{self.server_port}")
        while True:
            try:
                conn, addr = server_socket.accept()

                with self.lock:
                    self.connect_nodes[addr] = {
                        'socket': conn,
                        'status': 'Active',
                        'last_seen': time.time()
                    }
                print(f"[{self.type}] New node connected from {addr}")
                self.main_server_status = 1
            
            except Exception as e:
                print(f"[{self.type}] Error accepting connections: {e}")
            except KeyboardInterrupt:
                print(f"[{self.type}] Server shutting down.")
                break
    
     #fuction to manage flow of the node
    def handle_node_master(self):
        """Handles communication with a connected node."""
        while True:
            try:
                if self.main_server_status == 0:
                    #self.connect()
                    self.main_server_status = 1
                elif self.main_server_status == 1:
                    self.send_data_thread.start()
                    self.main_server_status = 2
                elif self.main_server_status == 2:
                    self.receive_data_thread.start()
                    self.main_server_status = 3
                elif self.main_server_status == 3:
                    self.disconnect()

            except socket.timeout:
                print(f'¨[{self.type}] Tiempo de espera agotado.')
            except (socket.error, OSError) as e:
                print(f'{self.type} Error de socket: {e}')