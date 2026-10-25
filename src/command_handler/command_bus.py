import queue
import threading

from src.command_handler.command_handlers import HANDLERS


class CommandBus:
    def __init__(self):
        self.command_queue = queue.Queue()  # storing all commands, their handlers are in HANDLERS
        self.worker = threading.Thread(target=self.handle_command,name="CommandBusWorker",daemon=True)
        self.worker.start()

    def raise_command(self, command):
        self.command_queue.put(command)

    def end_command_handler(self):
        self.raise_command(None)

    def handle_command(self):
        while True:

            try:
                command = self.command_queue.get()
                if command is None: # when a command is None, the thread will be ended
                    return
                for handler in HANDLERS:
                    handler(self, command)

            except Exception as e:
                print(f"Error handling command: {e}")

command_bus = CommandBus()