import sys 
import socket
import threading


def do_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1' 
    port = 12345       
    client_socket.connect((host, port))

    message = input("Prompt: ")
    client_socket.send(message.encode('utf-8'))

    response = client_socket.recv(16384).decode('utf-8')
    print(response)

    client_socket.close()


def handle_client(client_socket, client_address):
    print(f"Got connection.")
    while True:
        prompt = client_socket.recv(16384).decode('utf-8')
        if not prompt:
            break  # connection closed by client
        print(f"Received prompt")
        '''
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda:0")
        input_len = len(inputs["input_ids"][0])
        outputs = model.generate(**inputs)[0]
        response = tokenizer.decode(outputs)
        '''
        response = "Hello!"
        client_socket.send(response.encode('utf-8'))
        print("Sent response")
    client_socket.close()
    print(f"Connection closed")


def do_server():
    '''
    import torch
    from transformers import BitsAndBytesConfig
    from transformers import AutoModelForCausalLM, AutoTokenizer

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    model_id = "meta-llama/Llama-2-13b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        quantization_config=quantization_config,
        device_map="auto"
    )
    '''

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
        

if __name__ == "__main__":
    # default to client
    if len(sys.argv) < 2 or sys.argv[1].lower() != "server":
        do_client()
    else:
        do_server()