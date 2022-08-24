"""
This script initializes the application instance, which handles all web server
requests. It also initializes a cache instance used for data that is processed
once upon the app's startup. 
"""

from flask import Flask
from flask_caching import Cache
from flask_bootstrap import Bootstrap

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F2%J$LZGH*Uh'
app.config.from_mapping(config)
cache = Cache(app, config)
bootstrap = Bootstrap(app)

from jarbegone import routes
