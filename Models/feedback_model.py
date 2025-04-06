from mongoengine import Document, StringField,ReferenceField,DateTimeField
from datetime import datetime
from Models.user_model import User
from Models.petition_models import Petition

class Feedback(Document):
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    petition= ReferenceField(Petition, required=True, reverse_delete_rule=2)
    feedback = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
   

    def update(self, **kwargs):
        self.clean()
        return super().update(**kwargs)
   
    def to_json(self):
        return {
            "id": str(self.id),
            "user": str(self.user.id),
            "petition":str(self.petition.id) if self.petition else None,
            "feedback":self.feedback if self.feedback else None,
            "created_at":self.created_at if self.created_at else None,

        }
