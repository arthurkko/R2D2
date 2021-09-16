from dotenv import dotenv_values
import os

from dotenv.main import load_dotenv

config = dotenv_values()  # config = {"USER": "foo", "EMAIL": "foo@example.org"}

print(config["wolframalpha_key"])


load_dotenv()
print(os.environ.get("wolframalpha_key"))
