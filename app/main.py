from fastapi import FastAPI,status
from fastapi.responses import JSONResponse

from pydantic import BaseModel
import os

USER = os.getenv('MQTT_USER')
PASSWORD = os.environ.get('MQTT_PASSWORD')
URL = os.environ.get('MQTT_URL')
PORT = os.environ.get('MQTT_PORT')

class Item(BaseModel):
    topic: str
    message: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "topic": "testtopic/1",
                    "message": "Hello World"
                }
            ]
        }
    }

app = FastAPI()


@app.post("/https2mqtts/")
async def create_item(item: Item):
    
    stream = os.popen(f'mqtt publish -V 3 -h {URL} -p {PORT} -t "{item.topic}" -u {USER} -pw {PASSWORD} -m "{item.message}" -d --capath /etc/ssl/certs')
    #output = stream.read()
    return JSONResponse(status_code=status.HTTP_200_OK, content=f"MQTT: msg transmitted to {item.topic}")
