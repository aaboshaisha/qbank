import os
import logging

from flask import Flask, render_template
import stripe
from dotenv import load_dotenv

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    logging.basicConfig(level=logging.DEBUG)

    # load env variables from .env file
    load_dotenv()
    # set some default configuration for app to use
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'myapp.sqlite'),
        STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY'),
        STRIPE_SECRET_KEY=os.getenv('STRIPE_SECRET_KEY'),
        STRIPE_WEBHOOK_SECRET=os.getenv('STRIPE_WEBHOOK_SECRET')
    )

    # Set Stripe API key
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    # if a configuration file exists in instance folder, override default configuration
    if test_config is None:
        # load from instance folder 
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load from file passed
        app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import questions
    app.register_blueprint(questions.bp)

    from . import webhook
    app.register_blueprint(webhook.bp)

    # render a simple page
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app


