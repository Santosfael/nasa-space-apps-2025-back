from flask import Flask, request, jsonify
from flask_cors import CORS
import service
import logging

app = Flask(__name__)
CORS(app)

@app.route('/daily-probability', methods=['GET'])
def get_daily_probability():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    date_param = request.args.get('date')

    if not all([lat, lon, date_param]):
        return jsonify({"error": "Parameters 'lat', 'lon', and 'date' are required."}), 400

    # Chama o service para fazer o trabalho
    result, city_name = service.get_daily_analysis(lat, lon, date_param)
    
    if "error" in result:
        return jsonify(result), 404
        
    final_response = {
        "data_source_location": city_name,
        "analysis": result
    }
    return jsonify(final_response)

@app.route('/hourly-probability', methods=['GET'])
def get_hourly_probability():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    date_param = request.args.get('date')
    hour_param = request.args.get('hour')

    if not all([lat, lon, date_param, hour_param]):
        return jsonify({"error": "Parameters 'lat', 'lon', 'date', and 'hour' are required."}), 400

    result, city_name = service.get_hourly_analysis(lat, lon, date_param, hour_param)
    
    if "error" in result:
        return jsonify(result), 404

    final_response = {
        "data_source_location": city_name,
        "analysis": result
    }
    return jsonify(final_response)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)