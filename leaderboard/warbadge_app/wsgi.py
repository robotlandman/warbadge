#!/usr/bin/env python
""" This is the entry point for gunicorn to launch the app"""
from warbadge_app.app import app as application

if __name__ == "__main__":
    application.run()
