import os
import csv
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response,url_for
import security_check as sc

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config['UPLOAD_FOLDER'] = sc.UPLOAD_FOLDER

DATABASEURI = "postgresql://yg2466:Asdfgh12345!@w4111vm.eastus.cloudapp.azure.com/w4111"
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

@app.route('/DBA_add',methods=['POST'])
def my_dba_add():
    return redirect(url_for('.index'))

@app.route('/perf_vis',methods=['POST'])
def myperf_vis():
    return render_template('perf_vis.html')

@app.route('/perf_vis/query_in',methods=['POST'])
def perf_vis_query():
    team = request.form.get('team')
    player = request.form.get('player')
    location = request.form.get('location')
    print team + " " + player + " " + location
    team = sc.parse_team(team)

    if team == 'error':
        print "Error: Team Not Found"
        return render_template(url_for('.index'))

    query_string = "SELECT E.ssn As pssn, E.name AS pname, P.age, E.salary, T.tid " \
                   "FROM Pay_Born_Emp As E JOIN Player As P Using(ssn), from_Team As T, Performance PE " \
                   "WHERE PE.ssn = P.ssn and E.tid = T.tid and T.tid = '" + team + "';"
    cursor = g.conn.execute(query_string)
    results = []
    for result in cursor:
        results.append(result['pname'])  # can also be accessed using result[0]
    cursor.close()
    print results
    return render_template('perf_vis.html',t_player_data = results)

@app.route('/tquery', methods=['GET', 'POST'])
def my_query():
    error = None
    if request.method == 'POST':
        mytable =  request.form['table']
        print mytable
        cursor = g.conn.execute("SELECT * FROM " + mytable)
        names = []
        for result in cursor:
            names.append(result['name'])  # can also be accessed using result[0]
        cursor.close()
        print names

    return render_template('vis_main.html', my_data=names)

@app.route("/vis_main.html")
def vis_main_foo():
    return render_template('vis_main.html')

@app.route("/")
def index():
    # DEBUG: this is debugging code to see what request looks like
    print request.args

    #
    # example of a database query
    #
    '''
    cursor = g.conn.execute("SELECT tid FROM from_Team")
    names = []
    for result in cursor:
        names.append(result['tid'])  # can also be accessed using result[0]
    cursor.close()

    print names
    '''
    return render_template('index.html')

if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=5000, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using:

            python server.py

        Show the help text using:

            python server.py --help

        """

        HOST, PORT = host, port
        print "running on %s:%d" % (HOST, PORT)
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()