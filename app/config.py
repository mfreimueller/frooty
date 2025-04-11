import json

class Config:
    @staticmethod
    def load_config(path: str):
        with open(path, 'r') as file:
            rawConfig = json.load(file)
            
            protocol = rawConfig['protocol'] or 'tcp:'
            address = rawConfig['address'] or 'localhost'
            port = rawConfig['port'] or 5555

            return Config(protocol, address, port)

    def __init__(self, protocol: str, address: str, port: int):
        self.protocol = protocol
        self.address = address
        self.port = port