#!/bin/bash
#pep8 badge/*.py
pycodestyle $(find leaderboard -name '*.py')
