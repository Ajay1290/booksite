from flask import Blueprint, render_template, request
from sqlalchemy import func
from manager.models.Books import Books, Authors, Tags, Publishers

authors = Blueprint('authors', __name__)

@authors.route('/authors')
def authors_all():
	authors = Authors.query.all()
	random_tags = Tags.query.order_by(func.random()).limit(10)
	return render_template('apps/authors/authors.html', authors=authors, random_tags=random_tags)

@authors.route('/authors/<author_id>/')
def author(author_id):
	author = Authors.query.get_or_404(author_id)	
	author_books = author.books.filter(Books.post_status==0)\
								.order_by(Books.created_on.desc())\
								.paginate(page= request.args.get('page',1,type=int), per_page=14)
	random_authors = Authors.query.order_by(func.random()).limit(4)
	
	return render_template('apps/authors/author.html', author=author, author_books=author_books
													 , random_authors=random_authors)


@authors.route('/authors/<author_id>/follow')
def author_follow(author_id):
	author = Tags.query.get_or_404(author_id)
	
	return render_template('apps/authors/author.html', author=author)

@authors.route('/publisher')
def publishers_all():
	publishers = Publishers.query.all()
	random_tags = Tags.query.order_by(func.random()).limit(10)
	return render_template('apps/authors/publishers.html', publishers=publishers, random_tags=random_tags)

@authors.route('/publishers/<publisher_id>/')
def publisher(publisher_id):
	publisher = Publishers.query.get_or_404(publisher_id)
	publisher_books = publisher.books.filter(Books.post_status==0)\
								.order_by(Books.created_on.desc())\
								.paginate(page= request.args.get('page',1,type=int), per_page=14)
	random_publishers = Publishers.query.order_by(func.random()).limit(4)

	return render_template('apps/authors/publisher.html', publisher=publisher, publisher_books=publisher_books
														, random_publishers=random_publishers)

@authors.route('/authors/<publisher_id>/follow')
def publisher_follow(publisher_id):
	publisher = Publishers.query.get_or_404(publisher_id)
	return render_template('apps/authors/publisher.html', publisher=publisher)
