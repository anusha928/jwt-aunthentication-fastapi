from pydantic import EmailStr, BaseModel

class CreateUserRequest(BaseModel):
    first_name:str
    last_name: str
    email: EmailStr
    password: str