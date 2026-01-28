"""
All database models with optimizations
"""
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Index, Text
from database import Base


class Note(Base):
    """
    Represent a note record
    """
    __tablename__ = 'note'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False, index=True)
    text = Column(Text, nullable=False)  # Use Text instead of String for longer content
    source = Column(String(500), nullable=False, index=True)
    tags = Column(String(500), default='')
    comments = Column(String(500), default='')
    deleted = Column(Boolean, nullable=False, default=False, index=True)
    created_on = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    modified_on = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    
    # Composite indexes for efficient filtering
    __table_args__ = (
        Index('ix_user_deleted', 'user_id', 'deleted'),
    )

    def __init__(self, user_id, text, source):
        self.user_id = user_id
        self.text = text
        self.source = source
        self.created_on = datetime.datetime.utcnow()
        self.modified_on = datetime.datetime.utcnow()

    def serialize(self):
        """
        Serialize the note object to dictionary
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'source': self.source,
            'tags': self.tags,
            'comments': self.comments,
            'created_on': self.created_on.isoformat() if self.created_on else None,
            'modified_on': self.modified_on.isoformat() if self.modified_on else None
        }

    def __repr__(self):
        return f'<Note id={self.id}, user_id={self.user_id}>'
