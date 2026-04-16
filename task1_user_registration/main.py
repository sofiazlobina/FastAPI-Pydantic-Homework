from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, model_validator, Field
from datetime import datetime
import re
from fastapi import FastAPI

app = FastAPI(
    title="User Registration API",
    description="API для валидации регистрации пользователей (Pydantic)",
    version="1.0.0",
    docs_url="/user/docs",
    redoc_url="/user/redoc"
)

class UserRegistration(BaseModel):
    model_config = ConfigDict()

    username: str
    email: EmailStr
    password: str
    password_confirm: str
    age: int
    registration_date: datetime = Field(default_factory=datetime.now)

    # username
    @field_validator("username")
    def validate_username(cls, v):
        if not (3 <= len(v) <= 20):
            raise ValueError("Username должен быть от 3 до 20 символов")
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username может содержать только латинские буквы, цифры и _")
        return v

    # password
    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[a-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        return v

    # age
    @field_validator("age")
    def validate_age(cls, v):
        if not (18 <= v <= 120):
            raise ValueError("Возраст должен быть от 18 до 120")
        return v

    # password confirm
    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.password_confirm:
            raise ValueError("Пароли не совпадают")
        return self


# функция регистрации
def register_user(data: dict):
    try:
        user = UserRegistration(**data)

        # убираем password_confirm из вывода (правильный способ v2)
        return user.model_dump(exclude={"password_confirm"})

    except Exception as e:
        return str(e)

def main():
    data = {
        "username": "test_user",
        "email": "test@mail.com",
        "password": "Test1234",
        "password_confirm": "Test1234",
        "age": 25
    }

    result = register_user(data)
    print(result)


if __name__ == "__main__":
    main()