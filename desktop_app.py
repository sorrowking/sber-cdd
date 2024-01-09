import os
import sys
import time
from threading import Thread
import webview


def start_webview():
    window = webview.create_window('СБЕР кафе', 'http://localhost:8000/', fullscreen=True)
    webview.start()
    window.closed = os._exit(0)


def start_django():
    if sys.platform in ['win32', 'win64']:
        os.system("python manage.py runserver {}:{}".format('127.0.0.1', '8000'))
        # time.sleep(10)
    else:
        os.system("python3 manage.py runserver {}:{}".format('127.0.0.1', '8000'))
        # time.sleep(10)


if __name__ == '__main__':
    Thread(target=start_django).start()
    #start_webview()