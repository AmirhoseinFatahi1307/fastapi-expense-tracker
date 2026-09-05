from fastapi import APIRouter, Path, Depends, HTTPException, Body, Query, status
from fastapi.responses import JSONResponse
from expense.schemas import *
from expense.models import ExpenseModel
from user.models import UserModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from auth.jwt_auth import get_authenticated_user

router = APIRouter(tags=["Expense"], prefix="/expense")


@router.get("/Expense", response_model=List[ExpenseResponseSchema])
async def retrieve_expense_list(
    category: str = Query(None, description="Filter expense based on the category"),
    limit: int = Query(
        default=10,
        gt=0,
        le=50,
        description="Maximum number of expense returned per page",
    ),
    offset: int = Query(
        default=0, ge=0, description="Number of items to skip before returning results"
    ),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    query = db.query(ExpenseModel).filter_by(user_id=user.id)
    if category is not None:
        query = query.filter(ExpenseModel.category.ilike(category))
    return query.limit(limit).offset(offset).all()


@router.get("/Expense/{expense_id}", response_model=ExpenseResponseSchema)
async def retrieve_expense_detail(
    expense_id: int = Path(
        deprecated=True,
        gt=0,
        description="It will be searched with the title you provided",
    ),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    query = db.query(ExpenseModel).filter_by(user_id=user.id, id=expense_id).first()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    return query


@router.post(
    "/Expense",
    response_model=ExpenseResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_expense(
    request: ExpenseCreateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    data = request.model_dump()
    data.update({"user_id": user.id})
    expense_obj = ExpenseModel(**data)
    db.add(expense_obj)
    db.commit()
    db.refresh(expense_obj)
    return expense_obj


@router.put(
    "/Expense/{expense_id}",
    response_model=ExpenseUpdateSchema,
    status_code=status.HTTP_200_OK,
)
async def update_expense(
    request: ExpenseUpdateSchema = Body(),
    expense_id: int = Path(
        deprecated=True,
        description="It will be searched with the title you provided",
        gt=0,
    ),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    expense = db.query(ExpenseModel).filter_by(user_id=user.id, id=expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
    updated_at = request.model_dump(exclude_unset=True)
    for field, value in updated_at.items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/Expense/{expense_id}")
async def deleting_expense(
    expense_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    expense = (
        db.query(ExpenseModel).filter_by(user_id=user.id, id=expense_id).one_or_none()
    )
    if expense:
        db.delete(expense)
        db.commit()
        return JSONResponse(content={"Detail": "Expense removed successfully"})
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
        )
