import click
from sqlalchemy import create_engine, DateTime, ForeignKey, Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

#  Base class declarative used for ORM classes
Base = declarative_base()
#user
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), default="Regular")

    notes = relationship("Note", back_populates="user")

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username}, email={self.email}, role={self.role})"

    @classmethod
    def create(cls, session, username, email, role="Regular"):
        user = cls(username=username, email=email, role=role)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def delete(cls, session, user_id):
        user = session.query(cls).filter_by(user_id=user_id).first()
        if user:
            session.delete(user)
            session.commit()

    @classmethod
    def update(cls, session, user_id, **kwargs):
        user = session.query(cls).filter_by(user_id=user_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.commit()
            return user
        return None

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, user_id):
        return session.query(cls).filter_by(user_id=user_id).first()
#note class
class Note(Base):
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(1000))
    created_at = Column(DateTime, default=func.now())
    last_modified_at = Column(DateTime, onupdate=func.now())

    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="notes")

    def __repr__(self):
        return f"Note(note_id={self.note_id}, title={self.title}, content={self.content}, created_at={self.created_at})"

    @classmethod
    def create(cls, session, title, content, user_id):
        note = cls(title=title, content=content, user_id=user_id)
        session.add(note)
        session.commit()
        return note

    @classmethod
    def delete(cls, session, note_id):
        note = session.query(cls).filter_by(note_id=note_id).first()
        if note:
            session.delete(note)
            session.commit()
