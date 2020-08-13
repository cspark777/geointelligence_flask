# backend/views.py

from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from socialblog import db
from socialblog.models import BlogPost, Comments, Charts, Contacts
from socialblog.backend.forms import BackendForm
from socialblog.blog_posts.forms import BlogPostForm
from socialblog.charts.forms import ChartForm

from socialblog import images, videos


backend = Blueprint('backend', __name__)

# dashboard
@backend.route('/backend/', methods=['GET', 'POST'])
@login_required
def backend_dashboard():      
    #return render_template('/backend/dashboard.html')
    return redirect('/backend/posts')

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
    if current_user.username == "admin":
        blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).all()    
    else:
        blog_posts = BlogPost.query.filter_by(user_id=current_user.id).order_by(BlogPost.date.desc()).all()

    return render_template('/backend/posts.html', posts=blog_posts)

# CREATE
@backend.route('/backend/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        if form.post_image.data:
            
            content_type = request.files['post_image'].content_type

            if "video" in content_type:
                filename = videos.save(request.files['post_image'])    
                content_type = "video"
                url = videos.url(filename)
            else:
                filename = images.save(request.files['post_image'])
                content_type = "image"
                url = images.url(filename)

            blog_post = BlogPost(title=form.title.data,
                             text=form.text.data, user_id=current_user.id, image_filename=filename, image_url=url, image_type=content_type)

        else:
            blog_post = BlogPost(title=form.title.data,
                             text=form.text.data, user_id=current_user.id)
         
        db.session.add(blog_post)
        db.session.commit()
        return redirect(url_for('backend.backend_posts'))
    return render_template('/backend/create_post.html', title='Updating', form=form, page_name="New Post")


# UPDATE
@backend.route('/backend/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    blog_post = BlogPost.query.get_or_404(post_id)

    #print(blog_post.author)
    #print(current_user)
    if current_user.username != "admin":
        if blog_post.author != current_user:
            abort(403)

    form = BlogPostForm()
    
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data

        if form.post_image.data:

            content_type = request.files['post_image'].content_type

            if "video" in content_type:
                filename = videos.save(request.files['post_image'])    
                content_type = "video"
                url = videos.url(filename)
            else:
                filename = images.save(request.files['post_image'])
                content_type = "image"
                url = images.url(filename)
            
            

            blog_post.image_filename = filename
            blog_post.image_url = url
            blog_post.image_type = content_type

        print(blog_post.image_filename)
        print(blog_post.image_url)
        print(blog_post.image_type)

        db.session.commit()
        flash(u'Your Post has been updated', 'alert alert-success')
        return redirect(url_for('backend.backend_posts'))

    form.title.data = blog_post.title
    form.text.data = blog_post.text
    return render_template('/backend/create_post.html', title='Updating', form=form, page_name="Update Post")

# DELETE
@backend.route('/backend/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    blog_post = BlogPost.query.get_or_404(post_id)

    if current_user.username != "admin":
        if blog_post.author != current_user:
            abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash(u'Blog Post Deleted', 'alert alert-warning')
    return redirect(url_for('backend.backend_posts'))



# posts
@backend.route('/backend/charts', methods=['GET', 'POST'])
@login_required
def backend_charts():     
    if current_user.username != "admin":   
        abort(403)

    charts = Charts.query.order_by(Charts.id.asc()).all()        
    return render_template('/backend/charts.html', charts=charts)

# UPDATE
@backend.route('/backend/chart/<int:chart_id>/update', methods=['GET', 'POST'])
@login_required
def chart_update(chart_id):
    chart = Charts.query.get_or_404(chart_id)
    if current_user.username != "admin":        
        abort(403)

    form = ChartForm()
    if form.validate_on_submit():
        chart.title = form.title.data
        chart.text = form.text.data        

        db.session.commit()
        flash(u'Your Chart has been updated', 'alert alert-success')
        return redirect(url_for('backend.backend_charts'))

    form.title.data = chart.title
    form.text.data = chart.text
    return render_template('/backend/create_chart.html', title='Updating', form=form, page_name="Update Chart")

# contacts
@backend.route('/backend/contacts', methods=['GET', 'POST'])
@login_required
def backend_contacts():     
    if current_user.username != "admin":   
        abort(403)

    contacts = Contacts.query.order_by(Contacts.id.desc()).all()        
    return render_template('/backend/contacts.html', contacts=contacts)
