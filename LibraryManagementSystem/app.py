from flask import Flask, flash, session, render_template,request, make_response
from flask_cors import CORS
import bson
from models import LMS
from database.database import db


app = Flask(__name__)
CORS(app)
app.secret_key = "mykey"

@app.route('/')
def index():
    active_section="signup_page"
    return render_template("index.html",active_section=active_section)

@app.route('/signup_page',methods=['POST','GET'])
def signup_page():
    active_section="signup_page"
    return render_template("index.html",active_section=active_section)

@app.route('/signin_page',methods=['POST','GET'])
def signin_page():
    active_section="signin_page"
    return render_template("index.html",active_section=active_section)

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        result=request.form.to_dict()
        new_user=LMS.addUser(result)
        if new_user:
            flash("Already have an account!!", "error")
            active_section="signup_page"
            return render_template("index.html",active_section=active_section)
        active_section="signin_page"
        print('result-->>',result)
    return render_template("index.html",active_section=active_section)

@app.route('/signin',methods=['POST','GET'])
def signin():
    access_level=''
    access_level_email=''
    if request.method=='POST':
        result=request.form.to_dict()
        login_user=LMS.loginUser(result)
        print('login_user data',login_user)
        if login_user==False:
            flash("The email or password is incorrect !!", "error")
            active_section="signin_page"
            return render_template("index.html",active_section=active_section)
        access_level=login_user[0].get('inputRole')
        access_level_email=login_user[0].get('inputEmail')
        session['user']=access_level_email
        if access_level=='admin':
            if 'user' not in session:    
                return render_template("index.html",active_section="signin_page")
            admin_active_section='admin_view_books'
            show_all_books=LMS.show_all_books()
            return render_template("admin.html",access_level=access_level,admin_active_section=admin_active_section,
                                   show_all_books=show_all_books,access_level_email=access_level_email)
    user_active_section='user_view_books'
    show_all_books=LMS.show_all_books()
    return render_template("user.html",access_level=access_level,access_level_email=access_level_email,
                           user_active_section=user_active_section,show_all_books=show_all_books)

@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('user',None)
    active_section="signin_page"
    return render_template("index.html",active_section=active_section)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/admin_add_book/<access_level_email>',methods=['POST','GET'])
def admin_add_book(access_level_email):
    if 'user' not in session:
        return render_template("index.html",active_section="signin_page")
    admin_active_section='admin_add_book'
    access_level='admin'
    access_level_email=access_level_email
    return render_template("admin.html",access_level=access_level,admin_active_section=admin_active_section,
                           access_level_email=access_level_email)

@app.route('/admin_view_books/<access_level_email>',methods=['POST','GET'])
def admin_view_books(access_level_email):
    if 'user' not in session:
        return render_template("index.html",active_section="signin_page")
    admin_active_section='admin_view_books'
    access_level='admin'
    access_level_email=access_level_email
    show_all_books=LMS.show_all_books()
    return render_template("admin.html",access_level=access_level,admin_active_section=admin_active_section,
                           show_all_books=show_all_books,access_level_email=access_level_email)

@app.route('/adminAddBook/<access_level_email>',methods=['POST','GET'])
def adminAddBook(access_level_email):
    if 'user' not in session:     
        return render_template("index.html",active_section="signin_page")
    
    result=request.form.to_dict()
    new_book=LMS.adminAddBook(result)
    admin_active_section='admin_view_books'
    access_level='admin'
    access_level_email=access_level_email
    show_all_books=LMS.show_all_books()
    return render_template("admin.html",access_level=access_level,admin_active_section=admin_active_section,
                           access_level_email=access_level_email,show_all_books=show_all_books)



@app.route('/adminEditBook/<book_id>/<access_level_email>',methods=['POST','GET'])
def adminEditBook(book_id,access_level_email):
    if 'user' not in session:
        return render_template("index.html",active_section="signin_page")
    edit_book_data=LMS.adminEditBook(book_id)
    access_level='admin'
    access_level_email=access_level_email
    return render_template("adminEditBook.html",access_level=access_level,edit_book_data=edit_book_data,
                           access_level_email=access_level_email)

@app.route('/adminUpdatedBook/<book_id>/<access_level>/<access_level_email>',methods=['POST','GET'])
def adminUpdatedBook(book_id,access_level,access_level_email):
    if 'user' not in session:    
        return render_template("index.html",active_section="signin_page")
    if request.method=='POST':
        result=request.form.to_dict()
        print('update result', result)
        updated_book=db.admin_addBook.update_one({'_id':bson.ObjectId(book_id)},
                                                 {"$set" :
                                                        {
                                                            'inputTitle':result.get('inputTitle'),
                                                            'inputAuthor':result.get('inputAuthor'),
                                                            'inputGenre': result.get('inputGenre'),
                                                            'inputCopies':result.get('inputCopies')
                                                        }
                                                })
        
        
        
        access_level='admin'
        access_level_email=access_level_email
        print('access_level_email',access_level_email)
    admin_active_section='admin_view_books'
    show_all_books=LMS.show_all_books()
    return render_template("admin.html",access_level=access_level,admin_active_section=admin_active_section,
                           show_all_books=show_all_books,access_level_email=access_level_email)

