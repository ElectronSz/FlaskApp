from pymongo import MongoClient
import pprint
import datetime

client = MongoClient('mongodb://localhost:27017/')

db = client.Api
cust = db['customers']

#find all customers
# curs = cust.find()
# for cu in curs:
#     #pass
#     print(cu)

#find one customer
print(cust.find({'_id', '5db5896e65d18824616570a1'}))

#insert one customer
# customer = {
#     'reg_date': datetime.datetime.utcnow(),
#     'fname': "Buhle",
#     'lname': "Mbhamali",
#     'age': 23,
#     'email': "buhle@fmail.com"
# }

# cust_id = cust.insert_one(customer)
#print(cust_id)