from app.core.entity import (User as UserModel)
from app.core.repository import IUserRepository


from sqlalchemy.orm import Session


class UserRepository(IUserRepository):

    def __init__(self, db: Session):
        super(UserRepository, self).__init__()
        self.db = db

    def create_user(self, user: UserModel) -> bool:
        try:
            self.db.add(user)
            self.db.commit()
        except:
            return False
        return True

    def get_user_by_username(self, username: str):
        user = self.db.query(UserModel).filter(UserModel.username == username).first()

        if not user:
            return None
        return user
