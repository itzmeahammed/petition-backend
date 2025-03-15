from mongoengine import Document, StringField, ReferenceField, DateTimeField, ListField, IntField
from Models.user_model import User
from datetime import datetime

class Petition(Document):
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    petition_title = StringField(required=True)
    petition_description = StringField(required=True)
    petition_content = StringField(required=True)
    category = StringField(required=True)
    handler = StringField(choices=['admin','superadmin'],required=True)
    tags = ListField(StringField())
    signatures = IntField(default=0)
    status = StringField(default="Pending")
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    image_url = StringField()
    
    def to_json(self):
        return {
            "id": str(self.id),
            "user": str(self.user.id) if self.user else None,
            "petition_title": self.petition_title,
            "petition_description": self.petition_description,
            "petition_content": self.petition_content,
            "category": self.category,
            "handler": self.handler,
            "tags": self.tags,
            "signatures": self.signatures,
            "status": self.status,
            "created_at": self.created_at.strftime("%d %B %Y"),
            "updated_at": self.updated_at.strftime("%d %B %Y"),
            "image_url": self.image_url
        }
