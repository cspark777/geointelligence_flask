# core/views.py

from flask_dance.contrib.google import make_google_blueprint, google
from flask import render_template, request, Blueprint, redirect, url_for, jsonify
from socialblog.models import BlogPost, Charts, Contacts
from socialblog.core.forms import ContactForm
import settings
from socialblog import db
import mysql.connector
import random
from collections import deque
from threading import Timer
from datetime import datetime, timedelta
import time
import json

core = Blueprint('core', __name__)

mydb = mysql.connector.connect(
    host=settings.MYSQL_HOST,
    user=settings.MYSQL_USER,
    passwd=settings.MYSQL_PASSWORD,
    database=settings.MYSQL_DATABASE,
    charset = 'utf8'
)

g_update_interval_time = 10 #10 sec
g_x_axis_count = 180

g_graph1_data = {
                'y_positive': deque(maxlen=g_x_axis_count), 
                'y_negative': deque(maxlen=g_x_axis_count), 
                'y_neutral': deque(maxlen=g_x_axis_count),
                }

def generate_graph1_data():
    global mydb, g_graph1_data, g_update_interval_time
    
    time_now = datetime.utcnow()

    #print(time_now.strftime('%H:%M:%S'))

    time_interval_before = timedelta(hours=0, minutes=0, seconds=g_update_interval_time)

    time_interval = (time_now - time_interval_before).strftime('%Y-%m-%d %H:%M:%S')
    query = "SELECT SUM(IF(polarity=-1, 1, 0)) AS negative, SUM(IF(polarity=0, 1, 0)) AS neutral, SUM(IF(polarity=1, 1, 0)) AS positive FROM {} WHERE created_at >= '{}' ".format(settings.TABLE_NAME, time_interval)

    graph_data = None
    if mydb.is_connected():
        mycursor = mydb.cursor()        
        mycursor.execute(query)
        graph_data = mycursor.fetchall()   
        mycursor.close()   

    if graph_data[0][0] is None:
        graph_data[0] = (random.randint(1,20), random.randint(50,100), random.randint(1,20))

    #print(graph_data)

    t = int(round(time.time() * 1000))

    y_negative = {"t": t, "y": -graph_data[0][0]}
    y_neutral = {"t": t, "y": graph_data[0][1]}
    y_positive = {"t": t, "y": graph_data[0][2]}
    
    g_graph1_data["y_negative"].append(y_negative)    
    g_graph1_data["y_neutral"].append(y_neutral)
    g_graph1_data["y_positive"].append(y_positive)

    Timer(g_update_interval_time, generate_graph1_data).start()

generate_graph1_data()

@core.route('/', methods=['GET', 'POST'])
def index():

    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=3)

    json_obj = {"y_negative": list(g_graph1_data["y_negative"]), "y_neutral": list(g_graph1_data["y_neutral"]), "y_positive": list(g_graph1_data["y_positive"])}

    chart1_data = json.dumps(json_obj)

    form = ContactForm()    
    form.name = ""
    form.phone = ""
    form.email = ""
    form.message = ""

    chart1 = Charts.query.get_or_404(1)

    return render_template('index.html', form=form, posts=blog_posts, chart1_data=chart1_data, chart1_title=chart1.title)

@core.route('/info')
def info():
    return render_template('info.html')

@core.route('/get_chart1_data')
def get_chart1_data():
    json_obj = {"y_negative": list(g_graph1_data["y_negative"]), "y_neutral": list(g_graph1_data["y_neutral"]), "y_positive": list(g_graph1_data["y_positive"])}
    return jsonify(json_obj)

@core.route('/post/<int:post_id>',  methods=['GET'])
def view_post(post_id):
    json_obj = {"y_negative": list(g_graph1_data["y_negative"]), "y_neutral": list(g_graph1_data["y_neutral"]), "y_positive": list(g_graph1_data["y_positive"])}

    chart1_data = json.dumps(json_obj)

    blog_post = BlogPost.query.get_or_404(post_id)
    return render_template('/post.html', post=blog_post, chart1_data=chart1_data)

@core.route('/chart/<int:chart_id>',  methods=['GET'])
def view_chart(chart_id):
    chart = Charts.query.get_or_404(chart_id)
    if chart_id == 1:
        json_obj = {"y_negative": list(g_graph1_data["y_negative"]), "y_neutral": list(g_graph1_data["y_neutral"]), "y_positive": list(g_graph1_data["y_positive"])}

        chart1_data = json.dumps(json_obj)

        return render_template('/chart.html', chart_data=chart1_data, chart=chart)

# posts
@core.route('/post_list', methods=['GET', 'POST'])
def post_list():    
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).all()      
    return render_template('/post_list.html', posts=blog_posts)

# contact
@core.route('/contact', methods=['GET', 'POST'])
def contact():   
    form = ContactForm()    
    if form.validate_on_submit():       
        Contact = Contacts(name=form.name.data, phone=form.phone.data, email=form.email.data, message=form.message.data)
         
        db.session.add(Contact)
        db.session.commit()
        
    return redirect(url_for('core.index'))

