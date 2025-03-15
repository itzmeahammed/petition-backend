from flask import Blueprint
from Controllers.user_controller import UserController

user_bp = Blueprint('User', __name__)

user_bp.add_url_rule('/getUser', view_func=UserController.getOneUser, methods=['GET'])
user_bp.add_url_rule('/signUp', view_func=UserController.signup, methods=['POST'])
user_bp.add_url_rule('/updateUser', view_func=UserController.updateUser, methods=['PUT'])
user_bp.add_url_rule('/deleteUser', view_func=UserController.deleteUser, methods=['DELETE'])
user_bp.add_url_rule('/signIn', view_func=UserController.login, methods=['PUT'])
user_bp.add_url_rule('/signOut', view_func=UserController.signOut, methods=['PUT'])
