from flask import render_template, request, json
from json.decoder import JSONDecodeError
from app import app


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")


@app.route("/sensor-data/<greenhouse_id>", methods=["POST"])
def receive_sensor_data(greenhouse_id):

    print(greenhouse_id)

    if request.is_json:
        # Access the raw data from the POST request
        raw_data = request.data
        # Decode the byte string to a regular string
        data_string = raw_data.decode("utf-8")
        try:
            # deserializing string
            data_dict = json.loads(data_string)
            print(data_dict)

            ntc_temp = data_dict.get("ntc_temp")
            ldr_lux = data_dict.get("ldr_lux")
            dht_temp = data_dict.get("dht_temp")
            dht_humidity = data_dict.get("dht_humidity")

        except JSONDecodeError as e:
            print(f"JSON decoding failed: {e}")
        except TypeError as e:
            print(f"TypeError occurred: {e}")
        return "ok", 200

    return "Invalid request", 400
