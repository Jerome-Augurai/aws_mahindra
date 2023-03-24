import random
import time
from fastapi import FastAPI, Query
from typing import List

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
        triger_res['v'] = random.choice([True, False]) 
        triger_res['t'] = int(time.time())
        json_response['readResults'].append(triger_res)
    return json_response