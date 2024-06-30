from flask import render_template, url_for, redirect, flash
from forms import RegisterForm, ReviewForm, AuthorizationForm, CommentForm, EmailForm
from models import Reviewmodel, User, Comment, Email, BaseModel
from ext import app, db
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from os import path
from flask_login import login_user, logout_user, login_required, current_user

UPLOAD_FOLDER = 'path_to_save_directory'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


profiles = []
reviews = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["GET","POST"])
def contact():
    form = EmailForm()
    if form.validate_on_submit():
        new_email = Email(email=form.email.data)

        db.session.add(new_email)
        db.session.commit()
    return render_template("contact.html", form=form)

@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('registration'))
        
        new_user = User(username=form.username.data, password=form.password.data, phonenum=form.phonenum.data, date=form.date.data, role=form.role.data)

        new_user.create()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('home'))

    return render_template("registration.html", form=form)

@app.route("/authorization", methods=["GET", "POST"])
def authorization():
    form = AuthorizationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template("authorization.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route("/profile/<int:profile_id>")
def profile(profile_id):
    print("revieve profile id:", int(profile_id))
    return render_template("profile.html", user=profiles[profile_id])

@app.route("/review", methods=["GET", "POST"])
def review():
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = Reviewmodel(user=current_user.username, role = current_user.role, title=form.title.data, content=form.content.data)
        if form.image.data:    
            image = form.image.data
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)

            new_review.image = image.filename

        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('review_page'))
    return render_template("review.html", form=form)

@app.route("/reviews/<int:review_id>", methods=["GET", "POST"])
def comment(review_id):
    review = Reviewmodel.query.get_or_404(review_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(user=current_user.username, role=current_user.role, content=form.content.data, review_id=review.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('comment', review_id=review.id))
    
    comments = Comment.query.filter_by(review_id=review.id).order_by(Comment.date_posted.desc()).all()
    return render_template("comment.html", form=form, review=review, comments=comments)


@app.route("/delete-comment/<int:id>")
def delete_comment(id):
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect('/reviews')

@app.route("/reviews")
def review_page():
    reviews = Reviewmodel.query.all()
    return render_template("review-page.html", reviews=reviews)

@app.route("/delete-review/<int:id>")
def delete_review(id):
    review = Reviewmodel.query.get(id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('review'))


@app.route("/edit-review/<int:id>", methods=["GET", "POST"])
def edit_review(id):
    review = Reviewmodel.query.get(id)
    form = ReviewForm(title=review.title, content=review.content)
    if form.validate_on_submit():
        review.title = form.title.data
        review.content = form.content.data

        if form.image.data:
            image = form.image.data
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            review.image = image.filename

        db.session.commit()
        return redirect("/reviews")

    return render_template("review.html", form=form)