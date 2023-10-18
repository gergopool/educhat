from flask import Flask

app = Flask(__name__)
app.secret_key = 'very_secret_key'

import educhat.routes