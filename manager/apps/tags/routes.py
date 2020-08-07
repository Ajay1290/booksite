from flask import Blueprint, render_template, request
from sqlalchemy import func
from manager.models.Books import Books, Tags

tags = Blueprint('tags', __name__)


@tags.route('/tags/<tag_id>/')
def tag(tag_id):
	tag = Tags.query.get_or_404(tag_id)	
	random_tags = Tags.query.order_by(func.random()).limit(10)
	books_by_tag = tag.books.filter(Books.post_status == 0).order_by(Books.created_on.desc()).paginate(page=request.args.get('page' , 1 , type=int) ,per_page=16)
	return render_template('apps/tags/tag.html', tag=tag, books_by_tag=books_by_tag, random_tags=random_tags)

@tags.route('/tags/<tag_id>/follow')
def tag_follow(tag_id):
	tag = Tags.query.get_or_404(tag_id)
	return render_template('apps/tags/tag.html', tag=tag)
