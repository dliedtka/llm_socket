import os
import socket 
import threading
import json
import openai 
from transformers import AutoTokenizer
from pprint import pprint

MODEL_ID = "meta-llama/Llama-2-7b-chat-hf"

openai.api_key = ""
openai.api_base = "http://localhost:42196/v1"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)


def chat_get_num_tokens(messages):
    # seems like I end up one off, but that's ok...
    text = ""
    
    # assume first message system prompt
    text += "<s>[INST] <<SYS>>\n"
    assert(messages[0]["role"] == "system")
    text += messages[0]["content"]
    text += "\n<</SYS>>\n\n"

    # convo history
    counter = 1
    while counter + 2 < len(messages):
        assert(messages[counter]["role"] == "user")
        text += messages[counter]["content"]
        text += " [/INST] "
        assert(messages[counter+1]["role"] == "assistant")
        text += messages[counter+1]["content"]
        text += " </s><s>[INST] "
        counter += 2

    # new instruction
    text += messages[counter]["content"]
    text += " [/INST]"

    return len(tokenizer.encode(text))


def handle_client(client_socket, client_address):
    print(f"Got connection.")
    messages_json = client_socket.recv(4096 * 8).decode('utf-8') # should be a bigger buffer than we'd ever need (4096 token max context window, assume < 8 chars per token)
    print(f"Received prompt.")
    messages = json.loads(messages_json)
    
    # actual API call
    chat_completion = openai.ChatCompletion.create(
        model = MODEL_ID,
        max_tokens=(4096 - chat_get_num_tokens(messages)),
        messages=messages
    )

    response_json = json.dumps(chat_completion)
    
    client_socket.send(response_json.encode('utf-8'))
    print("Sent response.")
    client_socket.close()
    print(f"Connection closed")


if __name__ == "__main__":
    # parent to run VLLM
    if os.fork() != 0:
        os.system(f"python3 -m vllm.entrypoints.openai.api_server --model {MODEL_ID} --port 42196")
    # child to listen for connections
    else:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '0.0.0.0' 
        port = 12345      
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Ready for connections...")
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

