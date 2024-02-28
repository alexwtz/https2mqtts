from fastapi import FastAPI,status
from fastapi import Request
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Dict, Any
import os
import logging

logger = logging.getLogger(__name__)


USER = os.getenv('MQTT_USER')
PASSWORD = os.environ.get('MQTT_PASSWORD')
URL = os.environ.get('MQTT_URL')
PORT = os.environ.get('MQTT_PORT')
TOKEN = os.environ.get('API_TOKEN')

class Item(BaseModel):
    topic: str
    message: str
    token: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "topic": "testtopic/1",
                    "message": "Hello World",
                    "token": "token defined in .env"
                }
            ]
        }
    }

app = FastAPI()

@app.post("/dummypath")
async def get_body(request: Request):
    req = await request.body()
    logger.debug(f"{request.method} {request.url} ***  {req}")
    with open('output.txt', 'a') as f:
        f.write(f"{req}\n***\n")
    return req

@app.post("/https2mqtts/")
async def create_item(item: Item):
    if str(TOKEN) == str(item.token):
        stream = os.popen(f'mqtt publish -V 3 -h {URL} -p {PORT} -t "{item.topic}" -u {USER} -pw {PASSWORD} -m "{item.message}" -d --capath /etc/ssl/certs')
        #output = stream.read()
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"MQTT: msg transmitted to {item.topic}")
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="MQTT: invalid token")
