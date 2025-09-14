import pymongo
import uuid

class MongoLoad:
    def __init__(self,db,collection):
        self.mongodb = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.mongodb[db]
        self.collection = self.db[collection]

    def etrog_initialise(self,initial_dic):
        dic = initial_dic
        dic['_id'] = str(uuid.uuid4())
        dic['status'] = 'in-progress'
        dic['response'] = '🤌🤌🤌🤌🤌🤌'
        self.collection.insert_one(dic)
        return dic['_id']

    def get_answer(self,id):
        full_data = self.collection.find_one({'_id':id})
        answer = {'status':full_data['status'],
                  'response':full_data['response']}
        return answer






