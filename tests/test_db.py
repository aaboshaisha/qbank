import pytest
import sqlite3
from myapp.db import get_db

# test if we can connect to, maintain and close connection to db
@pytest.fixture
def test_get_close_db():
    with app.app_context():
        db = get_db() # call it first time
        assert db is get_db() # call 2nd time and see if equals first

    # test if we can close it after app context has ended (Above)
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    
    assert 'closed' in str(e.value) # make sure it's closed - again

# test init_db command - without initializing database using monkey patching
def test_init_db_command(runner, monkeypatch):
    class Recorder(object): # a simple flag to use with fake command
        called = False 

    def fake_init_db(): # fake command to avoid initializing database - just turns flag ON when called
        Recorder.called = True
    
    monkeypatch.setattr('myapp.db.init_db', fake_init_db) # replace real command with fake one
    result = runner.invoke(args=['init-db']) # invoke real command -> calls fake one
    assert 'Initialized' in result.output # our print statement in original command
    assert Recorder.called
