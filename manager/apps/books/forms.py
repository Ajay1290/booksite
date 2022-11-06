from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField, BooleanField, TextAreaField, FileField, RadioField
from wtforms.validators import DataRequired, Length, Optional, Regexp, EqualTo
from wtforms_components import EmailField, Email
from flask_wtf.file import FileField, FileAllowed
from wtforms_alchemy.validators import Unique
from manager.lib.util_wtforms import ModelForm
from manager.models.Users import Users
from manager.ext import db
from manager.models import Tags, Authors, Publishers
from manager.apps.users.validations import ensure_identity_exists, ensure_existing_password_matches
import random

class TagField(StringField):
	def _value(self):
		if self.data:
			# Display tags as a comma-separated list.
			return ', '.join([tag.name for tag in self.data])
		return ''
		
	def get_tags_from_string(self, tag_string):
		colors = ['info','primary','dark','light','danger','success','warning','secondary']		
		raw_tags = tag_string.lower().title().split(',')
		# Filter out any empty tag names.
		tag_names = [name.strip() for name in raw_tags if name.strip()]
		 # Query the database and retrieve any tags we have already
		 # saved.
		existing_tags = Tags.query.filter(Tags.name.in_(tag_names))
		 # Determine which tag names are new.
		new_names = set(tag_names) - set([tag.name for tag in existing_tags])
		# Create a list of unsaved Tags instances for the new tags.
		new_tags = [Tags(name=name, color=random.choice(colors)) for name in new_names]
		# Return all the existing tags + all the new, unsaved tags.
		return list(existing_tags) + new_tags
 
	def process_formdata(self, valuelist):
		if valuelist:
			self.data = self.get_tags_from_string(valuelist[0])
		else:
			self.data = []


class AuthorField(StringField):
	def _value(self):
		if self.data:
			# Display tags as a comma-separated list.
			return ', '.join([author.name for author in self.data])
		return ''
		
	def get_authors_from_string(self, author_string):
		raw_authors = author_string.replace('and',',').replace('&',',').replace('|',',').split(',')
		author_names = [name.strip() for name in raw_authors if name.strip()]
		existing_authors = Authors.query.filter(Authors.name.in_(author_names))
		new_names = set(author_names) - set([author.name for author in existing_authors])
		new_authors = [Authors(name=name) for name in new_names]
		return list(existing_authors) + new_authors
 
	def process_formdata(self, valuelist):
		if valuelist:
			self.data = self.get_authors_from_string(valuelist[0])
		else:
			self.data = []

class PublisherField(StringField):
	def _value(self):
		if self.data:
			# Display tags as a comma-separated list.
			return ', '.join([publisher.name for publisher in self.data])
		return ''
		
	def get_publisher_from_string(self, publisher_string):
		raw_publisher = publisher_string.replace('and',',').replace('&',',').replace('|',',').split(',')
		publisher_names = [name.strip() for name in raw_publisher if name.strip()]
		existing_publisher = Publishers.query.filter(Publishers.name.in_(publisher_names))
		new_names = set(publisher_names) - set([publisher.name for publisher in existing_publisher])
		new_publisher = [Publishers(name=name) for name in new_names]
		return list(existing_publisher) + new_publisher
 
	def process_formdata(self, valuelist):
		if valuelist:
			self.data = self.get_publisher_from_string(valuelist[0])
		else:
			self.data = []

class BookForm(ModelForm):
	title = StringField('Title', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])
	isbn10 = StringField('isbn10')
	isbn13 = StringField('isbn13')	

	image = FileField('Book Cover', validators=[FileAllowed(['jpg','jpeg', 'png'])])
	file = FileField('File', validators=[FileAllowed(['pdf'])])	
	tags = TagField('Tags' ,description='Separate multiple tags with commas, insted of space use _ underscore')
	authors = AuthorField('Authors' ,description='Separate multiple authors with commas, insted of space use _ underscore')
	publisher = PublisherField('Publisher' ,description='Separate multiple publisher with commas, insted of space use _ underscore')
	
class BookUpdateForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	description = TextAreaField('Content', validators=[DataRequired()])
	tags = TagField('Tags',description='Separate multiple tags with commas, insted of space use _ underscore')
	image = FileField('Book Cover', validators=[FileAllowed(['jpg','jpeg', 'png'])])
	file = FileField('File', validators=[FileAllowed(['pdf'])])	

class CommentForm(FlaskForm):
	comment = TextAreaField('Comment', validators=[DataRequired()])	

class ReportForm(FlaskForm):
	report_options = RadioField('Reporting for...',choices=[('Copyrighted Material','Copyrighted Material.'),
															('Book failed to load','Book failed to load or download.'),
															('information is wrong','Given information is wrong.'),
															('Adult or prohibited','Any kind of Adult or prohibited found.'),
															('User did not like','You did not like something Here.')])
	content = TextAreaField('Content', validators=[DataRequired()])	