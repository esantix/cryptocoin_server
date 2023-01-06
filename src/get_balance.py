import requests
import json

# Create blockchain
NODE_ADDR = "http://localhost:5000"


print(json.loads(requests.get(f'{NODE_ADDR}/balance').content))

