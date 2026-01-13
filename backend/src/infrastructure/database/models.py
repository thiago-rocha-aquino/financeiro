from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, Numeric, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.domain.entities import TransactionType


class Base(DeclarativeBase):
    """Base para todos os modelos."""

    pass


class UserModel(Base):
    """Modelo de banco de dados para usuário."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    initial_balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    categories: Mapped[list["CategoryModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    transactions: Mapped[list["TransactionModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    budgets: Mapped[list["BudgetModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class CategoryModel(Base):
    """Modelo de banco de dados para categoria."""

    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50))
    color: Mapped[str] = mapped_column(String(7), default="#6366f1")
    icon: Mapped[str] = mapped_column(String(30), default="tag")
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped["UserModel"] = relationship(back_populates="categories")
    transactions: Mapped[list["TransactionModel"]] = relationship(
        back_populates="category"
    )
    budgets: Mapped[list["BudgetModel"]] = relationship(back_populates="category")


class TransactionModel(Base):
    """Modelo de banco de dados para transação."""

    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    description: Mapped[str] = mapped_column(String(200))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType))
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped["UserModel"] = relationship(back_populates="transactions")
    category: Mapped[Optional["CategoryModel"]] = relationship(
        back_populates="transactions"
    )


class BudgetModel(Base):
    """Modelo de banco de dados para orçamento."""

    __tablename__ = "budgets"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    month: Mapped[int] = mapped_column()
    year: Mapped[int] = mapped_column()
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    user: Mapped["UserModel"] = relationship(back_populates="budgets")
    category: Mapped["CategoryModel"] = relationship(back_populates="budgets")
