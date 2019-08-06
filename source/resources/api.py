from flask import *
from flask_restplus import *
from source.models.base import books, book, authors, author
from source.server.instance import server
from sqlalchemy import *
from source.helpers.convert import *
from source.helpers.valid import *

@server.ns.route('/authors')
@server.ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
class authorList(Resource):
    '''Shows a list of all authors, and lets you POST to add new tasks'''
    #@server.ns.marshal_list_with(author)
    @server.ns.doc('get all authors')
    def get(self):
        '''List all authors'''
        bookCount = server.db.session.query(books.author_id, func.count(books.id)).group_by(books.author_id).all()
        highestVote = server.db.session.query(authors.id, books.isbn, books.title, books.vote).filter(books.author_id == authors.id).group_by(books.author_id).having(func.max(books.vote)).all()

        lst = server.db.session.query(authors).all()
        tup = []
        for row in lst:
            dict = ConvertToDict(row)
            bCount = 0
            isbn = title = ""
            for cnt in bookCount:
                if cnt[0] == row.id:
                    bCount = cnt[1]
                    break

            for vote in highestVote:
                if vote[0] == row.id:
                    title = vote[1]
                    isbn = vote[2]
                    break


            dict['bookCount'] = bCount
            dict['isbn'] = isbn
            dict['title'] = title
            tup.append(dict)

        return tup

    @server.ns.doc('add new author')
    @server.ns.expect(author)
    #@server.ns.marshal_list_with(author)
    def post(self):
        '''Add an author'''
        data = server.api.payload
        if invalid_author(data['email'], data['phone']):
            server.server.ns.abort(400)

        data_query = server.db.session.query(authors).order_by(authors.id.desc()).first()
        if data_query is not None:
            cnt = data_query.id
        else:
            cnt = 0
        newauthor = authors(id=cnt+1, firstname=data['firstname'], lastname=data['lastname'],
                         email=data['email'], phone=data['phone'],
                         address=data['address'], status=data['status'],
                         created=data['created'], updated=data['updated'])
        server.db.session.add(newauthor)
        server.db.session.commit()
        return data

@server.ns.route('/books')
@server.ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
class bookList(Resource):

    @server.ns.doc('Get all books')
    def get(self):
        '''List all books'''
        lst = server.db.session.query(books).all()
        tup = []
        for row in lst:
            tup.append(ConvertToDict(row))

        return tup

    @server.ns.doc('Add new book')
    @server.ns.expect(book)
    def post(self):
        '''Add a new book'''
        data = server.api.payload
        if invalid_book(data['isbn'], data['year']):
            server.server.ns.abort(400)

        data_query = server.db.session.query(books).order_by(books.id.desc()).first()
        if data_query is not None:
            cnt = data_query.id
        else:
            cnt = 0
        newbook = books(id=cnt+1, title=data['title'], isbn=data['isbn'], year=data['year'],
                     author_id=data['author_id'], status=data['status'],
                     created=data['created'], updated=data['updated'],
                     view=data['view'], vote=data['vote'], download=data['download'])
        server.db.session.add(newbook)
        server.db.session.commit()
        return data


@server.ns.route('/books/<int:id>')
@server.ns.param('id', 'Specify the ID associated with book')
@server.ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
            params={'id': 'Specify the Id associated with book'})
class bookListItem(Resource):

    @server.ns.doc('get book with ID')
    def get(self, id):
        '''Get book with given ID '''
        try:
            book = server.db.session.query(books).filter(books.id == id).one()
            return ConvertToDict(book)
        except:
            server.ns.abort(400)

    @server.ns.doc('delete book')
    def delete(self, id):
        '''Delete book with given ID'''
        try:
            books.query.filter_by(id=id).delete()
            server.db.session.commit()
        except:
            server.ns.abort(400)

    @server.ns.doc('update book with id')
    @server.ns.expect(book)
    def put(self, id):
        '''Update a book with given ID'''
        try:
            data = server.api.payload
            updatebook = books.query.filter_by(id=id).first()
            updatebook.year = data['year']
            updatebook.status = data['status']
            updatebook.updated = datetime.now()
            updatebook.view = data['view']
            updatebook.vote = data['vote']
            updatebook.download = data['download']
            server.db.session.commit()
        except:
            server.ns.abort(400)


@server.ns.route('/books/search')
@server.ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
@server.ns.param('isbn', 'Specify the ISBN associated with book')
@server.ns.param('title', 'Specify the title associated with book')
class BookSearch(Resource):

    def get(self):
        '''Search book with ISBN and/or title'''
        isbn = title = ""
        if 'isbn' in request.args:
            isbn = request.args.get('isbn')
        if 'title' in request.args:
            title = request.args.get('title')
        tup = []

        if isbn == "" and title == "":
            return tup
        elif isbn == "":
            lst = server.db.session.query(books).filter(books.title.contains(title)).all()
        elif title == "":
            lst = server.db.session.query(books).filter(books.isbn == isbn).all()
        else:
            lst = server.db.session.query(books).filter(books.title.contains(title)).filter(books.isbn == isbn).all()

        for row in lst:
            tup.append(ConvertToDict(row))

        return tup