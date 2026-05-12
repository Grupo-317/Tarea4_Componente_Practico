
# Sistema Integral de Gestión de Clientes, Servicios y 
# reservas, el sistema debe incluir clases abstractas, clases derivadas, metodos
# sobrecargados, manejo de listas internas y validaciones estrictas,
# demostrando un diseño orientado a objetos completamente funcional.

import datetime
from abc import ABC, abstractmethod
import traceback

# GESTIÓN DE ERRORES ESPECÍFICOS 
class ErrorSistemaFJ(Exception): # Define la clase base para errores del sistema.
    """ clase donde se identifican todos los errores dentro del sistema"""
    pass
class DatosInvalidosError(ErrorSistemaFJ): # Excepcion cuando los datos fallan.
    """ Indica cuando los datos de entrada no cumplen las validaciones"""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ): # Excepcion para servicios inactivos.
    """ Indica cuando el servicio solicitado no puede ser procesado"""
    pass

class ErrorFinanciero(ErrorSistemaFJ): # Excepcion para errores de cálculos.
    """ Indica inconsistencias en cálculos de costos o descuentos"""
    pass
class ErrorClienteNoEncontrados(ErrorSistemaFJ): # Excepcion para errores donde no se encuentre un registro de un cliente.
    """ Indica cuando un cliente no se encuentra registrado en el sistema"""
# CREACION DEL SISTEMA DE LOGS
class LoggerSistema: # Creacion de la clase para el sistema. 
    @staticmethod
    def registrar_evento(mensaje, nivel="Informacion"):# Define como recibir el mensaje y su etiqueta de importancia.
        try:
            with open("log_software_fj.txt", "a", encoding="utf-8") as archivo: # # Abre el archivo para escibir el mensaje.
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Crea la marca de tiempo actual.
                archivo.write(f"[{timestamp}] [{nivel}] {mensaje}\n") # Escribe la línea final en el archivo.
        except IOError as e:
            print(f" Error: No se puede acceder al archivo de registro {e}")   # Muestra mensaje de error.

    @staticmethod
    def registrar_error(excepcion, contexto=""): # Muestra y guarda el mensaje de error.
        mensaje = f"{contexto} - {type(excepcion).__name__}: {str(excepcion)}" # Muestra de mensaje de error detectado.
        LoggerSistema.registrar_evento(mensaje, "ERROR") # Muestra y  guarda el mensaje de error detectado.
        # El encadenamiento de excepciones se captura aquí si existe
        if excepcion.__cause__:
            LoggerSistema.registrar_evento(f" Motivos por el cual : {excepcion.__cause__}", "Informacion incorrecta") # Muestra mensajes. 
    pass
#  CREACION DE LA CLASE ABSTRACTA
class EntidadSistema(ABC):# Clase abstracta para entidades del sistema.
    def __init__(self):# Inicializador que marca la fecha de creacion
        self.fecha_registro = datetime.datetime.now()
        self._id = int(datetime.datetime.now().timestamp() * 1000)        
    @abstractmethod  # Define un metodo que obliga a las subclases a implementarlo.
    def mostrar_detalle(self): # Metodo abstracto para mostrar información o detalle.
        """ Garantiza la salida de información de cada subclase de manera correcta"""
        pass
    @abstractmethod
    def validar_datos(self): 
        pass
    # CREACION DE LA CLASE ABSTRACTA SERVICIOS 
class Servicio(EntidadSistema, ABC):  # Clase base para todos los servicios.
    def __init__(self, nombre, precio_base):  # Inicia con nombre y precio.
        super().__init__()  # Llama al constructor de la clase base.
        self.nombre = nombre  # Define el nombre del servicio.
        self.precio_base = precio_base  # Define el precio base del servicio.
        self.disponible = True
    @abstractmethod  # Método abstracto de cálculo de costos.
    def calcular_costo(self, *args, **kwargs):  # Firma para calculos especificos.
        pass

    def aplicar_impuesto(self, base, iva=0.19):  # Metodo para aplicar impuestos.
        """Método para simular sobrecarga y cálculos base."""
        return base * (1 + iva)  # Retorna el valor con impuesto.
