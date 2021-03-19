from flask import Blueprint, render_template, request, redirect, url_for, session, sessions
from sqlalchemy import func
from flask_login import current_user
from manager.models.Books import Books, Tags, Authors, Categories
from manager.models.Quotes import Quotes
from manager.models.Users import Users
from datetime import timedelta, datetime
from manager.lib.organizer import Organizer, Sort

main = Blueprint('main', __name__)

@main.route('/')
def home():
    organizer = Organizer()
    random_tags = Tags.query.order_by(func.random()).limit(10)
    return render_template('apps/main/home.html', organizer=organizer, random_tags=random_tags)

@main.route('/explore')
def explore():
    books = Sort()
    random_tags = Tags.query.order_by(func.random()).limit(10)
    return render_template('apps/main/explore.html', books=books, random_tags=random_tags)


@main.route('/categories')
def categories():
    return render_template('apps/main/categories.html')


@main.route('/popular')
def popular():
    books = Books.query.all()
    random_tags = Tags.query.order_by(func.random()).limit(10)
    return render_template('apps/main/popular.html', books=books, random_tags=random_tags)


@main.route('/top-10s')
def top10():
    books = Books.query.all()
    random_tags = Tags.query.order_by(func.random()).limit(10)
    return render_template('apps/main/top10.html', books=books, random_tags=random_tags)

@main.route('/search')
def search():
    search = request.args.get('q')
    page = request.args.get('page')
    query = Books.query.order_by(Books.created_on.desc())
    if search:
        query = query.filter((Books.description.contains(search)) | (Books.title.contains(search)))
        if page and page.isdigit():
            page = int(page)
        books = query.paginate(page, 16)
        return render_template('apps/main/search.html', books=books)
    else:
        return redirect(url_for('main.home'))
    return render_template('apps/main/search.html')
