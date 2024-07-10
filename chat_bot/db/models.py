from sqlalchemy import BigInteger, SmallInteger, String
from sqlalchemy.orm import mapped_column
from db.base import Base


class Chat(Base):
    __tablename__ = 'chats'

    user_id = mapped_column(BigInteger, primary_key=True)
    specialist_id = mapped_column(BigInteger)
    feedback = mapped_column(String, default='')
    status = mapped_column(String, default='in process')

    def __repr__(self):
        info: str = f'Пользователь [{self.user_id}] | Специалист {self.specialist_id}'
        return info


class Specialist(Base):
    __tablename__ = 'specialists'

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String)
    surname = mapped_column(String)
    age = mapped_column(SmallInteger)
    photo_id = mapped_column(BigInteger, default=0)
    file_id = mapped_column(BigInteger, default=0)
    description = mapped_column(String, default='...')
    status = mapped_column(SmallInteger, default=0)

    def __repr__(self):
        info: str = f'Специалист {self.surname} {self.name}, {self.age} лет'
        return info
