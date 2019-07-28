from flask import Blueprint
from flask import render_template
from flask import request, url_for
from flask import redirect
from models import Post
from .forms import PostForm
from app import db
from flask_security import login_required



posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def post_create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('Error')

        return redirect(url_for('posts.index'))
    form = PostForm()
    return render_template('posts/post_create.html', form=form)


@posts.route('/edit/<int:id>', methods=['POST', 'GET'])
def post_edit(id):
    post = Post.query.filter(Post.id == id).first()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_detail', id=post.id))

    form = PostForm(obj=post)
    return render_template('posts/post_edit.html', post=post, form=form)


@posts.route("/delete/<int:id>", methods=["POST"])
def post_delete(id):
    post = Post.query.filter(Post.id == id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.index'))



@posts.route('/<int:id>')
def post_detail(id):
    post = Post.query.filter(Post.id == id).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


@posts.route('/')
def index():
    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q)).all()
    else:
        posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)