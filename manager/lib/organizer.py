from flask import request
from sqlalchemy import func
from manager.models.Books import Books, Tags
from manager.ext import f_db

def books_per_block():
    # new arrivals
    for book in Books.query.order_by(Books.created_on.desc()).order_by(func.random()).limit(10):
        f_db.get('books').get('New Arrivals')['New Arrivals'].append(book.id)
        f_db.commit()

    # Trending
    for book in Books.query.order_by(Books.pg_views.desc()).order_by(func.random()).limit(10):
        f_db.get('books').get('Trending')['Trending'].append(book.id)
        f_db.commit()
    
    # Most Downloaded
    for book in Books.query.order_by(Books.downloads.desc()).order_by(func.random()).limit(10):
        f_db.get('books').get('Most Downloaded')['Most Downloaded'].append(book.id)
        f_db.commit()
    
    # Most Searched
    for book in Books.query.order_by(func.random()).limit(10):
        f_db.get('books').get('Most Searched')['Most Searched'].append(book.id)
        f_db.commit()   
    
    # Editor's choice
    try:
        for book in  Books.query.filter(Books.language == 'Hindi').order_by(func.random()).limit(10):
            f_db.get('books').get("Hindi Books")["Hindi Books"].append(book.id)
            f_db.commit()
    except Exception as e:
        print(e)

    # New inspiring
    try:
        for book in Books.query.filter(Books.categories[0] == 'Inspiring').order_by(func.random()).limit(10):
            f_db.get('books').get('New inspiring')['New inspiring'].append(book.id)
            f_db.commit()
    except Exception as e:
        print(e)


def Organizer():
    organizer = {}
    organizer['new_arrivals'] = [Books.query.get(b_id) for b_id in f_db.get('books').get('New Arrivals')['New Arrivals']]
    organizer['trending'] = [Books.query.get(b_id) for b_id in f_db.get('books').get('Trending')['Trending']]
    organizer['most_downloaded'] = [Books.query.get(b_id) for b_id in f_db.get('books').get('Most Downloaded')['Most Downloaded']]
    organizer['most_searched'] = [Books.query.get(b_id) for b_id in f_db.get('books').get('Most Searched')['Most Searched']]
    organizer['editors_choice'] = [Books.query.get(b_id) for b_id in f_db.get('books').get("Editor's choice")["Editor's choice"]]
    organizer['most_inspiring'] = [Books.query.get(b_id) for b_id in f_db.get('books').get('New inspiring')['New inspiring']]

    if f_db.get('books').get('Programming Tags'):
        organizer['programming_tags'] = [Tags.query.get(t_id) for t_id in f_db.get('books').get('Programming Tags')['Programming Tags']]
        organizer['programming_tags'] = [Tags.query.get(t_id) for t_id in f_db.get('books').get('Programming Tags')['Programming Tags']]
        organizer['programming_tags'] = [Tags.query.get(t_id) for t_id in f_db.get('books').get('Programming Tags')['Programming Tags']]
        organizer['programming_tags'] = [Tags.query.get(t_id) for t_id in f_db.get('books').get('Programming Tags')['Programming Tags']]

    return organizer

def Sort():
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