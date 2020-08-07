from manager.ext import db

post_tags = db.Table('post_tags',
 db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
 db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
)

author_posts = db.Table('author_posts',
 db.Column('author_id', db.Integer, db.ForeignKey('authors.id')),
 db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
)

categories_books = db.Table('categories_books',
 db.Column('categories_id', db.Integer, db.ForeignKey('categories.id')),
 db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
)

publishers_books = db.Table('publishers_books',
 db.Column('publishers_id', db.Integer, db.ForeignKey('publishers.id')),
 db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
)

categories_tags = db.Table('categories_tags',
 db.Column('categories_id', db.Integer, db.ForeignKey('categories.id')),
 db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

author_categories = db.Table('author_categories',
 db.Column('author_id', db.Integer, db.ForeignKey('authors.id')),
 db.Column('categories_id', db.Integer, db.ForeignKey('categories.id'))
)