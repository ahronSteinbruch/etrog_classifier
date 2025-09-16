from fastapi import FastAPI , HTTPException
import uvicorn
import threading
from mongo import MongoLoad
from kafka_pub import Produce
from kafka_sub import Subscriber
from contextlib import asynccontextmanager
import json

mongo = MongoLoad('etrog_db','etrogim')
kafka_publish = Produce()

consumer_running = False
consumer_thread = None

def kafka_consumer():

    global consumer_running, consumer_thread

    if consumer_running:
        return

    def consume_results():
        kafka_subscribe = Subscriber('etrog_finished')
        consumer_running = True

        try:
            for message in kafka_subscribe.consumer:
                if consumer_running:
                    mongo.update(message.value['_id'],message.value['status'],message.value['response'])
                    print(f'Etrog with id:{message.value['_id']} updated')
                else:
                    break
        except Exception as e:
            print(f'error:{e}')
        finally:
            kafka_subscribe.close()
            print('Consumer closed')
            consumer_running = False

    consumer_thread = threading.Thread(target=consume_results, daemon=True)
    consumer_thread.start()


def stop_consumer():
    global consumer_running
    consumer_running = False


@asynccontextmanager
async def lifespan(app : FastAPI):
    kafka_consumer()
    print('Consumer Starting')

    yield

    stop_consumer()
    mongo.close()
    kafka_publish.close()
    print('All shutting down')



app = FastAPI(title="Etrog Classifier API",lifespan=lifespan)



@app.post('/input')
async def input_pic(input_dict):
    try:
        input_dict = json.loads(input_dict)
        record_id = mongo.etrog_initialise(input_dict)
        if record_id:
            publish = kafka_publish.publish_message('etrogim_to_process',{'_id':record_id,'picture':input_dict['pic']})
            if not publish:
                mongo.update(record_id,'failed','Failed to queue for processing')
        else:
            raise HTTPException(status_code=500, detail="Failed to create database record")
        return {'id':record_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/answer/{id}')
async def answer(id):
    try:
        result =  mongo.get_answer(id)
        if 'error' in result:
            raise HTTPException(status_code=404, detail=result['error'])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)



