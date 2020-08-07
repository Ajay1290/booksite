from flask import render_template, url_for, flash, redirect, request , send_file , abort, Blueprint, current_app, session
import os
from manager.ext import db
import sys
import secrets
import urllib.parse
from sqlalchemy import func
from flask_login import current_user, login_required, login_user
from manager.apps.books.forms import BookForm
from manager.models.StaticFiles import BookFile, CoverImage
from manager.models.Books import Books, Reports, Categories, Comments, Authors, Publishers, Downloads, Tags
from manager.models.Users import Users
from manager.apps.books.forms import CommentForm, ReportForm, BookUpdateForm
from manager.apps.users.forms import SignupForm

books = Blueprint('books', __name__)

def recommend_books(cur_book, count):
    rec_books = []
    for books in Books.query.all():
        if rec_books.__len__() > count:
            break
        if books != cur_book:
            for tag in cur_book.tags:
                if tag in books.tags:                    
                    rec_books.append(books)
                    break    
    return rec_books

@books.route('/books/<book_id>', methods=['GET','POST'])
def book(book_id):
    book = Books.query.get_or_404(book_id)
    book.pg_views += 1
    db.session.commit()
    books_all = Books.query.order_by(func.random()).limit(5)
    uploader = Users.query.filter_by(username=book.user.username).first_or_404()
    uploader_books = Books.query.filter_by(user=uploader).order_by(Books.created_on.desc()).limit(5)    
    rec_books = recommend_books(book, 5)    
    random_books = Books.query.order_by(func.random()).limit(10)
    random_tags = Tags.query.order_by(func.random()).limit(10)
    random_authors = Authors.query.order_by(func.random()).limit(4)
    report_form = ReportForm()
    comment_form = CommentForm()
    form = SignupForm()
    if report_form.validate_on_submit():
        report = Reports(problem=report_form.report_options.data, describe=report_form.content.data,
                         problem_by=book,user_id=current_user.id)
        db.session.add(report)
        db.session.commit()
        flash('Your report has been sent activities regarding your problem will start in while.', 'success')
        return redirect(url_for('main.home'))    
    if comment_form.validate_on_submit():
        comment = Comments(content=comment_form.comment.data, user_id=current_user.id, book_id=book.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('books.book', book_id=book.id))        
    if form.validate_on_submit():
        user = Users(username=form.username.data.lower(),
                     password = form.password.data,
                     email=form.email.data.lower())
        db.session.add(user)
        db.session.commit()
        if login_user(user):
            user.update_activity_tracking(request.remote_addr)             
            flash('Welcome, Your account has been created and now You are able browse books as well as upload books.', 'success')
            return redirect(url_for('main.home'))
    return render_template('apps/books/book.html', book=book, uploader_books=uploader_books, books_all=books_all,
                            uploader=uploader, rec_books=rec_books, random_books=random_books, comment_form=comment_form, random_tags=random_tags,
                            form=form, report_form=report_form, random_authors=random_authors, Users=Users)

@books.route('/books/upload', methods=['GET','POST'])
def book_upload():
    form = BookForm()
    categories = Categories.query.all()
    try:
        if form.validate_on_submit():
            file = form.file.data
            image = form.image.data
            print(image)
            book = Books(title = form.title.data,
                         description = form.description.data,
                         tags = form.tags.data,
                         user_id = current_user.id,
                         size = request.form.get('size'),
                         pages = request.form.get('pages'),
                         authors = form.authors.data,
                         language = request.form.get('language'),
                         publishers = form.publisher.data,
                         isbn10 = form.isbn10.data,
                         isbn13 = form.isbn10.data,
                        )
            if Categories.query.get(request.form.get('categories')):
                book.categories = [Categories.query.get(request.form.get('categories'))]
            db.session.add(book)
            db.session.commit()
            if file:            
                if image:
                    file = BookFile(file=file, book_id=book.id)
                    image = CoverImage(image=image, book_id=book.id)
                    db.session.add(image)
                    db.session.add(file)
                    db.session.commit()
                else:
                    file = BookFile(file=file, scrape=True, book_id=book.id)
                    db.session.add(file)
            db.session.commit()
            return redirect(url_for('main.home'))
    except Exception as e:
        print(e)
        flash('There is Something Wrog with this book please upload any other copy.','warning')
        return redirect(url_for('books.book_upload'))
    return render_template('apps/books/book_upload.html', form=form, categories=categories)


@books.route('/books/<book_id>/download')
def book_download(book_id):
    if not 'downloads' in session.keys():
        session['downloads'] = 0
    if session['downloads'] >= 5:
        if current_user.is_authenticated:
            if session['downloads'] >= 10:
                flash('You already downloaded 10 Books a day.', 'success')
                return redirect(url_for('pages.download_limit'))
        else:
            flash('You already downloaded 5 Books a day.', 'success')
            return redirect(url_for('pages.download_limit'))
    session['downloads'] += 1
    book = Books.query.get_or_404(book_id)
    if current_user.is_anonymous == False:
        download = Downloads(user_id=current_user.id, book_id=book.id)
        db.session.add(download)
        db.session.commit()
    return send_file(current_app.root_path+'/static/books/' + str(book.file[0].path) , 
                     attachment_filename= book.title+ ' ( BookElf.in )' + '.pdf', as_attachment=True)


@books.route('/books/<book_id>/update', methods=['GET','POST'])
def book_update(book_id):
    book = Books.query.get(book_id)
    form = BookUpdateForm()
    if form.validate_on_submit():
        file = form.file.data
        image = form.image.data
        book.title = form.title.data
        book.content = form.description.data
        book.tags = form.tags.data
        if file:            
            if image:
                file = BookFile(file=file, book_id=book.id)
                data = BookFile.scrape_metadata(file.path)
                book.size = data['size']
                book.pages = data['pages']
                book.authors = data['authors']
                image = CoverImage(image=image, book_id=book.id)
                db.session.add(image)
                db.session.add(file)
                db.session.commit()
            else:
                file = BookFile(file=file, scrape=True, book_id=book.id)
                data = BookFile.scrape_metadata(file.path)
                book.size = data['size']
                book.pages = data['pages']
                book.authors = data['authors']
                db.session.add(file)
        db.session.commit()
        flash('Your book has been updated', 'success')
        return redirect(url_for('main.home'))
    if request.method == 'GET':
        form.title.data = book.title
        form.description.data = book.description
        form.tags.data = book.tags
    return render_template('apps/books/book_update.html', book=book, form=form)


@books.route('/books/<book_id>/delete')
def book_delete(book_id):
    book = Books.query.get_or_404(book_id)
    if book.user != current_user:
        abort(403)
    db.session.delete(book.file[0])
    db.session.delete(book.image[0])
    for com in book.comments:
        db.session.delete(com)
    for reo in book.reports:
        db.session.delete(reo)
    db.session.delete(book)
    db.session.commit()
    flash('Your book has been deleted.' , 'success')
    return redirect(url_for('main.home'))
