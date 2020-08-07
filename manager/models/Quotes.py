from manager import db

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String, nullable=False)
    quote_by = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Quotes {self.quote} --{self.quote_by}>'