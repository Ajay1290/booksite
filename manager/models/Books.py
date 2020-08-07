from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer
from manager.ext import db
from manager.lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from manager.models.Relations import *


POST_ACCESS = { 'live': 0, 'draft': -1, 'down':-100 }

class Books(db.Model , ResourceMixin):

    id = db.Column(db.Integer, primary_key=True)
    
    # Book Metadata
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    size = db.Column(db.String, default='0')
    pages = db.Column(db.Integer, default=0)
    isbn13 = db.Column(db.String(13), default='')
    isbn10 = db.Column(db.String(10), default='')
    language = db.Column(db.String(100), default='')

    downloads = db.Column(db.Integer, default=0)
    pg_views = db.Column(db.Integer, default=0)
    post_status = db.Column(db.String, default='0')

    # Book uploaded By
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relation Ship
    image = db.relationship('CoverImage', backref='book', lazy=True)
    file = db.relationship('BookFile', backref='book', lazy=True)
    tags = db.relationship('Tags', secondary=post_tags, backref=db.backref('books', lazy='dynamic'))
    authors = db.relationship('Authors', secondary=author_posts, backref=db.backref('books', lazy='dynamic'))
    comments = db.relationship('Comments', backref='books', lazy='dynamic')
    reports = db.relationship('Reports', backref='problem_by', lazy=True)
    categories = db.relationship('Categories', secondary=categories_books, backref=db.backref('books', lazy='dynamic'))
    publishers = db.relationship('Publishers', secondary=publishers_books, backref=db.backref('books', lazy='dynamic'))
        

    @property
    def tag_list(self):
        return ', '.join(tag.name for tag in self.tags)      

    # @classmethod
    def is_live(self):
        return self.post_status == POST_ACCESS['live']

    def is_draft(self):
        return self.post_status == POST_ACCESS['draft']

    def is_down(self):
        return self.post_status == POST_ACCESS['down']
    
    @property
    def contenty(self):
        return self.body[:100]


    def __repr__(self):
        return f"<Book {self.title}>"

class Reports(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    problem = db.Column(db.String(60), nullable=False)
    describe = db.Column(db.Text)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Report {self.book_id} | {self.problem}>'


class Comments(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.book_id} | {self.content}>'

class Tags(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100), unique=True)
     color = db.Column(db.String(100))
     categories = db.relationship('Categories', secondary=categories_tags, backref=db.backref('tags', lazy='dynamic'))

     def __repr__(self):
        return f'<Tag {self.name}>' 

class Authors(db.Model, ResourceMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    content = db.Column(db.Text)
    image_file = db.relationship('AuthorProfileImage', backref='author_image', lazy=True)
    categories = db.relationship('Categories', secondary=author_categories, backref=db.backref('authors', lazy='dynamic'))
    pg_views = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Auhtor  %s>' % self.name

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

class Publishers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Publishers {self.name}>'

class Downloads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False , default=1)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False , default=1)

    def __init__(self,  **kwargs):        
        super(Downloads, self).__init__(**kwargs)
        Books.query.get(self.book_id).downloads += 1
        db.session.commit()

    def __repr__(self):
        return f'<Downloads {self.book_id} by {self.user_id}>'