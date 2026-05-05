
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
class ReservaSala(Servicio):  # Subclase para reserva de salas
    def calcular_costo(self, horas, descuento=0, aplicar_impuesto=False):
        if not isinstance(horas, (int, float)) or horas <= 0:  # Valida tipo y valor
            raise DatosInvalidosError(f"Horas inválidas: {horas}")  # Anuncia la  excepción
        
        costo = (self.precio_base * horas) - descuento  # Calcula el costo final
        if costo < 0:  # Valida que el costo no sea negativo
            raise ErrorFinanciero("El descuento es mayor al costo.")  # Anuncia la excepción
            
        if aplicar_impuesto:  # Aplica impuestos si se requiere el servicio
            costo = self.aplicar_iva(costo)  
        return costo  # Retorna el costo calculado

    def mostrar_detalle(self):  # Implementación del método abstracto
        return f"[SERVICIO] Sala: {self.nombre} | Tarifa: ${self.precio_base}/hr"
class AlquilerEquipos(Servicio):  # Subclase para alquiler de equipos
    def calcular_costo(self, dias, incluye_seguro=False): # Método para calcular costos
        if not isinstance(dias, (int, float)) or dias <= 0: # Valida los días para evitar errores 
            raise DatosInvalidosError(f"Días inválidos: {dias}") # Muestra el mensaje de Error 
        
        recargo = 1.15 if incluye_seguro else 1.0  # Calcula recargo por seguro
        return (self.precio_base * dias) * recargo  # Retorna costo total

    def mostrar_detalle(self):  # Implementación del método abstracto
        return f"[SERVICIO] Equipo: {self.nombre} | Tarifa: ${self.precio_base}/día"
class AsesoriaEspecializada(Servicio):  # Subclase para asesorías especializadas 
    def calcular_costo(self, sesiones, tipo_cliente="ESTANDAR"): # Metodo para calcular costos
        if not isinstance(sesiones, (int, float)) or sesiones <= 0: # Valida sesiones
            raise DatosInvalidosError(f"Sesiones inválidas: {sesiones}") # Muestra el mensaje de Error 
        
        descuento = 0.85 if tipo_cliente.upper() == "PREMIUM" else 1.0 # Aplica descuento
        return (self.precio_base * sesiones) * descuento # Calcula y retorna el costo total aplicando el descuento por sesiones

    def mostrar_detalle(self):  # Implementación del método abstracto
        return f"[SERVICIO] Asesoría: {self.nombre} | Tarifa: ${self.precio_base}/sesión"
    # CREACION DE LA CLASE CLIENTE (Encapsulación y Validaciones) 
class Cliente(EntidadSistema):  # Clase Cliente
    def __init__(self, nombre, correo):  # Nombre y correo del cliente 
        super().__init__()  # Llama al constructor base
        self.nombre = nombre  # Usa el setter para validar si la informacion es correcta
        self.correo = correo  # Usa el setter para validar si la informacion ingresada es correcta 

    @property  # Define getter para nombre
    def nombre(self): return self.__nombre  # Retorna atributo privado

    @nombre.setter  # Define setter para nombre
    def nombre(self, valor):  # Valida nombre
        if not valor or len(valor) < 3:  # Verifica longitud mínima
            raise DatosInvalidosError("Nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor  # Asigna valor si es correcto

    @property  # Define getter para correo
    def correo(self): return self.__correo  # Retorna atributo privado

    @correo.setter  # Define setter para correo
    def correo(self, valor):  # Valida correo
        if "@" not in valor or "." not in valor:  # Verifica formato
            raise DatosInvalidosError(f"Formato '{valor}' es incorrecto.")
        self.__correo = valor  # Asigna valor si es correcto

    def mostrar_detalle(self):  # Implementación del método abstracto
        return f"[CLIENTE] {self.nombre} ({self.correo})"
# CREACION DE LA CLASERESERVA (Gestión y Excepciones)
class Reserva(EntidadSistema):  # Define la subclase Reserva que hereda de EntidadSistema
    def __init__(self, cliente, servicio, cantidad, **params): # Prepara los datos necesarios para registrar una nueva reserva.
        super().__init__()  # Constructor base
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise DatosInvalidosError(" Error. Ingrese los datos de manera correcta, por favor.") # Mensaje de error 
        
        self.cliente = cliente  # Registra la informacion del cliente que hace la reserva
        self.servicio = servicio  # registra la informacion de las compras que hace el cliente
        self.cantidad = cantidad  # Registra la informacion del producto en el momento de su compra:Hora,día o sesiones.
        self.params = params  # Registra otro tipo de informacion dada por el cliente.
        self.estado = "Registrada"  # Marca el inicio de la reserva en el sistema.
    def procesar(self):  # Mostrar en pantalla que servicio se esta atendiendo 
        print(f"Procesando la informacion: {self.servicio.nombre} de {self.cliente.nombre}...")
        try:  # Bloque para manejo de errores
            if self.estado == "PROCESADA":  # Valida si la reserva se completo de manera correcta.
                raise ServicioNoDisponibleError("Error, esta informacion ya fue procesada.") # Mensaje de error. 

            total = self.servicio.calcular_costo(self.cantidad, **self.params) # Ejecuta polimorfismo.
            self.estado = "PROCESADA"  # Marca como éxito
            return f"Felicidades su informacion es correcta: Total a pagar: ${total:,.2f}" # Mensaje cuando la informacion se ingresa de manera correcta.

        except (DatosInvalidosError, ErrorFinanciero) as e: # Captura errores de negocio.
            self.estado = "Error informacion incorrecta"  # Mensaje de error cuando la informacion  es invalida.
            raise ErrorSistemaFJ(f"Error, datos ingresados de forma invalida: {e}") from e # Mensaje de  error
        
        except Exception as e:  # Captura otros errores.
            self.estado = "Error en el sistema"  # Actualiza estado a error a travez de este mensaje.
            raise ErrorSistemaFJ(f"Error, se evidencia fallas en el sistema : {e}") from e # Mensaje de error.
        
        finally:  # Bloque que siempre se ejecuta al final
            print(f"Estado final: {self.estado}") # Se evidencia un mensaje de  resultado final.

    def mostrar_detalle(self):  # Implementacion  del método abstracto.
        return f"[RESERVA] Cliente: {self.cliente.nombre} | Estado: {self.estado}"
    def registrar_log(mensaje, nivel="Sistema"):  # Función para registrar log.
        try:  # Intenta abrir el archivo
            with open("log_software_fj.txt", "a", encoding="utf-8") as f:
                 ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Formato fecha
                 f.write(f"[{ts}] [{nivel}] {mensaje}\n") # Escribe el registro
        except IOError as e: 
            print(f" Error, No se pudo escribir en log: {e}") # Mensaje de error si no hay acceso al archivo

      
