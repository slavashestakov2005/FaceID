import os
from server import app
from server.errors import start_debug
# from recognition.net.makens import load_net
from telegram.bot import run_bot


os.chdir(os.path.dirname(os.path.abspath(__file__)))
if __name__ == '__main__':
    start_debug()
    # load_net()
    run_bot()
    app.run(host='0.0.0.0', port=8080)
