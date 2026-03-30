import re

def validar_telefone(telefone):
    padrao = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'

    if re.match(padrao, telefone):
        return True
    return False

def validate_cpf(cpf: str) -> bool:
    # Remove pontos e traço
    cpf = cpf.replace(".", "").replace("-", "")

    # Verifica se tem 11 dígitos e se não é uma sequência repetida (ex: 111.111.111-11)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Validação do primeiro dígito verificador
    total = sum(int(cpf[i]) * (10 - i) for i in range(9))
    remainder = (total * 10) % 11
    if remainder == 10:
        remainder = 0
    if remainder != int(cpf[9]):
        return False

    # Validação do segundo dígito verificador
    total = sum(int(cpf[i]) * (11 - i) for i in range(10))
    remainder = (total * 10) % 11
    if remainder == 10:
        remainder = 0
    if remainder != int(cpf[10]):
        return False

    return True