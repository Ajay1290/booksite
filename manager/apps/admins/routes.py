from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import current_user
from sqlalchemy import func
from flask_login import login_required
from manager.apps.users.decorators import role_required
from manager.models import *
from manager.apps.admins.models import Dashboard
from manager.apps.admins.forms import UserForm, BookForm, bulkBook, QuoteForm
from manager.apps.admins.forms import get_authors_from_string, get_tags_from_string
from manager.apps.admins.forms import get_publisher_from_string

admins = Blueprint('admins', __name__, template_folder='templates', url_prefix='/admin')


@admins.before_request
@login_required
@role_required('admin')
def before_request():
    pass

# Dashboard -------------------------------------------------------------------
@admins.route('')
def dashboard():
    d = Dashboard.group_and_count(Tags, Tags.color)
    return render_template('dashboard.html', d=d)

# Users -----------------------------------------------------------------------
@admins.route('/users', defaults={'page': 1})
@admins.route('/users/page/<int:page>')
def users(page):
	paginated_users = Users.query.paginate(page, 50, True)
	return render_template('users/index.html', users=paginated_users)

@admins.route('/users/create', methods=["GET","POST"])
def users_create():
	form = UserForm()
	if form.validate_on_submit():
		user = Users(username=form.username.data,
					 phone=form.phone.data,
					 email=form.email.data,
					 password=form.password.data,
					 locale=form.locale.data,
					 role=request.form.get('role'))
		db.session.add(user)
		db.session.commit()
		flash("Your User has been Created!",'success')
		return redirect(url_for('admins.users_info',user_id=user.id))
	return render_template('users/create.html', form=form)


@admins.route('/users/info/<user_id>')
def users_info(user_id):
	user = Users.query.get(user_id)
	return render_template('users/info.html', user=user)


@admins.route('/users/edit/<user_id>', methods=["GET","POST"])
def users_edit(user_id):
	user = Users.query.get(user_id)
	form = UserForm()
	if request.method == 'GET':
		form.username.data 	= 	user.username
		form.phone.data		=	user.phone
		form.email.data		=	user.email
		form.password.data	=	user.password
		form.locale.data	=	user.locale
	if form.validate_on_submit():
		user.username 	=	 form.username.data
		user.phone 		=	 form.phone.data
		user.email 		=	 form.email.data
		user.password 	=	 form.password.data
		user.locale 	=	 form.locale.data
		user.role 		=	 request.form.get('role')
		db.session.commit()
		flash("Your User has been Updated!", 'success')
		return redirect(url_for('admins.users_info',user_id=user.id))
	return render_template('users/edit.html', user=user, form=form)


@admins.route('/users/delete/<user_id>')
def users_delete(user_id):
	user = Users.query.get(user_id)
	db.session.delete(user)
	db.session.commit()
	flash("Your User has been Deleted!",'success')
	return redirect(url_for('admins.users'))


# Books -----------------------------------------------------------------------
@admins.route('/books', defaults={'page': 1})
@admins.route('/books/page/<int:page>')
def books(page):
	paginated_books = Books.query.paginate(page, 50, True)
	return render_template('books/index.html', books=paginated_books)

@admins.route('/books/create', methods=["GET","POST"])
def books_create():
	form = UserForm()
	if form.validate_on_submit():
		user = Books(username=form.username.data,
					 phone=form.phone.data,
					 email=form.email.data,
					 password=form.password.data,
					 locale=form.locale.data,
					 role=request.form.get('role'))
		db.session.add(user)
		db.session.commit()
		flash("Your User has been Created!",'success')
		return redirect(url_for('admins.users_info',user_id=user.id))
	return render_template('books/create.html', form=form)


@admins.route('/books/info/<book_id>')
def books_info(book_id):
	book = Books.query.get(book_id)
	return render_template('books/info.html', book=book, Users=Users)


@admins.route('/books/bulk', methods=["GET","POST"])
def books_bulk():
	form = bulkBook()
	if form.validate_on_submit():
		files = request.files.getlist('file')
		for i, file in enumerate(files):
			print(i)
			upload_book(form, file, i)
		return redirect(url_for('admins.books'))
	return render_template('books/bulk-upload.html', form=form)

