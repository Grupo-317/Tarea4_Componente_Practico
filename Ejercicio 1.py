
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
class EntidadSistema(ABC):# Clase abstracta para entidades del sistema
    def __init__(self):# Inicializador que marca la fecha de creación
        self.fecha_registro = datetime.datetime.now() # Guarda la fecha actual

    @abstractmethod # Define un método que obliga a las subclases a implementarlo
    def mostrar_detalle(self): # Método abstracto para mostrar información o detalle
        """ Garantiza la salida de información de cada subclase de manera correcta"""
        pass
    # CREACION DE LA CLASE ABSTRACTA SERVICIOS 
class Servicio(EntidadSistema, ABC):  # Clase base para todos los servicios
    def __init__(self, nombre, precio_base):  # Inicia con nombre y precio
        super().__init__()  # Llama al constructor de la clase base
        self.nombre = nombre  # Define el nombre del servicio
        self.precio_base = precio_base  # Define el precio base del servicio

    @abstractmethod  # Método abstracto de cálculo de costos
    def calcular_costo(self, *args, **kwargs):  # Firma para cálculos específicos
        pass

    def aplicar_iva(self, base, iva=0.19):  # Método para aplicar impuestos
        """Método para simular sobrecarga y cálculos base."""
        return base * (1 + iva)  # Retorna el valor con impuesto