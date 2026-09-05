from fastapi import FastAPI
from contextlib import asynccontextmanager
from expense.routes import router as expense_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")


metadata_tags = [
    {"name": "Expense", "description": "Operation related to expenses management"}
]


app = FastAPI(
    title="Expense-Tracker",
    contact={
        "name": "AmirhoseinFatahi1307",
        "email": "fatahiamirhosein8@gmail.com",
        "url": "https://www.linkedin.com/in/amirhosein-fatahi-64b797413/",
    },
    license_info={"name": "MIT"},
    lifespan=lifespan,
    openapi_tags=metadata_tags,
)


app.include_router(expense_routers)
