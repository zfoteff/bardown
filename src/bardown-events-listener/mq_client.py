import pika


class RMQClient:
    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", port="5672")
        )
