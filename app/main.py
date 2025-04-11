# TODO:
# - initialize ZeroMQ
# - listen for incoming messages
# - on message:
#   - build model (iff not up to date) using data from db
#   - make prediction
#   - return prediction

from .config import Config
import sys
import zmq
from zmq.asyncio import Context

config_path = "config.json"
if len(sys.argv) > 1:
    config_path = sys.argv[1]

config = Config.load_config(config_path)

ctx = Context.instance()

socket = ctx.socket(zmq.REP)
socket.bind(f"{config.protocol}://{config.address}:{config.port}")

while True:
    request = socket.recv_json()
    print("received message from socket:", request)

    # we assume that request has the following structure:
    # { "group_id": <group_id> }

    # TODO: invoke ml algorithm using request.group_id

    response = {
        "meals": []
    }

    socket.send_json(response)
