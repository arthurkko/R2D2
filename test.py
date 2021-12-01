import os
from dotenv import load_dotenv

load_dotenv()
id = os.environ.get("wolframalpha_key")
def printar():
    print(id)