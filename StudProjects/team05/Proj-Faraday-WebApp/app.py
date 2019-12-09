import threading
import time

from flask import Flask
from flask_cache import Cache

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

time.sleep(2.0)

cache = Cache(app,config={'CACHE_TYPE': 'simple'})


def main():
    cache.init_app(app)

    with app.app_context():
        cache.clear()


if __name__ == '__main__':
    app.run(debug=True)
