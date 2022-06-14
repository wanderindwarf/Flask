import os
import psycopg2
import psycopg2.extras
from flask import Flask, request, render_template, g, current_app
from datetime import datetime
import pytz
from flask.cli import with_appcontext
import click

# initialize Flask
app = Flask(__name__)


######################################################### Routes #######################################################


@app.route("/browse")
def browse():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rowlist = cursor.fetchall()
    return render_template('browse.html', entries=rowlist)


@app.route("/dump")
def dump_entries():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rows = cursor.fetchall()
    output = ""
    for r in rows:
        debug(str(dict(r)))
        output += str(dict(r))
        output += "\n"
    return "<pre>" + output + "</pre>"

# Let's break down the dump_entries() function line by line.

# We get our database connection object via get_db().
# We get a database cursor object by calling cursor(). Cursors are useful, but we'll just gloss over this for now.
# We call the execute() function which executes one SQL command given as a string.
# We then call fetchall() which gives us a list of rows that we can iterate through.
# We make an output string that we will concatenate everything with.

# We start a loop over the rows iterator, using the variable r to represent a single row. r's datatype we can treat much
# like a Python dictionary. In other words, if you want to access a specific attribute, you can use
# r["name-of-attribute"].

# We convert r to a Python dictionary explicitly, then a string (for pretty-printing reasons), then print it with
# debugging and also concatenate it with our output.

# We finally send output to the web browser with return.


@app.route("/")
def homepage():
    return "Hello Catherine!"

#
# @app.route("/time")
# def get_time():
#     now = datetime.now().astimezone(pytz.timezone("US/Central"))
#     timestring = now.strftime(
#         "%Y-%m-%d %H:%M:%S")  # format the time as a easy-to-read string
#     return render_template("time.html", timestring=timestring)


################################################## Database handling ##################################################


@app.cli.command('populate')
def populate_db():
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("populate.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Populated DB with sample data.")


@app.cli.command("initdb")
def init_db():
    """Clear existing data and create new tables."""
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("schema.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Initialized the database.")


def connect_db():
    """Connects to the database."""
    debug("Connecting to DB.")
    conn = psycopg2.connect(host="localhost", user="postgres", password="utqpty,thu", dbname="practice",
                            cursor_factory=psycopg2.extras.DictCursor)
    return conn


def get_db():
    """Retrieve the database connection or initialize it. The connection
    is unique for each request and will be reused if this is called again.
    """
    if "db" not in g:
        g.db = connect_db()

    return g.db


@app.teardown_appcontext
def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
        debug("Closing DB")

# Here are what the functions in this section do:

# connect_db() is in charge of explicitly making a connection to our PostgreSQL database. This function uses the
# psycopg2 library to connect to the database, and returns a connection object.

# get_db() is the function your application code will use to retrieve the database connection object. You can see how
# the code asks the g object if it already has an attribute representing the database connection. If it doesn't,
# it explicitly connects to the database.

# close_db() is the function that closes the database. Just like files, databases should be properly opened and closed
# (or connected to and disconnected from). The only new part of this code is the @app.teardown_appcontext part.
# This is another kind of decorator Flask has; it tells Flask to automatically run this function when the application
# context is being "torn down," which happens at the end of a webpage request. So the effect is that the database
# connection is automatically closed at the end of every individual webpage request.


########################################################### Debugging ##################################################


def debug(s):
    """Prints a message to the screen (not web browser)
    if debugging is turned on."""
    if app.config['DEBUG']:
        print(s)


##################################################### App begins running here ##########################################


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)  # can turn off debugging with False