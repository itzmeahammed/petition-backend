from Models.feedback_model import Feedback
from Models.user_model import User
from Utils.CommonExceptions import CommonException
import logging
from flask import request, jsonify


class FeedbackController:
    def getFeedbackByPetition():
        try:
            petition= request.args.get('petition')
            if not petition:
                return CommonException.IdRequiredException()
            feedbacks = Feedback.objects(petition=petition)
            if feedbacks:
                return jsonify([feedback.to_json() for feedback in feedbacks]), 200
            return jsonify({"message": "No feedback found for this petition"}), 200
        except Exception as e:
            logging.error(f"Error in getFeedbackByPetition: {str(e)}")
            return CommonException.handleException(e)

    def createFeedback():
        try:
            token = request.headers.get('Authorization')
            user = User.objects(auth_token=token).first()
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()

            petition_id = data.get("petition")

            if not petition_id :
                return jsonify({"message": "Petition ID required"}), 400

            feedback = Feedback(user=user.id,**data)
            feedback.validate()
            feedback.save()

            return jsonify({"message": "Feedback added successfully", "feedback": str(feedback.id)}), 200

        except Exception as e:
            logging.error(f"Error in createFeedback: {str(e)}")
            return CommonException.handleException(e)

    def updateFeedback():
        try:
            id = request.args.get('id')
            if not id:
                return CommonException.IdRequiredException()
            data = request.get_json()
            if not data:
                return CommonException.DataRequiredException()

            feedback = Feedback.objects(id=id).first()
            if not feedback:
                return jsonify({"message": "Feedback not found or unauthorized"}), 404

            feedback.update(**data)
            return jsonify({"message": "Feedback updated successfully"}), 200

        except Exception as e:
            logging.error(f"Error in updateFeedback: {str(e)}")
            return CommonException.handleException(e)

    def deleteFeedback():
        try:
            id = request.args.get('id')
            if not id:
                return CommonException.IdRequiredException()
            feedback = Feedback.objects(id=id).first()
            if not feedback:
                return jsonify({"message": "Feedback not found or unauthorized"}), 404

            feedback.delete()
            return jsonify({"message": "Feedback deleted successfully"}), 200

        except Exception as e:
            logging.error(f"Error in deleteFeedback: {str(e)}")
            return CommonException.handleException(e)
