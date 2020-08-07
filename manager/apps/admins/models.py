from sqlalchemy import func
from manager.ext import db

class Dashboard:

    

    @classmethod
    def group_and_count(cls, model, field):
        count = func.count(field)
        query = db.session.query(count, field).group_by(field).all()
        results = {
            'query': query,
            'total': model.query.count()
        }
        return results