#    CREACION DE LA CLASE CLIENTE "ENCAPSULAMIENTO"
class Cliente(EntidadSistema): # Creamos la clase Cliente
    def __init__(self, nombre, correo, telefono=""):
        super().__init__()
        self.nombre = nombre  # Guarda el nombre
        self.correo = correo   # Guarda el correo
        self.telefono = telefono  # Guarda el telefono
        self.reservas = [] 

    @property
    def nombre(self): return self.__nombre # Muestra el nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3: # Se evidencia cual es la condicion, para que el dato ingresado sea valido.
            raise DatosInvalidosError(" Ingrese el nombre correctamente, minimo  tres carateres") # Muestra un mensaje de error.
        self.__nombre = valor.strip()

    @property
    def correo(self): return self.__correo # Muestra el correo

    @correo.setter
    def correo(self, valor):
        if "@" not in valor or "." not in valor: # Revisa que el correo tenga un '@' y un '.' para que sea valido
            raise DatosInvalidosError(f"Email incorrecto: {valor}") # Muestra un mensaje de error.
        self.__correo = valor

    def validar_datos(self): 
        return len(self.__nombre) > 0 and "@" in self.__correo #  devuelve 'True' si el nombre  y el correo son correctos.
        
    def mostrar_detalle(self):
        return f"Cliente: {self.nombre} | Email: {self.correo}"    # Muestra en pantalla cliente: nombre y correo.       
class ReservaSala(Servicio):  # Subclase para reserva de salas.
    def calcular_costo(self, horas, descuento=0, aplicar_impuesto=False):
        if float(horas) <= 0: raise DatosInvalidosError("Las horas deben ser positivas") # Valida que no se ingresen horas negativas o cero
        total = (self.precio_base * float(horas)) - descuento # Calcula: Precio por hora * cantidad de horas y le resta el descuento. 
        if total < 0: raise ErrorFinanciero("El descuento excede el costo") # Mensaje de error 
        return self.aplicar_impuestos(total) if aplicar_impuesto else total
         
    def mostrar_detalle(self): return f" SALA: {self.nombre} (${self.precio_base}/h)" # Muestra el nombre de la sala y cuánto cuesta cada hora
    def validar_datos(self): return self.precio_base > 0 # Revisa que el precio de la sala sea mayor a cero para ser valido
        
class AlquilerEquipos(Servicio): # Subclase para alquiler de equipos.
    def calcular_costo(self, dias, incluye_seguro=False):# Metodo para calcular costos.
        costo = self.precio_base * float(dias)  
        if incluye_seguro: costo *= 1.15 # Muestra el nombre del equipo y su costo por día
        return costo
    def mostrar_detalle(self): return f" EQUIPO: {self.nombre} (${self.precio_base}/día)" # Muestra el nombre del equipo y su costo por día
    def validar_datos(self): return self.precio_base > 0 # Asegura que no se alquilen equipos con precio base de $0

class AsesoriaEspecializada(Servicio): # Subclase para asesoria especialisadas.
    def calcular_costo(self, sesiones, tipo="ESTANDAR"):
        costo = self.precio_base * int(sesiones)
        if str(tipo).upper() == "PREMIUM": costo *= 0.85 # Si la asesoría es "PREMIUM", se aplica un descuento.
        return costo

    def mostrar_detalle(self): return f" ASESORÍA: {self.nombre} (${self.precio_base} base)" # Muestra el tipo de asesoría y su precio base
    def validar_datos(self): return self.precio_base > 0   # Verifica que la asesoría tenga un precio definido

class Reserva(EntidadSistema):# Define la subcase reserva que hereda de EntidadSistema.
    def __init__(self, cliente, servicio, cantidad, **params):# prepara los datos necesario para registrar una nueva reserva.
        super().__init__() # Constructor base
        self.cliente = cliente  #Guarda el objeto Cliente que está haciendo la compra.
        self.servicio = servicio # registra la informacion de las compras que hace el cliente.
        self.cantidad = cantidad  # Registra la informacion del producto en el momento de su compra:Hora,dia o sesiones.
        self.params = params  # Registra otro tipo de informacion dada por el cliente.
        self.estado = "PENDIENTE" # Define que la reserva inicia en espera hasta que se procese el pago.
        self.costo_total = 0 # Inicializa el contador de dinero en cero antes de realizar el cálculo.

    def procesar(self): # Este método intenta completar la compra y calcular el dinero total.
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError("Servicio no disponible") # Mensaje de error
            
            try:
                self.costo_total = self.servicio.calcular_costo(self.cantidad, **self.params)  #Intenta completar la compra y calcular el dinero total.
            except Exception as e:
                # Encadenamiento de excepciones solicitado
                raise ErrorFinanciero("Fallo en el calculo financiero interno") from e  # Mensaje de error
                # Si ocurre cualquier error conocido durante el proceso   
        except (ServicioNoDisponibleError, ErrorFinanciero, DatosInvalidosError) as e:
            self.estado = "ERROR" # Cambia el estado para saber que algo salio mal.
            LoggerSistema.registrar_error(e, f"Reserva {self._id}") # Guarda el error
            raise ErrorSistemaFJ(f"No se pudo completar la reserva: {e}")  # Mensaje de error
        else:
            self.estado = "CONFIRMADA" # Marca la reserva como exitosa.
            self.cliente.reservas.append(self) # Guarda esta reserva.
            LoggerSistema.registrar_evento(f"Reserva Confirmada ID {self._id}") # Registra el éxito
            return f" Confirmada. Total: ${self.costo_total:,.2f}" # Muestra el precio final con 2 decimales
        finally:
            LoggerSistema.registrar_evento(f"Intento de procesamiento ID {self._id} finalizado.")

    def cancelar(self): # Metodo para anular una reserva que ya existe.
        if self.estado == "CANCELADA":
            return "La reserva ya estaba cancelada." # Mensaje de que la reserva ya esta cancelada.
        self.estado = "CANCELADA" # Cambia el estado a cancelado.
        LoggerSistema.registrar_evento(f"Reserva {self._id} Cancelada por el usuario.")
        return f" Reserva #{self._id} ha sido cancelada."

    def mostrar_detalle(self):# Crea un resumen visual de la factura o recibo 
        return f"📅 Reserva #{self._id} | {self.servicio.nombre} | Estado: {self.estado} | Total: ${self.costo_total:,.2f}"
    
    def validar_datos(self): return self.cliente and self.servicio # Verifica que la reserva tenga un cliente y un servicio asignados para ser correcta.  



    # CREACION DE LA CLASE CLIENTE (Encapsulacion y Validaciones) 
