from flask import Blueprint, render_template, request
from sqlalchemy import func
from manager.models.Books import Books, Authors, Tags

authors = Blueprint('authors', __name__)

@authors.route('/authors')
def authors_all():
	authors = Authors.query.all()
	return render_template('apps/authors/authors.html', authors=authors)

@authors.route('/authors/<author_id>/')
def author(author_id):
	author = Authors.query.get_or_404(author_id)	
	author_books = author.books.filter(Books.post_status==0)\
								.order_by(Books.created_on.desc())\
								.paginate(page= request.args.get('page',1,type=int), per_page=14)
	random_authors = Authors.query.order_by(func.random()).limit(4)
	return render_template('apps/authors/author.html', author=author, author_books=author_books, random_authors=random_authors)


@authors.route('/authors/<author_id>/follow')
def author_follow(author_id):
	author = Tags.query.get_or_404(author_id)
	return render_template('apps/authors/author.html', author=author)
