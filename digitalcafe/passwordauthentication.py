import pymongo
import database as db

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]

order_management_db = myclient["order_management"]

def editpassword(password):
    is_valid_password = False
    passwordname=None
    temp_password = db.get_password(password)
    if(temp_password != None):
        if(temp_password["password"]==password):
            is_valid_password = True
            passwordname={"password":temp_password["password"]}
    return is_valid_password,passwordname
