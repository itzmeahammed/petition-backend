from flask import Flask,request,jsonify
from mongoengine import connect,get_connection
from flask_cors import CORS
import os
from Utils.jwt_authentication import CheckAuthorization
from dotenv import load_dotenv
from Routes.user_route import user_bp
from Routes.petition_route import petition_bp


load_dotenv()


app = Flask(__name__)

db = os.getenv('DB')
db_host = os.getenv('DB_CONNECTION_STRING')
server_host = os.getenv('SERVER_HOST')
server_port = os.getenv('SERVER_PORT')
connect(db=db,host=db_host,ssl=True)

CORS(app,origins='*')


@app.before_request
def check_auth_token():
    if request.method == 'OPTIONS':
        return
    except_routes = [
        '/api/user/signUp',
        '/api/user/signIn',
    ]

    if request.path not in except_routes:
        token = request.headers.get("Authorization")
        verify = CheckAuthorization.VerifyToken(token)
        if verify != True:
            return verify

client = get_connection()

@app.route('/health', methods=['GET'])
def health_check():
    try:
        client.server_info()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({"status": "healthy", "database": db_status}), 200 if db_status == "connected" else 500

    
app.register_blueprint(user_bp,url_prefix='/api/user')
app.register_blueprint(petition_bp,url_prefix='/api/petition')





if __name__ == '__main__':
    app.run(debug=True,host=server_host,port=server_port)




