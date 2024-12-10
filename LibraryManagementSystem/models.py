import bson
from flask import jsonify
from database.database import db
import datetime

class LMS:
    def __init__():
        return 
    
    def addUser(user):
        print('db-->',db)
        print('models user',user)
        if db.users.find_one({'inputEmail':user.get('inputEmail')}):
            print('yes',db.users.find({'inputEmail':user.get('inputEmail')}))
            return True
        new_user=db.users.insert_one({
            'inputName':user.get('inputName'),
            'inputEmail':user.get('inputEmail'),
            'inputPassword': user.get('inputPassword'),
            'inputRole':user.get('inputRole')

        })
        return False
    
    def loginUser(user):
        if db.users.find_one({'inputEmail':user.get('inputEmail'),'inputPassword': user.get('inputPassword')}):
            data=db.users.find({'inputEmail':user.get('inputEmail'),'inputPassword': user.get('inputPassword')})
            user_data=[{**user,"_id":str(user['_id'])} for user in data]
            print('yes',user_data)
            return user_data
            
        return False
    

    def filter_book(selectCategory):
        filtered_book=''
        filtered_book_data=''
        print('selectCategory',selectCategory)
        if selectCategory.get('inputCategory')=='all_books' and selectCategory.get('inputData')=="":
            filtered_book_data=db.admin_addBook.find()
        else:
            filtered_book_data=db.admin_addBook.find({
                selectCategory.get('inputCategory') : selectCategory.get('inputData')
            })
        filtered_book=filtered_book_data
        select_filtered_book=[{**book,'_id':str(book['_id'])} for book in filtered_book]
        print('select_filtered_book',select_filtered_book)
        return select_filtered_book



    def adminAddBook(book):
        new_book=db.admin_addBook.insert_one({
            'inputTitle': book.get('inputTitle'),
            'inputAuthor': book.get('inputAuthor'),
            'inputGenre':book.get('inputGenre'),
            'inputCopies':book.get('inputCopies')
        })
        return new_book
    
    def show_all_books():
        show_books=db.admin_addBook.find()
        show_all_books=[{**book,'_id':str(book['_id'])} for book in show_books]
        return show_all_books
    
    def adminEditBook(book_id):
        find_book=db.admin_addBook.find({'_id':bson.ObjectId(book_id)})
        show_find_book=[{**book,'_id':str(book['_id'])} for book in find_book]
        return show_find_book
    
    def admin_checked_books():
        rented_book_data=db.rented_bookShelf.find()
        rented_books=[{**book,'_id':str(book['_id'])} for book in rented_book_data]
        return rented_books
    
    def admin_recieve_book(book_id):
        data=db.rented_bookShelf.find({'_id':bson.ObjectId(book_id)})
        recieve_book_data=[{**book,'_id':str(book['_id'])} for book in data]
        print('recieve_book_data',recieve_book_data)
        book_previous_data=db.admin_addBook.find({'inputTitle':recieve_book_data[0].get('inputTitle'),
                                                  'inputAuthor': recieve_book_data[0].get('inputAuthor'),
                                                   'inputGenre':  recieve_book_data[0].get('inputGenre')})
        show_book_data=[{**book,'_id':str(book['_id'])} for book in book_previous_data]
        previous_copies=show_book_data[0].get('inputCopies')
        update_books=db.admin_addBook.update_one({'inputTitle':recieve_book_data[0].get('inputTitle'),
                                                  'inputAuthor': recieve_book_data[0].get('inputAuthor'),
                                                   'inputGenre':  recieve_book_data[0].get('inputGenre')},
                                                   {"$set":{
                                                       'inputCopies': str(int(previous_copies) + int(recieve_book_data[0].get('inputCopies')))
                                                   }
                                                    })
        received_book=db.rented_bookShelf.delete_one({'_id':bson.ObjectId(book_id)})
        return LMS.admin_checked_books()

    
    def userRentBook(book_id):
        find_book=db.admin_addBook.find({'_id':bson.ObjectId(book_id)})
        show_find_book=[{**book,'_id':str(book['_id'])} for book in find_book]
        return show_find_book
    
    def rented_book_shelf(book_id,user_email,result):
        date=str(datetime.date.today())
        book_previous_data=db.admin_addBook.find({'_id':bson.ObjectId(book_id)})
        show_book_data=[{**book,'_id':str(book['_id'])} for book in book_previous_data]
        previous_copies=show_book_data[0].get('inputCopies')
        update_book_copies=db.admin_addBook.update_one({'_id':bson.ObjectId(book_id)},
                                                 {"$set" :
                                                        {
                                                            'inputCopies': str(int(previous_copies) - int(result.get('inputCopies')))
                                                        }
                                                })
        data=db.rented_bookShelf.insert_one({
            'inputTitle': show_book_data[0].get('inputTitle'),
           'inputAuthor': show_book_data[0].get('inputAuthor'),
            'inputGenre': show_book_data[0].get('inputGenre'),
            'inputCopies':result.get('inputCopies'),
            'inputDays': result.get('inputDays'),
            'userEmail': user_email,
            'issueDate': date
        })
        return LMS.show_all_books()
    
    def user_personal_bookShelf(user_email):
        shelf=db.rented_bookShelf.find({'userEmail': user_email})
        personal_book_shelf=[{**book,'_id':str(book['_id'])} for book in shelf]
        print('personal_book_shelf',personal_book_shelf)
        return personal_book_shelf
    
    def user_return_book(book_id,user_email):
        data=db.rented_bookShelf.find({'_id':bson.ObjectId(book_id)})
        recieve_book_data=[{**book,'_id':str(book['_id'])} for book in data]
        print('recieve_book_data',recieve_book_data)
        book_previous_data=db.admin_addBook.find({'inputTitle':recieve_book_data[0].get('inputTitle'),
                                                  'inputAuthor': recieve_book_data[0].get('inputAuthor'),
                                                   'inputGenre':  recieve_book_data[0].get('inputGenre')})
        show_book_data=[{**book,'_id':str(book['_id'])} for book in book_previous_data]
        previous_copies=show_book_data[0].get('inputCopies')
        update_books=db.admin_addBook.update_one({'inputTitle':recieve_book_data[0].get('inputTitle'),
                                                  'inputAuthor': recieve_book_data[0].get('inputAuthor'),
                                                   'inputGenre':  recieve_book_data[0].get('inputGenre')},
                                                   {"$set":{
                                                       'inputCopies': str(int(previous_copies) + int(recieve_book_data[0].get('inputCopies')))
                                                   }
                                                    })
        received_book=db.rented_bookShelf.delete_one({'_id':bson.ObjectId(book_id)})
        user_rented_book_data=db.rented_bookShelf.find({'userEmail':user_email})
        user_personal_rented_books=[{**book,'_id':str(book['_id'])} for book in user_rented_book_data]
        
        return user_personal_rented_books







        
        