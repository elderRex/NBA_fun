import os
import csv
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['txt','csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def secure(mystr):
    str = mystr.split()
    for i in range(0, len(str)):
        if str[i] == "drop" or str[i] == "insert" or str[i] == "delete" or str[i] == "create":
            return "rejected"
    return mystr

def parse_team(team):
    if team == 'Miami Heat':
        return 'MIA'
    elif team == 'Charlotte Hornets':
        return 'CHA'
    elif team == 'Chicago Bulls':
        return 'CHI'
    elif team == 'Dallas Mavericks':
        return 'DAL'
    elif team == 'Golden State Warriors':
        return 'WAS'
    elif team == 'Houston Rockets':
        return 'HOU'
    elif team == 'Miami Heat':
        return 'MIA'
    elif team == 'Los Angeles Lakers':
        return 'LAL'
    elif team == 'Orlando Magic':
        return 'ORL'
    elif team == 'Phoenix Suns':
        return 'PHX'
    return 'error'