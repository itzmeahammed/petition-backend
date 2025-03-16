from Models.petition_models import Petition
from Models.user_model import User
from flask import jsonify, request
from Utils.CommonExceptions import CommonException
from Controllers.langChainModel_controller import LlmModelChatBotController
import logging
import json
import ast


class PetitionController():
    def getPetition():
        try:
            petitions = Petition.objects()
            if petitions:
                return jsonify([petition.to_json() for petition in petitions]), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            logging.error(f"Error in getPetition: {str(e)}")
            return CommonException.handleException()
        

    def getPetitionByHandler():
        try:
            handler = request.args.get('handler')
            if not handler:
                return CommonException.ParamsRequiredException()
            petitions = Petition.objects(handler=handler).all()
            if petitions:
                return jsonify([petition.to_json() for petition in petitions]), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            logging.error(f"Error in getPetitionByHandler: {str(e)}")
            return CommonException.handleException()
    

    def getPetitionsByUser():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            petitions = Petition.objects(user=user.id)
            if petitions:
                return jsonify([petition.to_json() for petition in petitions]), 200
            else:
                return jsonify([]), 200
        except Exception as e:
            logging.error(f"Error in getPetitionsByUser: {str(e)}")
            return CommonException.handleException(e)
    
    def createPetition():
        try:
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            if not user:
                return CommonException.InvalidIdException()
            
            system_prompt = (
                "Below is a user petition. You need to analyze the petition and assign it to the handler based on the "
                "content,description and title of the petition. It should be assigned to 'admin' or 'superadmin', who are two types of "
                "higher government officials responsible for resolving the user's problem. Your task is to decide "
                "whether the petition is handled by 'admin' (smaller cases like theft, minor disputes) or 'superadmin' "
                "(high-profile cases such as murder, rape, business-related issues, celebrity cases, confidential matters). "
                "Analyze every single word in the petition before making your decision. And also give the catogory of the  "
                "petition and some tags like related to petition in a array of string . Provide the response strictly in "
                "the following JSON format: [{'category':'eg theft',handler':'admin' or 'superadmin',tags:[]}]."
            )
            
            user_prompt = f"Title: {data.get('title')}\nDescription: {data.get('description')}\nContent: {data.get('content')}"
            
            input_prompt = [("system", system_prompt), ("user", user_prompt)]
            model = request.args.get('model', 'OpenAI')
            ai_response = LlmModelChatBotController.ConfigureAIModel(input_prompt, model)

            try:
                formatted_response = ai_response.replace("'", '"')
                handler_data = json.loads(formatted_response)
                handler = handler_data[0].get('handler')
                catogory = handler_data[0].get('category')
                tags = handler_data[0].get('tags')

            except json.JSONDecodeError as e:
                logging.error(f"JSON parsing error: {str(e)} - Trying ast.literal_eval()")

                try:
                    handler_data = ast.literal_eval(ai_response)
                    handler = handler_data[0].get('handler')
                    catogory = handler_data[0].get('category')
                    tags = handler_data[0].get('tags')

                except (ValueError, SyntaxError) as e:
                    logging.error(f"Error parsing AI response with ast: {str(e)}")
                    handler = "admin"
                    catogory= ''
                    tags = []
            
            petition = Petition(
                user=user,
                title=data.get('title'),
                description=data.get('description'),
                content=data.get('content'),
                category=catogory,
                tags=tags,
                handler=handler,
                date=data.get('date')
            )
            petition.validate()
            petition.save()
            return jsonify({"Message": "Petition Created Successfully", "Handler": handler}), 200
        except Exception as e:
            logging.error(f"Error in createPetition: {str(e)}")
            return CommonException.handleException(e)

    
    def updatePetition():
        try:
            # token = request.headers.get('Authorization')
            id = request.args.get('id')
            if not id:
                return CommonException.IdRequiredException()
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()
            petition = Petition.objects(id=id).first()
            if petition:
                petition.update(**data)
                return jsonify({"Message": "Petition Updated Successfully"}), 200
            else:
                return CommonException.InvalidIdException()
        except Exception as e:
            logging.error(f"Error in updatePetition: {str(e)}")
            return CommonException.handleException(e)
    
    def deletePetition():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            id = request.args.get('id')
            if not id:
                return CommonException.IdRequiredException()
            petition = Petition.objects(user=user.id, id=id).first()
            if petition:
                petition.delete()
                return jsonify({"Message": "Petition Deleted Successfully"}), 200
            else:
                return CommonException.InvalidIdException()
        except Exception as e:
            logging.error(f"Error in deletePetition: {str(e)}")
            return CommonException.handleException(e)

