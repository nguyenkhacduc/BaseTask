from flask_restplus import fields
from source.server.instance import server
from datetime import datetime

author = server.api.model('Author', {
    'id': fields.Integer(primary_key=True, required=True, readonly=True, description="Author's ID"),
    'firstname': fields.String(max_length=100, description="Author's first name"),
    'lastname': fields.String(max_length=100, description="Author's last name"),
    'email': fields.String(max_length=100, required=True, unique=True, description="Author's email"),
    'phone': fields.String(max_length=20, unique=True, description="Author's phone number"),
    'address': fields.String(max_length=100, description="Author's address"),
    'status': fields.String(max_length=200, description="Author's status"),
    'created': fields.DateTime(description="Time profile created"),
    'updated': fields.DateTime(description="Time profile updated")
})

book = server.api.model('Book', {
    'id': fields.Integer(primary_key=True, required=True, readonly=True, description="Book ID"),
    'title': fields.String(max_length=100, description="Book title"),
    'isbn': fields.String(nullable=False, max_length=10, required=True, unique=True, description="Book ISBN"),
    'year': fields.Integer(min=0,max=datetime.now().year, description="Publish year"),
    'author_id': fields.Integer(nullable=False, description="Book author"),
    'status': fields.String(max_length=200, description="Book status"),
    'created': fields.DateTime(description="Time book's information created"),
    'updated': fields.DateTime(description="Time book's information updated"),
    'view': fields.Integer(min=0, description="Book view"),
    'vote': fields.Integer(min=0, description="Book vote"),
    'download': fields.Integer(min=0, description="Book download")
})

class authors(server.db.Model):
    __tablename__ = 'authors'
    id = server.db.Column(server.db.Integer, primary_key=True)
    firstname = server.db.Column(server.db.String(50))
    lastname = server.db.Column(server.db.String(50))
    email = server.db.Column(server.db.String(100))
    phone = server.db.Column(server.db.String(20))
    address = server.db.Column(server.db.String(100))
    status = server.db.Column(server.db.String(200))
    created = server.db.Column(server.db.String(100))
    updated = server.db.Column(server.db.String(100))

    book = server.db.relationship('books', backref='authors', lazy=True)


class books(server.db.Model):
    __tablename__ = 'books'
    id = server.db.Column(server.db.Integer, primary_key=True)
    title = server.db.Column(server.db.String(100))
    isbn = server.db.Column(server.db.String(10))
    year = server.db.Column(server.db.Integer)
    author_id = server.db.Column(server.db.Integer, server.db.ForeignKey('authors.id'), nullable=False)
    status = server.db.Column(server.db.String(200))
    created = server.db.Column(server.db.String(100))
    updated = server.db.Column(server.db.String(100))
    view = server.db.Column(server.db.Integer)
    vote = server.db.Column(server.db.Integer)
    download = server.db.Column(server.db.Integer)

    def __repr__(self):
        return '<Book %r>' % self.title