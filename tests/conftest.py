# we start by Setting up the app , client, database and necessary configurations
import pytest
import tempfile
from myapp import create_app # the factory that creates app instance in __init__.py
from myapp.db import get_db, init_db # database conection & creation funcs

# we put our sql statements inside a file data.sql
# these the app will read to create temp database for testing
import os
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8') # read the queries and store in that variable for later use

# create the mock / test app
@pytest.fixture
def app():
    # make temporary file for database
    db_fd, db_path = tempfile.mkstemp()

    # create the app
    app = create_app({
        'Testing': True, # changes internal configuration to suit testing
        'DATABASE': db_path, # points to temp file we just created
    })

    # initialize database and provide database to app 
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    # return app - this is what test funcs will use
    yield app

    # the yield will terminate after the tests have finished, then this next code to tear down runs
    os.close(db_fd)
    os.unlink(db_path)



# create test client
@pytest.fixture
def client(app): # client` fixture depends on the `app` fixture, so `app` is passed as an argument.
    return app.test_client() 

# create test CLI runner
@pytest.fixture
def runner(app):
    return app.test_cli_runner()