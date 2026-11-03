class userDTO:
    def __init__(self):
        self.uid = None
        self.email = None
        self.name = None
        self.role = None

    def is_Empty(self):
        return self.uid is None and self.email is None

    def get_uid(self): return self.uid
    def set_uid(self, uid): self.uid = uid

    def get_email(self): return self.email
    def set_email(self, email): self.email = email

    def get_name(self): return self.name
    def set_name(self, name): self.name = name

    def get_role(self): return self.role
    def set_role(self, role): self.role = role

    def user_to_dict(self):
        return {
            "uid": self.uid,
            "email": self.email,
            "name": self.name,
            "role": self.role
        }