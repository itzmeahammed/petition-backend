import jwt
from Models.user_model import User
import logging
import os
from dotenv import load_dotenv

load_dotenv()

class CheckAuthorization:
    @staticmethod
    def VerifyToken(token):
        try:
            if not token:
                return {"message": "Token is required"}, 401
            
            jwt_secret = os.getenv("JWT_SECRET")

            try:
                decoded_token = jwt.decode(token, jwt_secret, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return {"message": "Token has expired"}, 401
            except jwt.DecodeError:
                return {"message": "Invalid token"}, 401
            except jwt.InvalidTokenError:
                return {"message": "Invalid token"}, 401

            # user_id = decoded_token.get("user_id")
            # if not user_id:
            #     return {"message": "Invalid token payload"}, 401

            user = User.objects(auth_token=token).first()
            if user:
                return True
            else:
                return {"message": "User not found"}, 401

        except Exception as e:
            logging.error(f"Unexpected error in VerifyToken: {str(e)}")
            return {"message": f"Error: {str(e)}"}, 500
