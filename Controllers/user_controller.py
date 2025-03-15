from Models.user_model import User
from Utils.CommonExceptions import CommonException
import logging
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import os
import datetime
from dotenv import load_dotenv
from flask import request, jsonify
from Utils.jwt_authentication import CheckAuthorization

load_dotenv()


class UserController():
    def getOneUser():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            if user:
                return jsonify(user.to_json()), 200
            else:
                return jsonify({"Error": "User not found"}), 404
        except Exception as e:
            logging.error(f"Error in getOneUser: {str(e)}")
            return CommonException.handleException(e)

    def signup():
        try:
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            
            if 'password' not in data:
                return jsonify({"Error": "Password is required"}), 400

            data['password'] = generate_password_hash(data['password'])
            
            user = User(**data)
            user.validate()
            user.save()

            exp_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            token = jwt.encode(
                {
                    "email": user.email,
                    "username": user.username,
                    "exp": exp_time,
                },
                os.getenv("JWT_SECRET"),
            )

            user.auth_token = token
            user.save()

            return jsonify({
                "role": user.role,
                "token": token,
                "exp": exp_time
            }), 200

        except Exception as e:
            logging.error(f"Error in signup: {str(e)}")
            return CommonException.handleException(e)


    def updateUser():
        try:
            data = request.get_json()
            token = request.headers.get('Authorization')
            if not data:
                return CommonException.DataRequiredException()
            if 'phone' in data or 'email' in data:
                return jsonify({"Error": "Cannot update Email or Password here"}), 400
            user = User.objects(auth_token=token).first()
            if user:
                user.update(**data)
                return jsonify({"Message": "User Updated Successfully"}), 200
            else:
                return CommonException.InvalidIdException()
        except Exception as e:
            logging.error(f"Error in updateUser: {str(e)}")
            return CommonException.handleException(e)

    def deleteUser():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            if user:
                user.delete()
                return jsonify({"Message": "User Deleted Successfully"}), 200
            else:
                return CommonException.InvalidIdException()
        except Exception as e:
            logging.error(f"Error in deleteUser: {str(e)}")
            return CommonException.handleException(e)

    def login():
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")       
            if not email or not password:
                return jsonify({"message": "Please enter both username and password"}), 400
            user = User.objects(email=email).first()
            if user and check_password_hash(user.password, password):
                exp_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
                token = jwt.encode(
                    {
                        "email": user.email,
                        "username": user.username,
                        "exp": exp_time,
                    },
                    os.getenv("JWT_SECRET"),
                )
                user.auth_token = token
                user.save()
                return {"token": token, "exp": exp_time,"role":user.role}, 200
            else:
                return {"error": "Invalid username or password"}, 400
        except Exception as e:
            logging.error(f"Error in login: {str(e)}")
            return CommonException.handleException(e)

    def signOut():
        try:
            token = request.headers.get("Authorization")
            check = CheckAuthorization.VerifyToken(token)
            if check == True:
                user = User.objects(auth_token=token).first()  
                if user:
                    user.auth_token = ""
                    user.save()
                    return {"message": "Logged out successfully!"}, 200
                else:
                    return {"message": "User not found."}, 404
            else:
                return check
        except Exception as e:
            logging.error(f"Error in signOut: {str(e)}")
            return CommonException.handleException(e)
