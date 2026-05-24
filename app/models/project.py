from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_name = Column(String(200), nullable=False, default="")
    project_idea = Column(Text, nullable=False)
    currency = Column(String(3), nullable=False, default="INR")
    status = Column(String(20), nullable=False, default="Exploring")
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    estimates = relationship("Estimate", back_populates="project", cascade="all, delete-orphan")


class Estimate(Base):
    __tablename__ = "estimates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    estimate_type = Column(String(50), nullable=False)  # "cost", "revenue", "risk", etc.
    estimate_data = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime, nullable=False, default=func.now())

    project = relationship("Project", back_populates="estimates")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    mode = Column(String(50), nullable=False, default="general")
    project_idea = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(100), index=True, nullable=False)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