def upload_book(form, file, i):
	book = Books()
	book.title = request.form.getlist('title')[i]
	book.description = request.form.getlist('description')[i]
	if get_tags_from_string(request.form.getlist('tags')[i]):
		book.tags = get_tags_from_string(request.form.getlist('tags')[i])
	book.user_id = current_user.id
	book.size = request.form.getlist('size')[i]
	book.pages = request.form.getlist('pages')[i]
	if get_authors_from_string(request.form.getlist('authors')[i]):
		book.authors = get_authors_from_string(request.form.getlist('authors')[i])
	if request.form.getlist('language'):
		book.language = request.form.getlist('language')[i]
	if get_publisher_from_string(request.form.getlist('publisher')[i]):
		book.publishers = get_publisher_from_string(request.form.getlist('publisher')[i])
	book.isbn10 = request.form.getlist('isbn10')[i]
	book.isbn13 = request.form.getlist('isbn13')[i]
	if Categories.query.get(request.form.getlist('categories')[i]):
		book.categories = [Categories.query.get(request.form.getlist('categories')[i])]
	db.session.add(book)
	db.session.commit()
	if file:
		file = BookFile(file=file, scrape=True, book_id=book.id)
		db.session.add(file)
	db.session.commit()


@admins.route('/books/edit/<book_id>', methods=["GET","POST"])
def books_edit(book_id):
	book = Books.query.get(book_id)
	form = BookForm()
	if request.method == 'GET':
		form.title.data 		= 	book.title
		form.description.data	=	book.description
	if form.validate_on_submit():
		book.title 			=	form.title.data
		book.description 	=	form.description.data
		book.language 		=	request.form.get('language')
		db.session.commit()
		flash("Your Book has been Updated!", 'success')
		return redirect(url_for('admins.users_info',book_id=book.id))
	return render_template('books/edit.html', book=book, form=form)


@admins.route('/books/delete/<book_id>')
def books_delete(book_id):
	book = Books.query.get(book_id)
	print(book.image)
	for i in book.image:
		db.session.delete(i)
		db.session.commit()
	for com in book.comments:
		db.session.delete(com)
		db.session.commit()
	for rep in book.reports:
		db.session.delete(rep)
		db.session.commit()
	for f in book.file:
		db.session.delete(f)
		db.session.commit()
	db.session.delete(book)
	db.session.commit()
	flash("Your Book has been Deleted!",'success')
	return redirect(url_for('admins.books'))

# Users -----------------------------------------------------------------------
@admins.route('/quotes', defaults={'page': 1})
@admins.route('/quotes/page/<int:page>')
def quotes(page):
	paginated_users = Quotes.query.paginate(page, 50, True)
	return render_template('quotes/index.html', quotes=paginated_users)

@admins.route('/quotes/create', methods=["GET","POST"])
def quote_create():
	form = QuoteForm()
	if form.validate_on_submit():
		q = Quotes(quote=form.quote.data,
					  quote_by=form.quote_by.data,)
		db.session.add(q)
		db.session.commit()
		flash("Your Quote has been Created!",'success')
		return redirect(url_for('admins.quotes'))
	return render_template('quotes/create.html', form=form)

@admins.route('/quotes/edit/<user_id>', methods=["GET","POST"])
def quote_edit(user_id):
	quote = Quotes.query.get(user_id)
	form = QuoteForm()
	if request.method == 'GET':
		form.quote.data 		= 	quote.quote
		form.quote_by.data		=	quote.quote_by
	if form.validate_on_submit():
		quote.quote 			=	 form.quote.data
		quote.quote_by 		=	 form.quote_by.data
		db.session.commit()
		flash("Your Quotes has been Updated!", 'success')
		return redirect(url_for('admins.quotes'))
	return render_template('quotes/edit.html', quote=quote, form=form)


@admins.route('/quotes/delete/<user_id>')
def quote_delete(user_id):
	user = Quotes.query.get(user_id)
	db.session.delete(user)
	db.session.commit()
	flash("Your User has been Deleted!",'success')
	return redirect(url_for('admins.quotes'))
