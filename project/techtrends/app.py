import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash, make_response
from werkzeug.exceptions import abort
import logging, sys

# define a global variable to count number of connections to the database
CON_COUNT = 0
# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global CON_COUNT
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    # increment for reach connection
    CON_COUNT += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/post/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      return render_template('404.html'), 404
    else:
      # log article that just got retrieved.
      app.logger.info('Article "{}" retrieved!'.format(post['title']))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            # log article title that just got created
            app.logger.info('Article "{}" created!'.format(title))

            return redirect(url_for('index'))

    return render_template('create.html')

# define the route to access the health of the application
@app.route('/healthz')
def health():
    data = {"result": "Ok - healthy"}
    return make_response(jsonify(data), 200)

# define the route to access metrics 
@app.route('/metrics')
def metric():
    # Connect and get all posts to determine the number of posts
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()

    data = {"db_connection_count": CON_COUNT, "post_count": len(posts)}
    return make_response(jsonify(data), 200)

# start the application on port 3111
if __name__ == "__main__":
    # set logger to handle STDOUT and STDERR
   stdout_handler = logging.StreamHandler(sys.stdout) # stdout handler 
   stderr_handler = logging.StreamHandler(sys.stderr) # stderr handler 
   handlers = [stderr_handler, stdout_handler]
   # format output
   format_output = '%(levelname)s: %(name)-2s - [%(asctime)s] - %(message)s'
   
   logging.basicConfig(format=format_output, level=logging.DEBUG, handlers=handlers)

   app.run(host='0.0.0.0', port='3111')
