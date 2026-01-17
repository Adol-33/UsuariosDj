""" Archivo para procesadores de contexto globales """

from datetime import datetime

def fecha_actual(request):
    """ Modulo que retorna la fecha actual """
#    Retorna la fecha actual para el contexto global
    return {
        'fecha': datetime.now()
    }
