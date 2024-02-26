from fastapi import FastAPI,status
from fastapi.responses import JSONResponse

from pydantic import BaseModel
import os

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


@app.post("/https2mqtts/")
async def create_item(item: Item):
    if str(TOKEN) == str(item.token):
        stream = os.popen(f'mqtt publish -V 3 -h {URL} -p {PORT} -t "{item.topic}" -u {USER} -pw {PASSWORD} -m "{item.message}" -d --capath /etc/ssl/certs')
        #output = stream.read()
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"MQTT: msg transmitted to {item.topic}")
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="MQTT: invalid token")