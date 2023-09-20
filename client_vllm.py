import os
import socket 
import json
from pprint import pprint


class Mock_ChatCompletion:
    def __init__(self, ip: str, port: int = 12345, debug: bool = False):
        self._ip = ip 
        self._port = port
        self._debug = debug

    # may need to take other args to be compatible with langchain...
    # use kwargs?
    def create(self, model: str = None, max_tokens: int = None, messages: list = None):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self._ip, self._port))

        messages_json = json.dumps(messages)
        client_socket.send(messages_json.encode('utf-8'))
        if self._debug:
            print("Sent prompt.")

        response_json = client_socket.recv(4096 * 8).decode('utf-8')
        chat_completion = json.loads(response_json)
        if self._debug:
            print("RESPONSE:")
            pprint(chat_completion)

        client_socket.close()

        return chat_completion


class Mock_openai:
    def __init__(self, ip: str, port: int = 12345, debug: bool = False):
        self.ChatCompletion = Mock_ChatCompletion(ip, port, debug)


if __name__ == "__main__":
    openai = Mock_openai("127.0.0.1")
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's your favorite color?"},
    ]
    response = openai.ChatCompletion.create(None, None, messages=messages)
    pprint(response)
