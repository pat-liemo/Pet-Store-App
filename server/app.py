from datetime import timedelta
from models import db, User,Pet,PetStore,Review,TokenBlocklist
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from views import *

from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)

jwt = JWTManager()
app.config["JWT_SECRET_KEY"] = "fjhjdjhfiskyfvdgvydklvsrfl"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt.init_app(app)



@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
    jti = jwt_data['jti']
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    if token:
        return token 
    else:
        return None
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)