import json

class User:
    def __init__(self, name, pub_key, priv_key) -> None:
        self.name  = name
        self.address = pub_key
        self.pub_key = pub_key
        self.priv_key = priv_key


    @staticmethod
    def from_folder(folder_path):
        with open(f'{folder_path}/metadata.json') as f:
            data = json.load(f)

        return User(
             name=data["name"], 
             pub_key=data["public_key"], 
             priv_key=data["priv_key"]
        )
