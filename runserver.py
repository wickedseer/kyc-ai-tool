"""
This script runs the kycweb application using a development server.
"""

from os import environ
from kycweb import app
import webbrowser
from threading import Timer

def open_browser(host, port):
      webbrowser.open_new("http://" + host + ":" + str(port))

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')

    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    Timer(1, open_browser(HOST, PORT)).start()
    app.run(HOST, PORT)
