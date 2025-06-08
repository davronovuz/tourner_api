"""Database models for tournaments and players."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for SQLAlchemy declarative models."""
    pass

class Tournament(Base):
    """Model representing a tournament."""
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    max_players = Column(Integer, nullable=False)
    start_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    players = relationship("Player", back_populates="tournament")

class Player(Base):
    """Model representing a player."""
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    tournament = relationship("Tournament", back_populates="players")