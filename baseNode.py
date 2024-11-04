import socket
import threading
import time

class Node:
    def __init__(self, node_type: str):
        #Address and port of the node to connect to server
        self.address = 'localhost' #value default
        self.port = 7000
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #data of the node itself
        self.status = 'Active'  # State of node ('Active', 'Inactive', etc.)
        self.lock = threading.Lock()
        self.node_type = node_type
        #Threads for the node
        self.receive_data_thread = threading.Thread(target=self.receive_data, daemon=True)
        self.send_data_thread = threading.Thread(target=self.send_data, daemon=True)
        #More data of the node
        self.main_server_status = 0
        self.range_text = []
        self.text = ""
        
       
    #fuction to connect to the server
    def connect(self):
        """Connects to the specified address and port."""
        try:
            print(f"[{self.node_type}] Connecting to {self.address}:{self.port}")
            self.socket.connect((self.address, self.port))
            print(f"[{self.node_type}] Connected to {self.address}:{self.port}")
            self.main_server_status = 1
        except socket.error as e:
            print(f"[{self.node_type}] Connection error: {e}")
            self.status = 'Inactive'

    def send_data(self, data):
        """Sends data to the connected node."""
        try:
            self.socket.send(data.encode())
            print(f"[{self.node_type}] Sent data: {data}")
            main_server_status = 2
        except Exception as e:
            print(f"[{self.node_type}] Error sending data: {e}")
            self.status = 'Inactive'

    #fuction to receive data from the server
    def receive_data(self):
        """Receives data from the connected node."""
        while self.status == 'Active':
            try:
                data = self.socket.recv(1024)
                time.sleep(3)
                if data:
                    print(f"[{self.node_type}] Data received: {data.decode()}")
                    main_server_status = 2
                else:
                    raise ConnectionError("No data received; possible disconnection.")
            except Exception as e:
                print(f"[{self.node_type}] Error receiving data: {e}")
                self.status = 'Inactive'
                break  # Exit receiving loop if inactive

    #fuction to wait for the server to response
    def wait_for_response(self):
        print(f'[{self.node_type}] ServerNode esperando respuesta...')
        time.sleep(10)  # Considera alternativas a sleep para mejorar la reactividad

    #function to disconnect from the server
    def disconnect(self):
        global MAIN_SERVER_STATUS
        with self.lock:
            MAIN_SERVER_STATUS = 0
        self.socket.close()
