from sqlalchemy import (
    func,
    Column,
    String,
    Integer,
    Boolean,
    Text,
    DATETIME,
    ForeignKey,
    Numeric,
)
from core.database import Base
from sqlalchemy.orm import relationship


class ExpenseModel(Base):
    __tablename__ = "expense"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(150), nullable=True)
    description = Column(Text(500), nullable=True)

    created_at = Column(DATETIME, server_default=func.now())
    updated_at = Column(DATETIME, server_default=func.now(), onupdate=func.now())
