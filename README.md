Just an easy script so I can run inference from my couch on my other laptop.

## VLLM Versions

For the VLLM versions, do something like this:
```
openai = None
if not remote_inference:
    import openai as openai
else:
    import client_vllm
    openai = client_vllm.Mock_openai(ip) # where ip is the local IP addr of your inference host
```

My goal is to abstract out the OpenAI API so I can use Langchain from my couch, so may need to add compatibility with more openai.ChatCompletion.create arguments (and maybe other openai.ChatCompletion and openai stuff) as I go.
