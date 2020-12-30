"""
all models
"""
import datetime
from sqlalchemy import Column, Integer, String, Boolean
from database import Base



class Note(Base):
    """
    represent a note record
    """
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True,)
    user_id = Column(String(50), nullable=False)
    text = Column(String(500), nullable=False)
    source = Column(String(200), nullable=False)
    tags = Column(String(500), default='')
    comments = Column(String(500), default='')
    deleted = Column(Boolean, nullable=False, default=False)
    created_on = Column(String(20), default=datetime.datetime.utcnow())
    modified_on = Column(String(20), default=datetime.datetime.utcnow())

    def __init__(self, user_id, text, source):
        self.user_id = user_id
        self.text = text
        self.source = source

    def serialize(self):
        """
        serializes the note object
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'source': self.source,
            'tags': self.tags,
            'comments': self.comments,
            'created_on': self.created_on,
            'modified_on': self.modified_on
        }

    # def __repr__(self):
    #     return '<data %r>' % self.text
