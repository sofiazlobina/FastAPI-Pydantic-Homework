from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from datetime import datetime
import re


class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str
    age: int

    # новые поля
    full_name: str
    phone: str

    registration_date: datetime = Field(default_factory=datetime.now)

    # конфигурация Pydantic v2 (пока пустая, но правильно оформлена)
    model_config = {}

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
            raise ValueError("Пароль должен быть минимум 8 символов")
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

    # full name
    @field_validator("full_name")
    def validate_full_name(cls, v):
        if len(v) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")
        if not v[0].isupper():
            raise ValueError("Имя должно начинаться с заглавной буквы")
        return v

    # phone
    @field_validator("phone")
    def validate_phone(cls, v):
        if not re.match(r"^\+\d-\d{3}-\d{2}-\d{2}$", v):
            raise ValueError("Телефон должен быть в формате +X-XXX-XX-XX")
        return v

    # проверка паролей
    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.password_confirm:
            raise ValueError("Пароли не совпадают")
        return self


# функция регистрации
def register_user(data: dict):
    try:
        user = UserRegistration(**data)

        # скрываем password_confirm при выводе
        return user.model_dump(exclude={"password_confirm"})

    except Exception as e:
        return str(e)


# тестовый запуск
def main():
    data = {
        "username": "test_user",
        "email": "test@mail.com",
        "password": "Test1234",
        "password_confirm": "Test1234",
        "age": 25,
        "full_name": "Ivan",
        "phone": "+7-123-45-67"
    }

    result = register_user(data)
    print(result)


if __name__ == "__main__":
    main()