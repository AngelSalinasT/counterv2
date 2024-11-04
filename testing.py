from assistant import Assistant
from worker import Worker
import threading

if __name__ == "__main__":
    worker = Worker()
    assistant = Assistant()
    assistant.node_type = 'Assistant' 
    worker.node_type = 'Worker'
    worker.server_port = 7000

    worker.handle_node_worker()
    assistant.handle_node_assistant() 

    print("Done")