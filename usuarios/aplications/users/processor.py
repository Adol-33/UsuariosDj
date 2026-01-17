""" Archivo para la generación de códigos aleatorios. """

import random # Importar el módulo random para generar números aleatorios
import string # Importar el módulo string para obtener caracteres predefinidos

def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Generates a random code consisting of uppercase letters and digits.

    Args:
        size (int): The length of the generated code. Default is 6.
        chars (str): The characters to choose from. Default is uppercase letters and digits.
    Returns:
        str: A randomly generated code.
    """
    # Generate a random code by selecting 'size' characters from 'chars'
    return ''.join(random.choice(chars) for _ in range(size)) # Generar el código aleatorio

