from flask_weather.app import app

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9090, threaded=False)
