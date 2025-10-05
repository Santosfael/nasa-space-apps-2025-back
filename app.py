from flask import Flask, request, jsonify
from flask_cors import CORS
import service
import logging

app = Flask(__name__)
CORS(app)

# --- ROTAS DE TEMPERATURA ---
@app.route('/temperature/daily-probability', methods=['GET'])
def get_temperature_daily_probability():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    date_param = request.args.get('date')
    if not all([lat, lon, date_param]): 
        return jsonify({"error": "Parameters 'lat', 'lon', 'date' are required."}), 400

    result, city_name = service.get_daily_temperature_analysis(lat, lon, date_param)
    
    if result and "error" in result: 
        return jsonify(result), 404
    return jsonify({"data_source_location": city_name, "analysis": result})

@app.route('/temperature/hourly-probability', methods=['GET'])
def get_temperature_hourly_probability():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    date_param = request.args.get('date')
    hour_param = request.args.get('hour')
    if not all([lat, lon, date_param, hour_param]):
        return jsonify({"error": "All parameters for hourly temperature are required."}), 400
    
    result, city_name = service.get_temperature_hourly_analysis(lat, lon, date_param, hour_param)
    
    if result and "error" in result: 
        return jsonify(result), 404
    return jsonify({"data_source_location": city_name, "analysis": result})


@app.route('/precipitation/daily-probability', methods=['GET'])
def get_precipitation_daily_probability():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    date_param = request.args.get('date')
    if not all([lat, lon, date_param]): 
        return jsonify({"error": "Parameters 'lat', 'lon', 'date' are required."}), 400

    result, city_name = service.get_precipitation_daily_analysis(lat, lon, date_param)
    
    if result and "error" in result: 
        return jsonify(result), 404
    return jsonify({"data_source_location": city_name, "analysis": result})

@app.route('/precipitation/hourly-probability', methods=['GET'])
def get_precipitation_hourly_probability():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    date_param = request.args.get('date')
    hour_param = request.args.get('hour')
    if not all([lat, lon, date_param, hour_param]):
        return jsonify({"error": "All parameters for hourly precipitation are required."}), 400

    result, city_name = service.get_precipitation_hourly_analysis(lat, lon, date_param, hour_param)

    if result and "error" in result: 
        return jsonify(result), 404
    return jsonify({"data_source_location": city_name, "analysis": result})

@app.route('/humidity/daily-probability', methods=['GET'])
def get_humidity_daily_probability():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    date_param = request.args.get('date')
    if not all([lat, lon, date_param]): 
        return jsonify({"error": "Parameters 'lat', 'lon', 'date' are required."}), 400

    result, city_name = service.get_humidity_daily_analysis(lat, lon, date_param)
    
    if result and "error" in result: 
        return jsonify(result), 404
    return jsonify({"data_source_location": city_name, "analysis": result})

@app.route('/humidity/hourly-probability', methods=['GET'])
def get_humidity_hourly_probability():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    date_param = request.args.get('date')
    hour_param = request.args.get('hour')
    if not all([lat, lon, date_param, hour_param]):
        return jsonify({"error": "All parameters for hourly humidity are required."}), 400

    result, city_name = service.get_humidity_hourly_analysis(lat, lon, date_param, hour_param)

    if result and "error" in result: 
        return jsonify(result), 404
    return jsonify({"data_source_location": city_name, "analysis": result})

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)