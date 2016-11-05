import os
import csv
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response,url_for
import security_check as sc

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir,static_url_path='')
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

@app.route('/perf_vis')
def myperf_vis():
    return render_template('perf_vis.html',cteam='Choose Team',X='Choose X',Y='Choose Y')

@app.route('/perf_vis/query_in',methods=['POST'])
def perf_vis_query():
    nteam = request.form.get('team')
    player = request.form.get('player')
    #location = request.form.get('location')
    print nteam
    print player
    #print location
    team = sc.parse_team(nteam)
    perf_resultsX = []
    perf_resultsY = []
    results = []
    X_axis=[]
    Y_axis=[]

    if team == 'error':
        print "Error: Team Not Found. Using default: Miami Heat"
        team = 'MIA'
    if player == "Choose Player" :#display performance of team using default X and Y if not given
        print request.form.get('X-Axis')
        X_axis = sc.secure_axis(request.form.get('X-Axis'))
        Y_axis = sc.secure_axis(request.form.get('Y-Axis'))
        query_string = "SELECT E.ssn As pssn, E.name AS pname, P.age, E.salary, T.tid " \
                       "FROM Pay_Born_Emp As E JOIN Player As P Using(ssn), from_Team As T, Performance PE " \
                       "WHERE PE.ssn = P.ssn and E.tid = T.tid and T.tid = '" + team + "';"
        cursor = g.conn.execute(query_string)
        for result in cursor:
            results.append(result['pname'])  # can also be accessed using result[0]
            p_query_string = "SELECT PE.ssn As pssn, PE." + X_axis + " AS px, PE." + Y_axis + " AS py " \
                            "FROM Performance PE " \
                            "WHERE PE.ssn = '"+result['pssn']+"' and season = '16-17';"
            cursortwo = g.conn.execute(p_query_string)
            for resulttwo in cursortwo:
                print resulttwo
                perf_resultsX.append(resulttwo['px'])
                perf_resultsY.append(resulttwo['py'])
        cursor.close()
        print results
    else:#display performance of particular player - on top of team info and make it biiiiiG!!
        X_axis = request.form.get('X-Axis')
        Y_axis = request.form.get('Y-Axis')
        if X_axis == Y_axis:
            print "meaningless query"
        p_query_string = "SELECT E.ssn As pssn, E.name as pname, PE."+X_axis+" AS px, PE."+Y_axis+" AS py " \
                       "FROM Pay_Born_Emp As E JOIN Player As P Using(ssn), Performance PE " \
                       "WHERE PE.ssn = P.ssn and season = '16-17' and E.name = '"+player+"';"
        cursor = g.conn.execute(p_query_string)
        for result in cursor:
            print result
            results.append(result['pname'])
            perf_resultsX.append(result['px'])  # can also be accessed using result[0]
            perf_resultsY.append(result['py'])
        cursor.close()

    return render_template('perf_vis.html',cteam=nteam,cplayer=player,t_player_data = results,pX=perf_resultsX,pY=perf_resultsY,X=X_axis,Y=Y_axis)

@app.route('/tquery', methods=['GET', 'POST'])
def my_query():
    error = None
    if request.method == 'POST':
        mytable =  request.form['table']
        print mytable
        cursor = g.conn.execute("SELECT ssn FROM player")
        names = []
        for result in cursor:
            names.append(result['ssn'])  # can also be accessed using result[0]
        cursor.close()
        print names

    return render_template('/visualization/vis_main.html', my_data=names)

@app.route('/company_sponsor')
def company_sponsor_foo():
    query = "select c.name cname, t.name tname "\
            "from from_Team t,company c, sponsor s "\
            "where s.cid=c.cid and s.tid=t.tid;"
    cursor = g.conn.execute(query)
    results = []
    for result in cursor:
        print result
        results.append(result)  # can also be accessed using result[0]
    cursor.close()
    return render_template('company_sponsor.html',fdata=results)

@app.route('/player_info')
def player_info_foo():
    query = "select p.name,l.state, l.city "\
            "from location l, Pay_Born_Emp p "\
            "where p.lid=l.lid;"
    cursor = g.conn.execute(query)
    results = []
    for result in cursor:
        print result
        results.append(result)  # can also be accessed using result[0]
    cursor.close()
    return render_template('player_info.html',fdata=results)

@app.route('/Game_visualization')
#app_url_rule('/','Game_visualization',Game_visualization_foo)
def Game_visualization_foo():

    query="select g.gid,g.guest_team,g.host_team,l.state,l.city,l.stadium "\
          "from  Location l, Game_at g "\
          "where g.lid=l.lid;"
    cursor = g.conn.execute(query)
    results = []
    for result in cursor:
        print result
        results.append(result)  # can also be accessed using result[0]
    cursor.close()

    return render_template('Game_visualization.html',fdata=results)

@app.route('/player_analysis')
def player_analysis_foo():
    query="select b.name,b.salary,p.points, p. assists, p.rebounds,p.three_points "\
          "from Pay_Born_Emp b, Performance p "\
          "where b.ssn=p.ssn;"
    cursor = g.conn.execute(query)
    results = []
    for result in cursor:
        print result
        results.append(result)  # can also be accessed using result[0]
    cursor.close()
    return render_template('player_analysis.html',fdata=results)

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