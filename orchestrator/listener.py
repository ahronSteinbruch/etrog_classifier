from fastapi import FastAPI
import uvicorn
from mongo import MongoLoad
from kafka_pub import Produce

app = FastAPI()
mongo = MongoLoad('db','etrogim')
kafka_publish = Produce()


@app.post('/input')
async def input_pic(input_dict):
    add = mongo.etrog_initialise(input_dict)
    kafka_publish.publish_message('etrogim',{'id':add,'picture':input_dict['pic']})
    return add

@app.get('/answer')
async def answer(id):
    return mongo.get_answer(id)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)