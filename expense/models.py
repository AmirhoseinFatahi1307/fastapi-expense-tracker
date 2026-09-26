from sqlalchemy import (
    func,
    Column,
    String,
    Integer,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Numeric,
)
from core.database import Base
from sqlalchemy.orm import relationship


class ExpenseModel(Base):
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(150), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(150), nullable=True)
    description = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("UserModel", back_populates="expense", uselist=False)
