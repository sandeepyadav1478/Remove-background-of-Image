from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep
import requests
import pandas as pd

df = pd.read_csv("crucials.csv")
remove_bg_api_key = str(df.iloc[0,-1])
img_loc = str(df.iloc[1,-1])
save_loc = str(df.iloc[2,-1])

class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


if __name__ == "__main__":
    with Loader("Sending request to server..."):

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(img_loc, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': remove_bg_api_key},
        )
        

    loader = Loader("Saving with object...", "That was fast!", 0.05).start()
    if response.status_code == requests.codes.ok:
        with open(save_loc, 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)
    loader.stop()