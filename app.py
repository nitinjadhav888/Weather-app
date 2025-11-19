from flask import Flask, request, jsonify
from models import predict_rain

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')

    if lat is None or lon is None:
        return jsonify({'error': 'Missing lat or lon'}), 400

    prob, mm = predict_rain(lat, lon)
    prediction = f"{prob*100:.0f}% chance of {mm:.1f}mm rain starting soon."

    return jsonify({
        'latitude': lat,
        'longitude': lon,
        'prediction': prediction
    })

if __name__ == '__main__':
    app.run(debug=True)