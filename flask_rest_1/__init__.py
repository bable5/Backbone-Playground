from flask import Flask
app = Flask(__name__)

import flask_rest_1.views.tasks
import flask_rest_1.views.todos

