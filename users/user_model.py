# app/users/models.py
from pydantic import BaseModel, EmailStr, Field

# Schema para os dados que o cliente envia ao criar um usuário
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = Field(default=None, min_length=3)

# Schema para os dados que o cliente envia ao ATUALIZAR um usuário
# Todos os campos são opcionais
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    full_name: str | None = Field(default=None, min_length=3)

# Schema para os dados que a API retorna ao cliente
class UserPublic(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None