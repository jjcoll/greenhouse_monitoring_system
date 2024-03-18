from flask import render_template, request, json, jsonify
from json.decoder import JSONDecodeError
from app.models import GreenhouseSensorData
from app import app, db


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")


@app.route("/sensor-data/<greenhouse_id>/<sensor_id>", methods=["POST"])
def receive_sensor_data(greenhouse_id, sensor_id):

    # print(greenhouse_id)

    if request.is_json:
        # Access the raw data from the POST request
        raw_data = request.data
        # print(raw_data)
        try:
            # print(greenhouse_id, sensor_id)
            # Decode the byte string to a regular string
            data_string = raw_data.decode("utf-8")
            # deserializing string
            data_dict = json.loads(data_string)
            # print(data_dict)

            ntc_temp = data_dict.get("ntc_temp")
            ldr_lux = data_dict.get("ldr_lux")
            dht_temp = data_dict.get("dht_temp")
            dht_humidity = data_dict.get("dht_humidity")

            if dht_humidity == "-1" or dht_temp == "-1":
                raise ValueError("Invalid readings for DHT sensor")

            # adding data to database
            data_to_add = GreenhouseSensorData(
                gh_id=greenhouse_id,
                sensor_id=sensor_id,
                dht_temp=dht_temp,
                dht_humidity=dht_humidity,
                ldr_lux=ldr_lux,
                ntc_temp=ntc_temp,
            )

            db.session.add(data_to_add)
            db.session.commit()
            return "ok", 200

        except JSONDecodeError as e:
            print(f"JSON decoding failed: {e}")
            return "Bad request, did not recieve expected JSON data", 400
        except ValueError as e:
            print(f"Value Error: {e}")
            return "Bad request, did not recieve expected JSON data", 400
        # except:
        #     print(f"Error occurred")
        #     return "Bad request, did not recieve expected JSON data", 400

    return "Invalid request", 400


@app.route("/get-sensor-data/<greenhouse_id>/<sensor_id>", methods=["GET"])
def get_sensor_data(greenhouse_id, sensor_id):
    latest_record = (
        GreenhouseSensorData.query.filter_by(gh_id=greenhouse_id, sensor_id=sensor_id)
        .order_by(GreenhouseSensorData.date.desc())
        .first()
    )

    print(f"record: {latest_record.dht_temp}")

    if latest_record:
        temp = latest_record.dht_temp
        humidity = latest_record.dht_humidity

        if temp < 20 or temp > 30 or humidity < 30 or humidity > 40:
            in_range = False
        else:
            in_range = True
        return jsonify({"display": in_range}), 200
    else:
        return jsonify({"error": "No data found for the given ids"}), 400