@app.route('/admin_checkRented_book/<access_level_email>')
def admin_checkRented_book(access_level_email):
    if 'user' not in session:    
        return render_template("index.html",active_section="signin_page")
    show_rented_books=LMS.admin_checked_books()
    admin_active_section='admin_checkRented_book'
    access_level_email=access_level_email
    access_level='admin'
    return render_template('admin.html',admin_active_section=admin_active_section,show_rented_books=show_rented_books,
                           access_level_email=access_level_email,access_level=access_level)

@app.route('/adminSelectCategory/<access_level_email>',methods=['POST','GET'])
def adminSelectCategory(access_level_email):
    if 'user' not in session:
        return render_template("index.html",active_section="signin_page")
    result=request.form.to_dict()
    show_all_books=LMS.filter_book(result)
    admin_active_section='admin_view_books'
    access_level='admin'
    access_level_email=access_level_email
    return render_template("admin.html",access_level=access_level,admin_active_section=admin_active_section,
                           show_all_books=show_all_books,access_level_email=access_level_email)
    

@app.route('/adminRecieveBook/<book_id>/<access_level_email>',methods=['POST','GET'])
def adminRecieveBook(book_id,access_level_email):
    if 'user' not in session:
        return render_template("index.html",active_section="signin_page")
    show_rented_books=LMS.admin_recieve_book(book_id)
    admin_active_section='admin_checkRented_book'
    access_level_email=access_level_email
    access_level='admin'
    return render_template('admin.html',admin_active_section=admin_active_section,show_rented_books=show_rented_books,
                           access_level_email=access_level_email,access_level=access_level)



@app.route('/user_view_books/<access_level_email>',methods=['POST','GET'])
def user_view_books(access_level_email):
    if 'user' not in session:
        return render_template("index.html",active_section="signin_page")
    user_active_section='user_view_books'
    access_level='member'
    show_all_books=LMS.show_all_books()
    access_level_email=access_level_email
    return render_template("user.html",access_level=access_level,user_active_section=user_active_section,
                           show_all_books=show_all_books,access_level_email=access_level_email)


@app.route('/userRentBook/<book_id>/<access_level_email>',methods=['POST','GET'])
def userRentBook(book_id,access_level_email):
    if 'user' not in session:
        return render_template("index.html",active_section="signin_page")
    print(book_id,access_level_email)
    rent_book_data=LMS.userRentBook(book_id)
    return render_template('userRentBook.html',rent_book_data=rent_book_data,access_level_email=access_level_email)

@app.route('/rentedBookShelf/<book_id>/<access_level_email>',methods=['POST','GET'])
def rentedBookShelf(book_id,access_level_email):
    if 'user' not in session:
        return render_template("index.html",active_section="signin_page")
    
    result=request.form.to_dict()
    show_all_books=LMS.rented_book_shelf(book_id,access_level_email,result)
    user_active_section='user_view_books'
    access_level_email=access_level_email
    access_level='member'
    return render_template("user.html",access_level=access_level,access_level_email=access_level_email,
                           user_active_section=user_active_section,show_all_books=show_all_books)

@app.route('/user_book_shelf/<access_level_email>',methods=['POST','GET'])
def user_book_shelf(access_level_email):
    if 'user' not in session:
        return render_template("index.html",active_section="signin_page")
    perosnal_shelf=LMS.user_personal_bookShelf(access_level_email)
    user_active_section='user_book_shelf'
    access_level_email=access_level_email
    access_level='member'
    return render_template('user.html',access_level=access_level,access_level_email=access_level_email,
                           user_active_section=user_active_section,perosnal_shelf=perosnal_shelf)

@app.route('/userSelectCategory/<access_level_email>',methods=['POST','GET'])
def userSelectCategory(access_level_email):
    if 'user' not in session:
        return render_template("index.html",active_section="signin_page")
    result=request.form.to_dict()
    show_all_books=LMS.filter_book(result)
    user_active_section='user_view_books'
    access_level='member'
    access_level_email=access_level_email
    return render_template("user.html",access_level=access_level,user_active_section=user_active_section,
                           show_all_books=show_all_books,access_level_email=access_level_email)


@app.route('/userReturnBook/<book_id>/<access_level_email>',methods=['POST','GET'])
def userReturnBook(book_id,access_level_email):
    if 'user' not in session:  
        return render_template("index.html",active_section="signin_page")
    perosnal_shelf=LMS.user_return_book(book_id,access_level_email)
    user_active_section='user_book_shelf'
    access_level_email=access_level_email
    access_level='member'
    return render_template('user.html',user_active_section=user_active_section,perosnal_shelf=perosnal_shelf,
                           access_level_email=access_level_email,access_level=access_level)


if __name__=="__main__":
    app.run(debug=True)