""" Default settings. These can be overriden with the
    WARBADGE_CONFIG env var"""
from warbadge_app.app import app

# Change these:
app.config['MYSQL_DATABASE_USER'] = 'someuser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'somepass'
app.config['MYSQL_DATABASE_DB'] = 'dev_warbadge'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
