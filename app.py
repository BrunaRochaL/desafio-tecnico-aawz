from flask import Flask
from controllers.seller_controller import app as seller_controller_app
from controllers.sale_controller import app as sale_controller_app
from database.database import init_db

app = Flask(__name__)
app.register_blueprint(seller_controller_app)
app.register_blueprint(sale_controller_app)


if __name__ == '__main__':
    init_db()
    app.run(port=8000, debug=True)
