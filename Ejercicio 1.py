
# Sistema Integral de Gestión de Clientes, Servicios y 
# reservas, el sistema debe incluir clases abstractas, clases derivadas, métodos
# sobrecargados, manejo de listas internas y validaciones estrictas,
# demostrando un diseño orientado a objetos completamente funcional.

import datetime
from abc import ABC, abstractmethod

# GESTIÓN DE ERRORES ESPECÍFICOS 
class ErrorSistemaFJ(Exception): # Define la clase base para errores del sistema
    """ clase donde se identifican todos los errores dentro del sistema"""
    pass
class DatosInvalidosError(ErrorSistemaFJ): # Excepción cuando los datos fallan
    """ Indica cuando los datos de entrada no cumplen las validaciones"""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ): # Excepción para servicios inactivos
    """ Indica cuando el servicio solicitado no puede ser procesado"""
    pass

class ErrorFinanciero(ErrorSistemaFJ): # Excepción para errores de cálculos
    """ Indica inconsistencias en cálculos de costos o descuentos"""
    pass
#  CREACION DE LA CLASE ABSTRACTA
class EntidadSistema(ABC):
    def __init__(self):
        self.fecha_registro = datetime.datetime.now()

    @abstractmethod
    def mostrar_detalle(self):
        """ Garantiza la salida de información de cada subclase de manera correcta"""
        pass