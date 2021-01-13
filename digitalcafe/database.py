import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]

order_management_db = myclient["order_management"]

def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user

def get_password(password):
    customers_coll = order_management_db['customers']
    password=customers_coll.find_one({"password":password})
    return password

def get_product(code):
    products_coll = products_db["products"]
    product = products_coll.find_one({"code":code})
    return product

def get_products():
    product_list = []
    products_coll = products_db["products"]
    for p in products_coll.find({}):
        product_list.append(p)
    return product_list

def get_branch(code):
    branches_coll = products_db['branches']
    branch = branches_coll.find_one({"code":code})
    return branch

def get_branches():
    branch_list=[]
    branches_coll = products_db['branches']
    for b in branches_coll.find({}):
        branch_list.append(b)
    return branch_list

def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)
