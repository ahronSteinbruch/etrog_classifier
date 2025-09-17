import json

import pymongo
import uuid

class MongoLoad:
    def __init__(self,db,collection):
        try:
            self.mongodb = pymongo.MongoClient("mongodb://localhost:27017")
            self.db = self.mongodb[db]
            self.collection = self.db[collection]
            print('All connected to mongoDB')
        except Exception as e:
            self.mongodb = None
            print(f'error__init__:{e}')


    def etrog_initialise(self,initial_dic):
        if self.mongodb:
            try:
                dic = initial_dic
                dic['_id'] = str(uuid.uuid4())
                dic['status'] = 'in-progress'
                dic['response'] = '🤌🤌🤌🤌🤌🤌'
                self.collection.insert_one(dic)
                print('Added initial record to mongoDB')
                return dic['_id']
            except Exception as e:
                print(f'error_etrog_initialise:{e}')
                return None
        else:
            print('Not connected to DB')
            return None

    def get_answer(self,id):
        if self.mongodb:
            try:
                record = self.collection.find_one({'_id':id})
                if record:
                    print('Record found')
                    return {'status':record['status'],
                              'response':record['response']}
                else:
                    print('ID not found')
                    return {'error': 'ID not found'}
            except Exception as e:
                print(f'error_get_answer:{e}')
                return {'error': str(e)}
        else:
            print('Database not available')
            return {'error': 'Database not available'}


    def update(self,id,status,quality):
        if self.mongodb:
            try:
                new_value = {'$set': {'status':status,'response':quality}}
                self.collection.update_one({'_id': id}, new_value)
                print('Record updated')
                return True
            except Exception as e:
                print(f'error_update:{e}')
                return False
        else:
            print('Database not available')
            return False

    def close(self):
        if self.mongodb:
            self.mongodb.close()
            print('Mongo closed')




