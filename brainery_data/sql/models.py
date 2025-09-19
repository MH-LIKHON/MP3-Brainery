# =======================================================
# SQLAlchemy Models (Users, Subjects, Topics)
# =======================================================

from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy import String, Text, ForeignKey, DateTime, UniqueConstraint


# =======================================================
# Base Class
# =======================================================

class Base(DeclarativeBase):
    pass


# =======================================================
# Users Model
# =======================================================

class UserSQL(Base):
    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)

    # Unique + indexed
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # user/admin
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


# =======================================================
# Subjects Model
# =======================================================

class Subject(Base):
    __tablename__ = "subjects"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Unique subject name
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    icon: Mapped[str] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


# =======================================================
# Topics Model
# =======================================================

class Topic(Base):
    __tablename__ = "topics"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # FK -> subjects.id
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


# =======================================================
# SavedTopics Model
# =======================================================

class SavedTopic(Base):
    __tablename__ = "saved_topics"
    __table_args__ = (UniqueConstraint("user_id", "title", name="uq_savedtopic_user_title"),)

    # Enforce 1 title per user
    __table_args__ = (
        UniqueConstraint("user_id", "title", name="uq_savedtopic_user_title"),
    )

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # FK -> users.id
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Title + summary
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=True)

    # Created timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


# =======================================================
# Resources Model
# =======================================================

class ResourceSQL(Base):
    __tablename__ = "resources"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # FK -> users.id (owner of the resource)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Core fields
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    link: Mapped[str] = mapped_column(String(500), nullable=True)
    category: Mapped[str] = mapped_column(String(120), nullable=True)

    # Created timestamp
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)