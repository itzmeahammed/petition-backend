from Controllers.petition_controller import PetitionController
from flask import Blueprint

petition_bp = Blueprint('Petition', __name__)

petition_bp.add_url_rule('/getPetition', view_func=PetitionController.getPetition, methods=['GET'])
petition_bp.add_url_rule('/getPetitionByHandler', view_func=PetitionController.getPetitionByHandler, methods=['GET'])
petition_bp.add_url_rule('/getPetitionsByUser', view_func=PetitionController.getPetitionsByUser, methods=['GET'])
petition_bp.add_url_rule('/createPetition', view_func=PetitionController.createPetition, methods=['POST'])
petition_bp.add_url_rule('/updatePetition', view_func=PetitionController.updatePetition, methods=['PUT'])
petition_bp.add_url_rule('/deletePetition', view_func=PetitionController.deletePetition, methods=['DELETE'])
