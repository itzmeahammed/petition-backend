from mongoengine import Document, StringField,EmailField
import datetime
class User(Document):
    username = StringField(required=True)
    number=StringField(required=True)
    email= EmailField(unique=True,required=True)
    role=StringField(choices=['user','admin','superadmin'],required=True)
    auth_token = StringField()
    password=StringField(required=True)
    address=StringField()

    def update(self, **kwargs):
        self.clean()
        return super().update(**kwargs)
   
    def to_json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "number":self.number if self.number else None,
            "email":self.email if self.email else None,
            "role":self.role if self.role else None,
            "address":self.address if self.address else None,

        }


    def remove_expired_tokens(self):
        current_time = datetime.datetime.utcnow()
        valid_tokens = [token for token in self.authToken if 'exp' in token and token['exp'] > current_time]
        self.update(set__authToken=valid_tokens if valid_tokens else "")
