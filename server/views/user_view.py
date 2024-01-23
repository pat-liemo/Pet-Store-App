from models import db, User
from app import app
from flask import request, jsonify, Blueprint
from flask_jwt_extended import  jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user_bp', __name__)

# Create a user
@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    phone_number = data["phone_number"]
    password = generate_password_hash(data["password"], )
    
    check_username = User.query.filter_by(username = username).first()
    check_email = User.query.filter_by(email = email).first()
    check_phone_number = User.query.filter_by(phone_number = phone_number ).first()
    
    if check_username or check_email or check_phone_number:
        return jsonify({"error": "User email/username/phone_number already exists!"})
    
    else:
        new_user = User(email = email, password = password, username = username, phone_number = phone_number)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": "User added successfully!"}), 201
    
    
# Get details of a single user
@user_bp.route("/users/<int:id>")
def get_user(id):
    user = User.query.get(id)
    user_list =[]
    
    if user:
        user_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number  
        })
        return jsonify(user_list), 200
    else:
        return jsonify({"error": "User not found!"}), 404
    
    
#Update single user's details
@user_bp.route("/users", methods = ["PUT"])
@jwt_required()
def update_user():
    user = User.query.get(get_jwt_identity())
    data = request.get_json()
    
    if user:
        username = data['username']
        email = data['email']
        phone_number = data['phone_number']
        profile_image = data['profile_image']

        check_username = User.query.filter(User.id != get_jwt_identity(), User.username == username).first()
        check_email = User.query.filter(User.id != get_jwt_identity(), User.email == email).first()
        check_phone_number = User.query.filter(User.id != get_jwt_identity(), User.phone_number == phone_number).first()
        
        if check_username or check_email or check_phone_number:
            return jsonify({"error": "User email/username/phone already exist!"})

        else:
            user.username = username
            user.email = email
            user.phone_number = phone_number
            user.profile_image = profile_image
        
            db.session.commit()
            return jsonify({"success": f"{username} updated successfully"}), 200
        
    else:
        return jsonify({"error":"The user you are trying to update does not exist!"}), 404


# Delete User's account
@user_bp.route("/users", methods = ["DELETE"])
@jwt_required()
def delete_user():
    user = User.query.get(get_jwt_identity())
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "The User you are trying to delete does not exist"}), 404
    
    
from . import create_app
app = create_app()

# app.register_blueprint(user_bp)