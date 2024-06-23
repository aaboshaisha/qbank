import sqlite3

import click # module for creating command line interfaces
from flask import current_app, g # g is a special obj that works like namespace 

def get_db(): # connect to the database and return a database connection object.
    if 'db' not in g:
        # if db not already stored in g, connect to it and store the connection in g 
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # tells connection to return rows that behave like dicts
        # so we can access columns by name
        return g.db

# function to execute the commands in schema.sql a.k.a initialize the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# define a command-line command to call init_db and show success msg to user

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database')

def close_db(e=None):
    db = g.pop('db', None) # retrieve db connection it if exists, else None
    if db is not None: # if u find a connection, close it
        db.close()