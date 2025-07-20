from flask import Flask
from flask_cors import CORS
from routes.driver_routes import driver_routes
from routes.company_routes import company_routes
from routes.location_routes import location_routes
from routes.mpesa_routes import mpesa_routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(driver_routes)
app.register_blueprint(company_routes)
app.register_blueprint(location_routes)
app.register_blueprint(mpesa_routes)

if __name__ == '__main__':
    app.run(debug=True)
