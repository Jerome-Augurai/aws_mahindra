import random
import time
import datetime
from fastapi import FastAPI, Query, BackgroundTasks
from typing import List
import uvicorn

app = FastAPI()

@app.get("/iotgateway/read/")
async def read_data(ids: List[str] = Query(...)):
    # Process the data for the provided IDs
    json_response = {'readResults':[]}
    for element  in ids:
        triger_res = {}
        triger_res['id'] = str(element)
        triger_res['s'] = True
        triger_res['r'] = ''
        v = random.choices([False, True], weights=[0.9, 0.1])[0]
        print(f"value of v:{v}")
        triger_res['v'] = v
        #triger_res['v'] = random.choice([True, False]) 
        triger_res['t'] = int(time.time())
        json_response['readResults'].append(triger_res)
    return json_response

if __name__ == '__main__':
    uvicorn.run(app)