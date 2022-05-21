import os
from server import app
from server.errors import start_debug
# from recognition.net.makens import load_net


os.chdir(os.path.dirname(os.path.abspath(__file__)))
if __name__ == '__main__':
    start_debug()
    # load_net()
    app.run(host='0.0.0.0', port=8080)
