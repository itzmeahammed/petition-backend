import jwt
from Models.user_model import User
# from Utils.CommonExceptions import CommonException
import logging
# from flask import jsonify
import os
from dotenv import load_dotenv
load_dotenv()
class CheckAuthorization():
    def VerifyToken(token):
        try:
            if not token:
                return {"message": "Token is required"}, 401
            try:
                decoded_token = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            except jwt.ExpiredSignatureError  as e:
                logging.error(f"Token Expired Error in verify_token: {str(e)}")
                return {"message": "Token has expired"}, 401
            except jwt.InvalidTokenError :
                return {"message": "Invalid token"}, 401
            user=User.objects(auth_token=token).first()
            if user:
                return True
            else:
                return {"message": "Token has expired or Invalid token "}, 401   
        except Exception as e:
            return {"message": f"Error: {str(e)}"}, 401
        
        