from mongoengine import Document, StringField, EmailField

class User(Document):
    username = StringField(required=True)
    number = StringField(required=True)
    email = EmailField(unique=True, required=True)
    role = StringField(choices=['user', 'admin', 'superadmin'], required=True)
    auth_token = StringField()
    password = StringField(required=True)
    address = StringField()
    district = StringField()  # For admin and superadmin
    station = StringField()   # Only for admin

    def update(self, **kwargs):
        self.clean()
        return super().update(**kwargs)
   
    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "number": self.number if self.number else None,
            "email": self.email if self.email else None,
            "role": self.role if self.role else None,
            "address": self.address if self.address else None,
            "district": self.district if self.district else None,
            "station": self.station if self.station else None,
        }
