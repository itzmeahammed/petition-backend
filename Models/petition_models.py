from mongoengine import Document, StringField, ReferenceField, DateTimeField, ListField
from Models.user_model import User
from datetime import datetime

class Petition(Document):
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    title = StringField(required=True)
    description = StringField(required=True)
    content = StringField(required=True)
    category = StringField(required=True)
    handler = StringField(choices=['admin', 'superadmin'], required=True)
    tags = ListField(StringField())
    status = StringField(default="Pending")
    station = StringField()  # Added station field
    district = StringField()  # Added district field
    date = StringField(required=True)
    solution = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    image_url = StringField()

    def to_json(self):
        return {
            "id": str(self.id),
            "user": self.user.username if self.user else None,
            "petition_title": self.title,
            "petition_description": self.description,
            "petition_content": self.content,
            "category": self.category,
            "handler": self.handler,
            "tags": self.tags,
            "date": self.date,
            "solution": self.solution,
            "station": self.station,  # Include station in the JSON response
            "district": self.district,  # Include district in the JSON response
            "status": self.status,
            "created_at": self.created_at.strftime("%d %B %Y"),
            "updated_at": self.updated_at.strftime("%d %B %Y"),
            "image_url": self.image_url
        }
