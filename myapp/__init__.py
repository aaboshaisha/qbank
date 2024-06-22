import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # set some default configuration for app to use
    app.config.from_mapping(
        SECRTE_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'myapp.sqlite')
    )

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
        


    # render a simple page
    @app.route('/hello')
    def hello():
        return 'Hello, World'
    
    return app


