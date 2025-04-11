from .config import Config
from .service import predict_meals
from sklearn.preprocessing import LabelEncoder
import sys
import zmq
from zmq.asyncio import Context

config_path = "config.json"
if len(sys.argv) > 1:
    config_path = sys.argv[1]

config = Config.load_config(config_path)

ctx = Context.instance()

socket = ctx.socket(zmq.REP)
socket.bind(f"{config.protocol}://{config.interface}:{config.port}")

# TODO: create MariaDB connector to pass to predict_meals
connector = None

label_encoder = LabelEncoder()

# TODO: something to consider -> async worker to allow for concurrent requests???
while True:
    request = socket.recv_json()
    print("received message from socket:", request)

    assert(connector)
    assert(request['group_id']) # we should never receive a malformed message

    # as this service is not public facing, we can assume that the group_id
    # is valid and the invoking user has the permission to interact with the
    # group identified by this id.
    group_id = request['group_id']
    meals = predict_meals(connector, label_encoder, group_id)

    response = {
        "meals": meals
    }

    socket.send_json(response)
