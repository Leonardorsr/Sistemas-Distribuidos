"""
Funções utilitárias
"""
from functools import wraps
from flask import jsonify, request
from typing import Callable, Any


def json_response(success: bool = True, data: Any = None, 
                 message: str = '', status_code: int = 200):
    """Padroniza respostas JSON"""
    response = {
        'success': success,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code


def handle_errors(f: Callable) -> Callable:
    """Decorator para tratamento de erros"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return json_response(
                success=False, 
                message=f'Erro de validação: {str(e)}',
                status_code=400
            )
        except Exception as e:
            print(f"Erro não esperado: {e}")
            return json_response(
                success=False,
                message='Erro interno do servidor',
                status_code=500
            )
    return decorated_function


def validate_required_fields(data: dict, fields: list) -> None:
    """Valida se campos obrigatórios estão presentes"""
    missing = [field for field in fields if field not in data]
    if missing:
        raise ValueError(f"Campos obrigatórios faltando: {', '.join(missing)}")