class Cliente(EntidadSistema):  # Clase Cliente.
    def __init__(self, nombre, correo):  # Nombre y correo del cliente. 
        super().__init__()  # Llama al constructor base.
        self.nombre = nombre  # Usa el setter para validar si la informacion es correcta.
        self.correo = correo  # Usa el setter para validar si la informacion ingresada es correcta. 

    @property  # Define getter para nombre.
    def nombre(self): return self.__nombre  # Retorna atributo privado.

    @nombre.setter  # Define setter para nombre.
    def nombre(self, valor):  # Valida nombre.
        if not valor or len(valor) < 3:  # Verifica longitud minima.
            raise DatosInvalidosError(" El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor  # Asigna valor si es correcto.

    @property  # Define getter para correo
    def correo(self): return self.__correo  # Retorna atributo privado.

    @correo.setter  # Define setter para correo.
    def correo(self, valor):  # Valida correo.
        if "@" not in valor or "." not in valor:  # Verifica formato.
            raise DatosInvalidosError(f"Formato '{valor}' es incorrecto.")
        self.__correo = valor  # Asigna valor si es correcto.

    def mostrar_detalle(self):  # Implementacion del metodo abstracto.
        return f"[CLIENTE] {self.nombre} ({self.correo})"
# CREACION DE LA CLASE RESERVA (Gestion y Excepciones)
class Reserva(EntidadSistema):  # Define la subclase Reserva que hereda de EntidadSistema.
    def __init__(self, cliente, servicio, cantidad, **params): # Prepara los datos necesarios para registrar una nueva reserva.
        super().__init__()  # Constructor base
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise DatosInvalidosError(" Error. Ingrese los datos de manera correcta, por favor.") # Mensaje de error 
        
        self.cliente = cliente  # 
        self.servicio = servicio  # registra la informacion de las compras que hace el cliente.
        self.cantidad = cantidad  # Registra la informacion del producto en el momento de su compra:Hora,dia o sesiones.
        self.params = params  # Registra otro tipo de informacion dada por el cliente.
        self.estado = "Registrada"  # Marca el inicio de la reserva en el sistema.
    def procesar(self):  # Mostrar en pantalla que servicio se esta atendiendo 
        print(f"Procesando la informacion: {self.servicio.nombre} de {self.cliente.nombre}...")
        try:  # Bloque para manejo de errores
            if self.estado == "PROCESADA":  # Valida si la reserva se completo de manera correcta.
                raise ServicioNoDisponibleError("Error, esta informacion ya fue procesada.") # Mensaje de error. 

            total = self.servicio.calcular_costo(self.cantidad, **self.params) # Ejecuta polimorfismo.
            self.estado = "PROCESADA"  # Marca como éxito.
            return f"Felicidades su informacion es correcta: Total a pagar: ${total:,.2f}" # Mensaje cuando la informacion se ingresa de manera correcta.

        except (DatosInvalidosError, ErrorFinanciero) as e: # Captura errores de negocio.
            self.estado = "Error informacion incorrecta"  # Mensaje de error cuando la informacion  es invalida.
            raise ErrorSistemaFJ(f"Error, datos ingresados de forma invalida: {e}") from e # Mensaje de  error.
        
        except Exception as e:  # Captura otros errores.
            self.estado = "Error en el sistema"  # Actualiza estado a error a travez de este mensaje.
            raise ErrorSistemaFJ(f"Error, se evidencia fallas en el sistema : {e}") from e # Mensaje de error.
        
        finally:  # Bloque que siempre se ejecuta al final.
            print(f"Estado final: {self.estado}") # Se evidencia un mensaje de  resultado final.

    def mostrar_detalle(self):  # Implementacion  del metodo abstracto.
        return f"[RESERVA] Cliente: {self.cliente.nombre} | Estado: {self.estado}"
def registrar_log(mensaje, nivel="Sistema"):  # Función para registrar log.
    try:  # Intenta abrir el archivo.
        with open("log_software_fj.txt", "a", encoding="utf-8") as f:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Formato de la fecha.
            f.write(f"[{ts}] [{nivel}] {mensaje}\n") # Escribe el registro.
    except IOError as e: 
        print(f" Error, No se pudo escribir en log: {e}") # Mensaje de error si no hay acceso al archivo.
    # SIMULACIÓN De LAS 10 OPERACIONES
def ejecutar_sistema():# Funcion principal para que se ejecute todo el sistema.
    print(""+"="*60)
    print("Sistema Integral De Gestion De La Empresa Sotware FJ\n") # Titulo del sistema.
    print("="*60)
    
    
    # Crear servicios
    s1 = ReservaSala(" Sala principal", 150000)  # Nombre del servicio y su precio. 
    s2 = AlquilerEquipos(" Laptop 5.ª Gen", 45000) # Nombre del servicio y su precio.
    s3 = AsesoriaEspecializada("Sistemas Operativos", 80000)# Nombre del servicio y su precio.
    # Crear clientes válidos, identificando error si se ingresa de manera correcta.
    try:
        c1 = Cliente("Gertrudiz Carvajal Cuchimba", "gertrudiz@unad.edu.co")# Nombre y correo del cliente 1.
        c2 = Cliente("Maria Gomez", "maria@gmail.com")# Nombre y correo del cliente 2.
    except ErrorSistemaFJ as e:# Atrapa errores de datos ingresados por el cliente.
        print(f"Error: la informacion ingresada no es valida: {e}") # Mensaje de error.
        return
    # Definir 10 operaciones entre correctas e incorretas
    operaciones = [
        lambda: Reserva(c1, s1, 3, aplicar_impuesto=True).procesar(), # Operacion  correcto
        lambda: Reserva(c1, s1, 1, descuento=150000).procesar(),      # Operacion incorrecto
        lambda: Reserva(c2, s2, 2, incluye_seguro=True).procesar(),   # Operacion correcto
        lambda: Reserva(c1, s2, -1).procesar(),                       # Operacion incorrecto 
        lambda: Reserva(c1, s3, 5, tipo_cliente="PREMIUM").procesar(),# Operacion correcto
        lambda: Reserva(c2, s1, "seis horas").procesar(),             # Operacion incorrecto
        lambda: Reserva(c2, s2, 1, incluye_seguro=False).procesar(),  # Operacion correcto
        lambda: Reserva(c1, s1, 9, descuento=30000).procesar(),       # Operacion correcto
        lambda: Cliente("PA", "error@test.com"),                      # Operacion incorrecto
        lambda: Cliente("Pedro", " correo invalido"),                 # Operacion incorrecto
    ]
    for i, op in enumerate(operaciones, 1): 
        print(f"\n ||  EJECUTANDO OPERACION #{i}||") # Se evidencia un mensaje con la palabra "EJECUTANDO OPERACION" de numero  1 al 10.
        try:
            resultado = op() # Se ejecuta las 10 operaciones con la funcion Lambda.
            if resultado:  # Evidencia si hay un resultado exitoso.
                print(resultado) # Muestra el total a pagar. 
                registrar_log(f"Operacion {i}: {resultado}") # Guarda en registra_log.
            else:
                # Caso de creación de clientes exitosa (aunque en la lista fallan)
                print("Proceso exitoso") # Muestra mensaje si es correcto.
        except ErrorSistemaFJ as e: # Captura los errores.
            mensaje = f"Excepcion controlada: {e}" # Muestra mensaje si es correcto.
            print(mensaje)
            registrar_log(mensaje, "ERROR") # Muestra mensaje si es incorrecto.
        except Exception as e:
            mensaje = f"Error: en el sistema: {e}"# Muestra mensaje si es incorrecto.
            print(mensaje)
            registrar_log(mensaje, " Emergencia") # Muestra mensaje si es incorrecto.

    print("\n" + "="*50)
    print("SISTEMA FINALIZADO. Revise 'log_software_FJ.txt'.") # Muestra mensaje de cierre del sistema.
    print("="*50)

if __name__ == "__main__":
    ejecutar_sistema()  # Llama a la función principal                 