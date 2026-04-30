
# Sistema Integral de Gestión de Clientes, Servicios y 
# reservas, el sistema debe incluir clases abstractas, clases derivadas, métodos
# sobrecargados, manejo de listas internas y validaciones estrictas,
# demostrando un diseño orientado a objetos completamente funcional.

import datetime
from abc import ABC, abstractmethod

# GESTIÓN DE ERRORES ESPECÍFICOS 
class ErrorSistemaFJ(Exception): 
    """ clase donde se identifican todos los errores dentro del sistema"""
    pass
class DatosInvalidosError(ErrorSistemaFJ): 
    """ Indica cuando los datos de entrada no cumplen las validaciones"""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ): 
    """ Indica cuando el servicio solicitado no puede ser procesado"""
    pass

class ErrorFinanciero(ErrorSistemaFJ): 
    """ Indica inconsistencias en cálculos de costos o descuentos"""
    pass