""" import app as application so gunicorn can
    find it.
"""
from warbadge_app.app import app as application
