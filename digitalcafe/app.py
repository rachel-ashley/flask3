from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
import database as db
import authentication
import passwordauthentication
import logging
import ordermanagement as om
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]

order_management_db = myclient["order_management"]

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'


logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/editpassword', methods=['GET', 'POST'])
def editpassword():
    return render_template('editpassword.html')


@app.route('/passauth', methods = ['GET','POST'])
def passauth():
    password = request.form.get('password')
    is_successful, passwordname = passwordauthentication.editpassword(password)
    app.logger.info('%s',is_successful)
    if(is_successful):
        session["user"]["password"] = passwordname
        return redirect('/editpasswordpart2')
    else:
        return redirect('/editpassword')

@app.route('/editpasswordpart2', methods=['GET','POST'])
def editpasswordpart2():
    return render_template('editpasswordpart2.html')

@app.route('/changepass', methods = ['GET','POST'])
def changepass():
    customers_coll = order_management_db["customers"]
    is_same_password = False
    newpassword = request.form.get('newpassword')
    confirmpassword = request.form.get('confirmpassword')
    if(newpassword==confirmpassword):
        is_same_password = True
        filter = {"username":(session["user"]["username"])}
        updated_password = {"$set":{"password":newpassword}}
        customers_coll.update_one(filter,updated_password)
        return redirect('/')
    else:
        return "Passwords don't match."

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches", branch_list=branch_list, branches=branches)

@app.route('/branchesdetails')
def branchesdetails():
    code = request.args.get('code', '')
    branch = db.get_branch(code)
    return render_template('branchesdetails.html', branchesdetails = branchesdetails, code=code, branch=branch)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a
    # quantity of 1 for now

    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
    # clear cart in session memory upon checkout
    om.create_order_from_cart()
    session.pop("cart",None)
    return redirect('/ordercomplete')

@app.route('/ordercomplete')
def ordercomplete():
    return render_template('ordercomplete.html')

@app.route('/updateqty')
def updateqty():
    qty = request.form.get('qty')
    newqty = request.form.get('value')
    editedqty = {"$set": {qty:newqty}}
    qty.update(newqty)
    return redirect('/')

@app.route('/pastorders')
def pastorders():
    all_orders = order_management_db['orders']
    return render_template('/pastorders.html', all_orders=all_orders, pastorders=pastorders)
