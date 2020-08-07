from manager.ext import db
from manager.lib.util_sqlalchemy import ResourceMixin
from flask import url_for, current_app
import os 
import sys
import fitz
from werkzeug.utils import secure_filename
import secrets
from PIL import Image
from manager.models.Books import Authors

class CoverImage(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False , default=1)

    def __init__(self, image=None, path=None, **kwargs):        
        super(CoverImage, self).__init__(**kwargs)
        if image:
            self.path = CoverImage.save_book_cover(image)
        elif path:
            self.path = path
        else:
            raise ValueError('Enter Image or Path')

    @classmethod
    def save_book_cover(cls, image):
        random_hex = secrets.token_hex(8)        
        _, f_ext = os.path.splitext(image.filename)
        picture_fn = random_hex + f_ext
        picture_path = current_app.root_path + f'\\static\\book_covers\\{picture_fn}'
        i = Image.open(image)
        output_size = (250, 380)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn   
        

    def __repr__(self):
        return '<CoverImage %d>' % self.book_id
        

class BookFile(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    def __init__(self, file, scrape=False, **kwargs):
        super(BookFile, self).__init__(**kwargs)
        self.path = BookFile.save_book(file)        
        if scrape:
            img_path = BookFile.scrape_cover_image(path=self.path)
            image = CoverImage(path=img_path, book_id=self.book_id)
            db.session.add(image)
            db.session.commit()

    @classmethod
    def save_book(cls, file):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(file.filename)
        book_fn = random_hex + f_ext
        book_path = current_app.root_path + f'\\static\\books\\{book_fn}'
        file.save(book_path)

        return book_fn

    @classmethod
    def get_authors_from_string(cls, author_string):
        raw_authors = author_string.replace('and',',').replace('&',',').replace('|',',').split(',')
        author_names = [name.strip() for name in raw_authors if name.strip()]
        existing_authors = Authors.query.filter(Authors.name.in_(author_names))
        new_names = set(author_names) - set([author.name for author in existing_authors])
        new_authors = [Authors(name=name) for name in new_names]        
        return list(existing_authors) + new_authors  

    @classmethod
    def scrape_cover_image(cls, path):
        doc = fitz.open(current_app.root_path + f'\\static\\books\\{path}')        
        mat = fitz.Matrix(0.51,0.58)
        pix = doc[0].getPixmap(alpha=False, matrix = mat)         
        image_name = doc.name[len(doc.name[:-20]):]
        filename = image_name[:-4]
        img_path = current_app.root_path +'\\static\\book_covers\\' + filename + ".jpg"
        pix.writeImage(img_path)        

        return filename + ".jpg"
    

    def __repr__(self):
        return '<File  %d>' % self.book_id



class ProfileImage(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String , nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False , default=1)

    def __init__(self, image, **kwargs):        
        super(ProfileImage, self).__init__(**kwargs)
        self.path = ProfileImage.save_user_file(image)

    @classmethod
    def save_user_file(cls, image):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(image)
        picture_fn = random_hex + f_ext
        picture_path = current_app.root_path + f'\\static\\profile_pic\\{picture_fn}'
        i = Image.open(image)        
        i.save(picture_path)

        return picture_path

    def __repr__(self):
        return '<ProfileImage %d>' % self.user_id

class AuthorProfileImage(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String , nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False , default=1)

    def __init__(self, image, **kwargs):        
        super(AuthorProfileImage, self).__init__(**kwargs)
        self.path = AuthorProfileImage.save_author_file(image)

    @classmethod
    def save_author_file(cls, image):
        random_hex = secrets.token_hex(8)
        picture_fn = random_hex + '.jpg'
        picture_path = current_app.root_path + f'\\static\\author_files\\{picture_fn}'
        i = Image.open(image)
        i.save(picture_path)

        return picture_path

    def __repr__(self):
        return '<AuthorProfileImage %s>' % self.path