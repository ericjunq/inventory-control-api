from schemas import UsuarioUpdateResponse, UsuarioSchema, UsuarioUpdate, UsuarioCreateResponse, RefreshTokenInput
from models import Usuario
from dependencies import get_db
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from validations import validar_telefone, validate_cpf
from security import verificar_senha, criptografar_senha, criar_access_token, criar_refresh_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from database import settings

auth_router = APIRouter(prefix='/users', tags=['users'])

# Rota de cadastro de usuário
@auth_router.post('/cadastro', response_model=UsuarioCreateResponse)
async def cadastrar_usuario(
    usuarioschema: UsuarioSchema, 
    db: Session = Depends(get_db)):
    # Verifica se o CPF é válido
    cpf_valido = validate_cpf(usuarioschema.cpf)
    if not cpf_valido:
        raise HTTPException(status_code=400, detail='CPF inválido')
    
    # Verifica se o telefone é válido
    telefone_valido = validar_telefone(usuarioschema.telefone)
    if not telefone_valido:
        raise HTTPException(status_code=400, detail='Telefone inválido')

    # Verifica se o email já existe no banco   
    email_existente = db.query(Usuario).filter(Usuario.email == usuarioschema.email).first()
    if email_existente:
        raise HTTPException(status_code=409, detail='Email já cadastrado')
    
    # Verifica se o CPF já existe no banco
    cpf_existente = db.query(Usuario).filter(Usuario.cpf == usuarioschema.cpf).first()
    if cpf_existente:
        raise HTTPException(status_code=409, detail='CPF já cadastrado')
    
    # Verifica se o telefone já existe no banco
    telefone_existente = db.query(Usuario).filter(Usuario.telefone == usuarioschema.telefone).first()
    if telefone_existente:
        raise HTTPException(status_code=409, detail='Telefone já cadastrado')
    
    # Criptografa a senha recebida
    senha_criptografada = criptografar_senha(usuarioschema.senha)

    # Cria novo usuario
    novo_usuario = Usuario(
        nome = usuarioschema.nome,
        sobrenome = usuarioschema.sobrenome,
        email = usuarioschema.email,
        senha_hash = senha_criptografada,
        cpf = usuarioschema.cpf,
        telefone = usuarioschema.telefone
    )
    # Insere e atualiza o usuario no banco
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario

# Rota de Login
@auth_router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)):

    # verifica se o email existe no banco
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    
    # verifica se a senha recebida bate com a senha cadastrada no banco em forma de hash
    if not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail='Senha incorreta')
    
    # cria access token
    access_token = criar_access_token(
        dados={'sub': form_data.username, 'type': 'access'}
    )
    
    # cria refresh token
    refresh_token = criar_refresh_token(
        dados={'sub': form_data.username, 'type': 'refresh'}
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }
    
# Rota pra editar dados do Usuário
@auth_router.patch('/editar_usuario', response_model=UsuarioUpdateResponse)
async def editar_usuario(
    usuario_update: UsuarioUpdate, 
    db: Session = Depends(get_db), 
    usuario_logado: Usuario = Depends(get_current_user)):

    usuario = db.query(Usuario).filter(Usuario.id == usuario_logado.id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    
    # transforma os dados recebidos em formato de dicionário
    dados_update = usuario_update.dict(exclude_unset=True)

    for campo, valor in dados_update.items():
        setattr(usuario, campo, valor)
    
    db.commit()
    db.refresh(usuario)

    return usuario


@auth_router.post('/refresh_token')
async def token_refresh(data: RefreshTokenInput, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            data.token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=401, detail='Token inválido')
        
        email = payload.get('sub')
        if email is None:
            raise HTTPException(status_code=401, detail='Token inválido')
    
    except JWTError:
        raise HTTPException(status_code=401, detail='Token inválido')
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise HTTPException(status_code=401, detail='Usuário não encontrado')
    
    novo_access_token = criar_access_token(
        dados={'sub': email, 'type': 'access'}
    )
    
    return {
        'access_token': novo_access_token,
        'type': 'bearer'
        }
        
    