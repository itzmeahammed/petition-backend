from flask import jsonify
from mongoengine.errors import ValidationError, NotUniqueError
from pymongo.errors import DuplicateKeyError

class CommonException():
    def handleException(error):
        if isinstance(error, ValidationError):
            return jsonify({"Error": "Validation Failed", "Details": str(error)}), 400
        elif isinstance(error, NotUniqueError) or isinstance(error, DuplicateKeyError):
            return jsonify({"Error": "Duplicate Key", "Details": str(error)}), 409
        elif isinstance(error, KeyError):
            return jsonify({"Error": "Missing Required Fields", "Fields": str(error)}), 400
        elif isinstance(error, ValueError):
            return jsonify({"Error": "Invalid Query", "Details": str(error)}), 400
        elif isinstance(error, TimeoutError):
            return jsonify({"Error": "Database Operation Timed Out"}), 500
        elif isinstance(error, PermissionError):
            return jsonify({"Error": "Unauthorized Access"}), 400
        elif isinstance(error,ConnectionError) or isinstance(error,ConnectionAbortedError) or isinstance(error,ConnectionRefusedError) or isinstance(error,ConnectionResetError):
            return jsonify({"Error": "Database Connection Failed"}), 500
        else:
            return jsonify({"Error": "Operation Failed", "Details": str(error)}), 500

    def IdRequiredException(feild="Id"):
        return jsonify({"Error": f"{feild} Required"}), 404
    def KeyRequiredException(feild="Key"):
        return jsonify({"Error": f"{feild} Required"}), 404
    def DataRequiredException():
        return jsonify({"Error": "Data Required"}), 404
    def ParamsRequiredException():
        return jsonify({"Error":"No Input Params Found"}),404
    
    def InvalidParamsException():
        return jsonify({"Error": f"Invalid Query, No Data Found"}),404

    def InvalidIdException(id=''):
        return jsonify({"Error": f"Invalid Id: No Data Found"}), 404