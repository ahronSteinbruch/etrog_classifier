import pymongo
import uuid

class MongoLoad:
    def __init__(self,db,collection):
        try:
            # Connect to mongo
            # Receives db:str, collection:str
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
                # Create document
                # Receives initial_dic: dict (pic,variety)
                # Returns id:str (None if issued)
                dic = initial_dic
                dic['_id'] = str(uuid.uuid4())
                dic['status'] = 'in-progress'
                dic['grade'] = '🤌🤌🤌🤌🤌🤌'
                self.collection.insert_one(dic)
                print('Added initial record to mongoDB')
                return dic['_id']
            except Exception as e:
                print(f'error_etrog_initialise:{e}')
                return None
        else:
            print('Not connected to DB')
            return None

    def get_answer(self,job_id):
        if self.mongodb:
            # Response when ready
            # Receives id:str
            # Returns dictionary of status and response (or error)
            try:
                record = self.collection.find_one({'_id': job_id})
                if record:
                    print('Record found')
                    return {'status': record['status'],
                            'grade': record['grade']}
                else:
                    print('ID not found')
                    return {'error': 'ID not found'}
            except Exception as e:
                print(f'error_get_answer:{e}')
                return {'error': str(e)}
        else:
            print('Database not available')
            return {'error': 'Database not available'}


    def update(self,id,status,grade):
        if self.mongodb:
            # Updates document
            # Receives id:str, status:str, quality:str
            # Returns bool
            try:
                new_value = {'$set': {'status': status,'grade': grade}}
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
            # Closes connection
            self.mongodb.close()
            print('Mongo closed')



