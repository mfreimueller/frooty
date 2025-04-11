import json

class Config:
    @staticmethod
    def load_config(path: str):
        with open(path, 'r') as file:
            rawConfig = json.load(file)

            protocol = rawConfig['protocol'] or 'tcp:'
            interface = rawConfig['interface'] or 'localhost'
            port = rawConfig['port'] or 5555

            return Config(protocol, interface, port)

    def __init__(self, protocol: str, interface: str, port: int):
        self.protocol = protocol
        self.interface = interface
        self.port = port