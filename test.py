import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response


app = Flask(__name__)


DATABASEURI = "postgresql://nickd:Asdfgh12345!@w4111vm.eastus.cloudapp.azure.com/w4111"
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
    print "great connection"
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

'''
@app.route('/tquery', methods=['GET', 'POST'])
def tquery():
    error = None
    if request.method == 'POST':
        mytable =  request.form['table']
        cursor = g.conn.execute("SELECT * FROM " + mytable)
        names = []
        for result in cursor:
            names.append(result['name'])  # can also be accessed using result[0]
        cursor.close()
        print names

    return render_template('index.html', my_data=names)
'''
@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()