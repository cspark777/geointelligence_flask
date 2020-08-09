# core/views.py

from flask_dance.contrib.google import make_google_blueprint, google
from flask import render_template, request, Blueprint, redirect, url_for, jsonify
from socialblog.models import BlogPost
import settings

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

@core.route('/')
def index():

    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=3)

    json_obj = {"y_negative": list(g_graph1_data["y_negative"]), "y_neutral": list(g_graph1_data["y_neutral"]), "y_positive": list(g_graph1_data["y_positive"])}

    chart1_data = json.dumps(json_obj)

    #print(list(g_graph1_data))
    #print(chart1_data)

    return render_template('index.html', posts=blog_posts, chart1_data=chart1_data)

@core.route('/info')
def info():
    return render_template('info.html')

@core.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

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
    if chart_id == 1:
        json_obj = {"y_negative": list(g_graph1_data["y_negative"]), "y_neutral": list(g_graph1_data["y_neutral"]), "y_positive": list(g_graph1_data["y_positive"])}

        chart1_data = json.dumps(json_obj)

        chart1_title = "Tweets about Covid-19"
        chart1_txt = 'Coronavirus disease 2019 (COVID-19) is an infectious disease caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2).[9] It was first identified in December 2019 in Wuhan, Hubei, China, and has resulted in an ongoing pandemic.[10][11] The first confirmed case has been traced back to 17 November 2019 in Hubei.[12] As of 9 August 2020, more than 19.7 million cases have been reported across 188 countries and territories, resulting in more than 728,000 deaths. More than 11.9 million people have recovered.[8]\
\
Common symptoms include fever, cough, fatigue, shortness of breath, and loss of smell and taste.[13][5][6][14] While the majority of cases result in mild symptoms, some progress to acute respiratory distress syndrome (ARDS) possibly precipitated by cytokine storm,[15] multi-organ failure, septic shock, and blood clots.[16][17][18] The time from exposure to onset of symptoms is typically around five days, but may range from two to fourteen days.[5][19]\
\
The virus is primarily spread between people in proximity,[a] most often via small droplets produced by coughing,[b] sneezing, and talking.[6][20][22] The droplets usually fall to the ground or onto surfaces rather than travelling through air over long distances.[6][23] However, the transmission may also occur through smaller droplets that are able to stay suspended in the air for longer periods of time in enclosed spaces, as typical for airborne diseases.[24] Less commonly, people may become infected by touching a contaminated surface and then touching their face.[6][20] It is most contagious during the first three days after the onset of symptoms, although spread is possible before symptoms appear, and from people who do not show symptoms.[6][20] The standard method of diagnosis is by real-time reverse transcription polymerase chain reaction (rRT-PCR) from a nasopharyngeal swab.[25] Chest CT imaging may also be helpful for diagnosis in individuals where there is a high suspicion of infection based on symptoms and risk factors; however, guidelines do not recommend using CT imaging for routine screening.[26][27]\
\
Recommended measures to prevent infection include frequent hand washing, maintaining physical distance from others (especially from those with symptoms), quarantine (especially for those with symptoms), covering coughs, and keeping unwashed hands away from the face.[7][28][29] The use of cloth face coverings such as a scarf or a bandana has been recommended by health officials in public settings to minimise the risk of transmissions, with some authorities requiring their use.[30][31] Health officials also stated that medical-grade face masks, such as N95 masks, should be used only by healthcare workers, first responders, and those who directly care for infected individuals.[32][33]\
\
There are no vaccines nor specific antiviral treatments for COVID-19.[6] Management involves the treatment of symptoms, supportive care, isolation, and experimental measures.[34] The World Health Organization (WHO) declared the COVID‑19 outbreak a public health emergency of international concern (PHEIC)[35][36] on 30 January 2020 and a pandemic on 11 March 2020.[11] Local transmission of the disease has occurred in most countries across all six WHO regions.[37]'

        return render_template('/chart.html', chart_data=chart1_data, title=chart1_title, text=chart1_txt)
