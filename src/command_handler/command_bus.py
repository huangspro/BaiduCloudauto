from src.command_handler.command_handlers import HANDLERS


class CommandBus:
    def __init__(self):
        self.command_list = []
        self.running = False

    def raise_command(self, command):
        self.command_list.append(command)
        if not self.running:
            self.handle_command()

    def handle_command(self):
        while len(self.command_list) > 0:
            self.running = True
            for command in self.command_list:
                for handler in HANDLERS:
                    if handler(self, command):
                        print("handled command", command.name)

        self.running = False

    def remove_command(self, command):
        self.command_list.remove(command)