import queue
import threading

from src.command_handler.command_handlers import HANDLERS


class CommandBus:
    def __init__(self):
        self.command_queue = (
            queue.Queue()
        )  # storing all commands, their handlers are in HANDLERS
        # the command bus works in a sub thread
        self.worker = threading.Thread(
            target=self.handle_command, name="CommandBusWorker", daemon=True
        )
        self.worker.start()

    # add command to command bus command queue
    def raise_command(self, command):
        self.command_queue.put(command)

    # add None to command queue, which can end the worker
    def end_command_handler(self):
        self.raise_command(None)

    # handle command from the command queue
    def handle_command(self):
        while True:
            try:
                # get a command from queue, the get() function is block, if the queue is empty, this function will block the thread
                command = self.command_queue.get()
                if command is None:  # when a command is None, the thread will be ended
                    return
                for handler in HANDLERS:
                    handler(self, command)

            except Exception as e:
                print(f"Error handling command: {e}")


# instantiate a command bus as a global bus
command_bus = CommandBus()
