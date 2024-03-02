from fastapi import FastAPI,status
from fastapi import Request
from fastapi.responses import JSONResponse
from app.dragino import decode_body

from pydantic import BaseModel
from typing import Dict, Any
import os

USER = os.getenv('MQTT_USER')
PASSWORD = os.environ.get('MQTT_PASSWORD')
URL = os.environ.get('MQTT_URL')
PORT = os.environ.get('MQTT_PORT')
TOKEN = os.environ.get('API_TOKEN')

topic='office/sensor1'

app = FastAPI()

'''
@app.post("/dummypath")
async def get_body(request: Request):
    body = await request.body()
    
    with open('output.txt', 'a') as f:
        f.write(f"{req}\n***\n")
    return req
'''

@app.post("/https2mqtts")
async def get_body(request: Request):
    body = await request.body()
    if body is None:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="MQTT: no body")
    json_data=decode_body(body)
    if json_data:
        with open('output.txt', 'a') as f:
            f.write(f"{json_data}\n***\n")
        data = {
            "temperature":json_data['decoded']['TempC_SHT'],
            "humidity":json_data['decoded']['Hum_SHT']
        }
        cmd = f'''mqtt publish -V 3 -h {URL} -p {PORT} -t '{topic}' -u {USER} -pw {PASSWORD} 
		-m '\{"temperature":{json_data['decoded']['TempC_SHT']},"humidity":{json_data['decoded']['Hum_SHT']}\}' 
		-d --cafile ca-certificates.crt'''
        with open('output.txt', 'a') as f:
            f.write(f"cmd: {cmd}\n***\n")
        stream = os.popen(cmd)
        #output = stream.read()
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"MQTT: msg transmitted to {item.topic}")
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="MQTT: invalid json")
