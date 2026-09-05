from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ExpenseBaseSchema(BaseModel):
    title: str = Field(
        ..., max_length=150, min_length=2, description="Title of the expense"
    )
    amount: Decimal = Field(
        ...,
        gt=0,
        max_digits=10,
        decimal_places=2,
        description="Amount of the expense",
    )
    category: Optional[str] = Field(
        default=None,
        max_length=150,
        description="Category of the expense",
        examples=["Food", "Transport", "Bills"],
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Description of the expense"
    )


class ExpenseCreateSchema(ExpenseBaseSchema):
    pass


class ExpenseUpdateSchema(BaseModel):
    title: Optional[str] = Field(
        default=None, max_length=150, min_length=2, description="Title of the expense"
    )
    amount: Optional[Decimal] = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
        description="Amount of the expense",
    )
    category: Optional[str] = Field(
        default=None,
        max_length=150,
        description="Category of the expense",
        examples=["Food", "Transport", "Bills"],
    )
    description: Optional[str] = Field(
        default=None, max_length=500, description="Description of the expense"
    )


class ExpenseResponseSchema(ExpenseBaseSchema):
    id: int = Field(..., description="Unique identifier of the Expense")
    created_at: datetime = Field(
        ..., description="Creation date and time of the Expense"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Updating date and time of the Expense"
    )
