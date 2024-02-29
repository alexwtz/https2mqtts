import base64
import json

Ext_sensor = {
         "0":"No external sensor",
         "1":"Temperature Sensor",
         "4":"Interrupt Sensor send",
         "5":"Illumination Sensor",
         "6":"ADC Sensor",
         "7":"Interrupt Sensor count",
       }

def decode_lht65(bytes):
    # Decode an uplink message from a buffer (array) of bytes to an object of fields.
    value = ((bytes[0] << 8) | bytes[1]) & 0x3FFF
    batV = value / 1000  # Battery voltage in units: V

    value = (bytes[2] << 8) | bytes[3]
    if bytes[2] & 0x80:
        value |= 0xFFFF0000
    temp_SHT = round(value / 100, 2)  # SHT20 temperature in units: °C

    value = (bytes[4] << 8) | bytes[5]
    hum_SHT = round(value / 10, 1)  # SHT20 humidity in units: %

    value = (bytes[7] << 8) | bytes[8]
    if bytes[7] & 0x80:
        value |= 0xFFFF0000
    temp_ds = round(value / 100, 2)  # DS18B20 temperature in units: °C

    ext_sensor = Ext_sensor.get(str(bytes[6]&0x7F))

    
    return {
        'BatV': batV,
        'TempC_DS': temp_ds,
        'TempC_SHT': temp_SHT,
        'Hum_SHT': hum_SHT,
        'Ext_sensor':ext_sensor
    }

def decode_body(body):
    if not body:
        # Decode the byte string to a regular string
        json_string = body.decode('utf-8')

        # Parse the JSON string into a Python dictionary
        json_data = json.loads(json_string)
        
        # Convert the base64-encoded string to bytes
        base64_string = json_data.get('payload')
        bytes_data = base64.b64decode(base64_string)
        json_data['decoded']= decode_lht65(bytes_data)
        return json_data
    return body

def main():
    body = b'{\n  "id": "c9ac2be0-357a-4432-a7f8-5b1991489a95",\n  "name": "Dragino LHT65",\n  "app_eui": "A000000000000101",\n  "dev_eui": "A840413BD182D3DC",\n  "devaddr": "11000048",\n  "downlink_url": "https://console.helium.com/api/v1/down/8bb0ff63-f6b1-43a6-9272-7145376ddb9f/zRFYJ40npC3K6EesgBAv9w0Nfz8B_SMF/c9ac2be0-357a-4432-a7f8-5b1991489a95",\n  "fcnt": "511",\n  "port": "2",\n  "payload": "y8QHKwJtAQcOf/8=",\n  "reported_at": "1709239250688"\n}'
    json_data=decode_body(body)
    print(json_data)

main()
