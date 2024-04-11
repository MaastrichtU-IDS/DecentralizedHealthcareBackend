import time
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlmodel import Field, Session, SQLModel, select

from luce.config import settings, engine

router = APIRouter()

# Login with LDAP: https://gist.github.com/femmerling/5097365

class CreateUser(SQLModel, table=False):
    email: str = Field(default='name@gmail.com', primary_key=True, index=True)
    first_name: str
    last_name: str
    institution: str
    user_type: int
    gender: int
    gdpr: str
    country: Optional[str]
    age: Optional[str]
    ethereum_public_key: Optional[str]
    ethereum_private_key: Optional[str]


    @validator("email", "username", "employee_id", "affiliation", "project_type", "project_description", "gdpr")
    def reject_empty_strings(cls, v):
        assert v != ''
        return v

    # @validator("email")
    # def validate_email(cls, v):
    #     pattern = re.compile("^[a-zA-Z0-9\._-]+@[a-zA-Z0-9_-].[a-zA-Z]$")
    #     assert pattern.match(v)
    #     return v

    # class config: validate_assignment = True


class User(CreateUser, table=True):
    comment: str = ''
    access_enabled: bool = False
    created_at: datetime = datetime.now()


# TODO: /user/login


@router.post("/user/register", name="Register a user to access the LUCE blockchain",
    description="Register a user in the LUCE blockchain database",
    response_model=dict,
)
def register_user(createUser: CreateUser = Body(...)) -> dict:
    with Session(engine) as session:
        db_user = User.from_orm(createUser)
        # db_user = User.validate(createUser)
        try:
            session.add(db_user)
            session.commit()
        except IntegrityError:
            return JSONResponse({'errorMessage': f'User with the email {createUser.email} already exists'})
        except OperationalError as e:
            # if e[0] == 2006:
            # Sometime we get "MySQL server has gone away" and we just need to rerun the query
            print(e)
            print('Got "MySQL server has gone away" error, retrying to add the user.')
            time.sleep(1)
            return register_user(createUser)
        except Exception as e:
            print(e)
            return JSONResponse({'errorMessage': f'Error creating the user in the database: {e}'})

    return JSONResponse({'message': f'User {createUser.email} successfully added'})


@router.get("/users", response_model=list[User])
def get_users(response: Response, request: Request) -> list[User]:
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
