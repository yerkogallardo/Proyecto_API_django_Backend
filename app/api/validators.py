import os
from django.core.exceptions import ValidationError

EXTENSIONES_PERMITIDAS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']

def custom_validate_file(value):     #el parametro value es un objeto de tipo UploadedFile de django. representa el archivo
    #que se está subiendo y tiene atributos como .name, .size, .content_type
    """
    Valida que el archivo subido tenga una extensión permitida.
    """
    ext = os.path.splitext(value.name)[1].lower()     #extrae extension del archivo
    if ext not in EXTENSIONES_PERMITIDAS:
        raise ValidationError(f"Extensión no permitida: {ext}. Solo se permiten {', '.join(EXTENSIONES_PERMITIDAS)}.")
    
    return value     #si pasa validacion, devuelve archivo sin errores





# NO ES IMPORTANTE EN ESTE MOMENTO, MAS ADELANTE TAL VEZ SEGUN NECESIDADES DEL CLIENTE