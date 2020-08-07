from flask import Blueprint, render_template, request, redirect, url_for, session, sessions
from sqlalchemy import func
from flask_login import current_user
from manager.models.Books import Books, Tags, Authors
from manager.models.Users import Users
from datetime import timedelta, datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    books = Books.query.order_by(func.random()).limit(10)
    random_tags = Tags.query.order_by(func.random()).limit(10)
    return render_template('apps/main/home.html', books=books, random_tags=random_tags)


@main.route('/explore')
def explore():
    books = sort_books()
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
        query = query.filter( (Books.description.contains(search) ) |
				              (Books.title.contains(search))
                            )
        if page and page.isdigit():
            page = int(page)
        books = query.paginate(page, 16)
        return render_template('apps/main/search.html', books=books)
    else:
        return redirect(url_for('main.home'))
    return render_template('apps/main/search.html')


def sort_books():
    if request.method == 'GET':
        sort_q = request.args.get('s')
        page_e = request.args.get('page' , 1 , type=int)
        if sort_q == 'down':
            books = Books.query.filter(Books.post_status == 0).order_by(Books.downloads.desc()).paginate(page=page_e ,per_page=16)
        elif sort_q == 'pg':
            books = Books.query.filter(Books.post_status == 0).order_by(Books.pages.desc()).paginate(page=page_e ,per_page=16)
        elif sort_q == 'pop':
            books = Books.query.filter(Books.post_status == 0).order_by(Books.pg_views.desc()).paginate(page=page_e ,per_page=16)
        elif sort_q == 'pub':
            books = Books.query.filter(Books.post_status == 0).order_by(Books.created_on.desc()).paginate(page=page_e ,per_page=16)
        elif sort_q == 'size':
            books = Books.query.filter(Books.post_status == 0).order_by(Books.size.desc()).paginate(page=page_e ,per_page=16)
        else:
            books = Books.query.filter(Books.post_status == 0).order_by(Books.pg_views.desc()).paginate(page=page_e ,per_page=16)
            
        return books