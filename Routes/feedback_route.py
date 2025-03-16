from Controllers.feedback_controller import FeedbackController
from flask import Blueprint

feedback_bp = Blueprint('Feedback', __name__)

feedback_bp.add_url_rule('/getFeedbackByPetition', view_func=FeedbackController.getFeedbackByPetition, methods=['GET'])
feedback_bp.add_url_rule('/createFeedback', view_func=FeedbackController.createFeedback, methods=['POST'])
feedback_bp.add_url_rule('/updateFeedback', view_func=FeedbackController.updateFeedback, methods=['PUT'])
feedback_bp.add_url_rule('/deleteFeedback', view_func=FeedbackController.deleteFeedback, methods=['DELETE'])
