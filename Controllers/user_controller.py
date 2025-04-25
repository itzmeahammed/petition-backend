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
    def getAllUser():
        try:
            users = User.objects()
            if users:
                return jsonify([user.to_json() for user in users]), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            logging.error(f"Error in getAllUser: {str(e)}")
            return CommonException.handleException(e)
        
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

    def signup():
        try:
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            
            if 'password' not in data:
                return jsonify({"Error": "Password is required"}), 400

            # Hash the password
            data['password'] = generate_password_hash(data['password'])
            
            # Check if the email is already taken
            existing_user = User.objects(email=data['email']).first()
            if existing_user:
                return jsonify({"Error": "Email is already registered"}), 400

            # Admin specific logic
            if data['role'] == 'admin':
                district = data.get('district')
                station = data.get('station')
                
                if not district or not station:
                    return jsonify({"Error": "District and Station are required for Admin."}), 400
                
                # Check if this station already has an admin
                existing_station_admin = User.objects(station=station).first()
                if existing_station_admin:
                    return jsonify({"Error": f"Station {station} already has an admin."}), 400
                
                # Add district and station to the data
                data['district'] = district
                data['station'] = station
                
            # Super Admin specific logic
            if data['role'] == 'superadmin':
                district = data.get('district')
                if not district:
                    return jsonify({"Error": "District is required for Super Admin."}), 400
                
                # Check if this district already has a super admin
                existing_district_superadmin = User.objects(district=district).first()
                if existing_district_superadmin:
                    return jsonify({"Error": f"District {district} already has a Super Admin."}), 400
                
                # Add district to the data
                data['district'] = district
            
            user = User(**data)
            user.validate()
            user.save()

            # Generate JWT token for the user
            exp_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            token = jwt.encode(
                {
                    "user_id": str(user.id),
                    "email": user.email,
                    "username": user.username,
                    "exp": exp_time
                },
                os.getenv("JWT_SECRET"),
                algorithm="HS256"
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

                # Return district and station information based on role
                user_info = {
                    "token": token,
                    "exp": exp_time,
                    "role": user.role
                }

                if user.role == "admin":
                    user_info["district"] = user.district
                    user_info["station"] = user.station
                elif user.role == "superadmin":
                    user_info["district"] = user.district
                
                return jsonify(user_info), 200
            else:
                return jsonify({"error": "Invalid username or password"}), 400
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
