# backend/views.py

from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from socialblog import db
from socialblog.models import BlogPost, Comments
from socialblog.backend.forms import BackendForm
from socialblog import images


backend = Blueprint('backend', __name__)

# dashboard
@backend.route('/backend/', methods=['GET', 'POST'])
@login_required
def backend_dashboard():      
    return render_template('/backend/dashboard.html')

'''
# users
@backend.route('/backend/users', methods=['GET', 'POST'])
@login_required
def backend_users():    
    username = current_user.username
    if username != "admin":
        flash('You have no previlege to access this page')
        return redirect(url_for('backend.backend_dashboard'))
    return render_template('/backend/dashboard.html')
'''


# posts
@backend.route('/backend/posts', methods=['GET', 'POST'])
@login_required
def backend_posts():    
    print(current_user)
    return render_template('/backend/posts.html')

