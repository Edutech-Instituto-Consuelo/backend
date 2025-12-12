from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal, Annotated
from datetime import date, datetime

TipoUser = Literal["instrutor", "aluno", "admin"]

"""Annotated é um tipo parametrizado do Python que permite adicionar metadados a um tipo existente."""

NomeType = Annotated[str, Field(min_length=1, max_length=45, description="Nome")]
SobrenomeType = Annotated[str, Field(min_length=1, max_length=45, description="Sobrenome")]
SenhaType = Annotated[str, Field(min_length=6, max_length=128, description="Senha em texto")]
EmailType = Annotated[EmailStr, Field(description="Email válido")]

##===================== USUARIO ========================##

# Campos base usados tanto em input quanto em output (sem senha)
# É o modelo base usado tanto para envio quanto para retorno de dados
class UsuarioBase(BaseModel):
    nome: NomeType
    sobrenome: SobrenomeType
    email: EmailType

# schema de entrada quando o usuário está criando uma conta
class UsuarioCriar(UsuarioBase):
    senha_hash: SenhaType
    tipo_usuario:TipoUser = "aluno"
    data_nascimento: date

# schema de saída, ou seja, aquilo que o servidor retorna ao cliente ao consultar um usuário
class UsuarioResponse(UsuarioBase):
    id: int
    tipo_usuario: TipoUser
    data_cadastro: datetime
    ultimo_login: Optional[datetime]

    # permite que o Pydantic converta objetos SQLAlchemy:
    class Config:
        #orm_mode = True  # pydantic v1
        from_attributes = True  #pydantic v2 (automático)

class UsuarioAtualizarTudo(BaseModel):
    nome: NomeType
    sobrenome: SobrenomeType
    email: EmailType
    data_nascimento: date

class UsuarioAtualizarParcial(BaseModel):
    """Usado em PATCH: todos opcionais"""
    nome: Optional[NomeType] = None
    sobrenome: Optional[SobrenomeType] = None
    email: Optional[EmailType] = None
    data_nascimento: Optional[date] = None

# schema usado quando o usuário faz login.
class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioAdminUpdate(BaseModel):
    tipo_usuario: TipoUser
