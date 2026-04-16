from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, model_validator, Field
from datetime import datetime
import re


class UserRegistration(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
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

    class Config:
        # скрываем password_confirm при выводе
        fields = {"password_confirm": {"exclude": True}}


# функция регистрации
def register_user(data: dict):
    try:
        user = UserRegistration(**data)
        return user
    except Exception as e:
        return str(e)