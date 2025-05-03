from datetime import datetime
from App import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Comment(db.Model):
    uid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    user_uid = db.Column(UUID(as_uuid=True), db.ForeignKey('user.uid', ondelete='CASCADE'), nullable=False)
    post_uid = db.Column(UUID(as_uuid=True), db.ForeignKey('post.uid', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)