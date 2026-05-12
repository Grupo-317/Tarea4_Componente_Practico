
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
class ErrorClienteNoEncontrado(ErrorSistemaFJ): # Excepcion para errores donde no se encuentre un registro de un cliente.
    """ Indica cuando un cliente no se encuentra registrado en el sistema"""
    pass
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
            LoggerSistema.registrar_evento(f" Causas : {excepcion.__cause__}", "Error") # Muestra mensajes. 
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
        return self.aplicar_impuesto(total) if aplicar_impuesto else total
         
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
        return f" Reserva #{self._id} | {self.servicio.nombre} | Estado: {self.estado} | Total: ${self.costo_total:,.2f}"
    
    def validar_datos(self): return self.cliente and self.servicio # Verifica que la reserva tenga un cliente y un servicio asignados para ser correcta. 
#    CREACION DEL SISTEMA DE GESTION
class SistemaFJ:
    def __init__(self):
        self.clientes = {} # Diccionario para buscar clientes rapido por su correo.
        self.servicios = {} # Diccionario para buscar servicios por su codigo.
        self.reservas_globales = [] # Lista que guarda el historial de todas las ventas
        self._precargar_datos() # Ejecuta la carga de servicios de prueba automáticamente

    def _precargar_datos(self):
        self.servicios["S1"] = ReservaSala("Sala de Juntas", 50000)  # Nombre del servicio y su costo
        self.servicios["S2"] = AlquilerEquipos("Laptop Pro", 35000) # Nombre del servicio y su costo
        self.servicios["S3"] = AsesoriaEspecializada("Consultoría Python ", 120000) # Nombre del servicio y su costo
      #  Crea un nuevo cliente y lo guarda en el sistema. Verifica que el correo no esté repetido para evitar errores.
    def registrar_cliente(self, nombre, correo): # Registar nombre y correo del cliente.
        if correo in self.clientes: raise DatosInvalidosError("El correo ya existe") # Mensaje de error
        nuevo = Cliente(nombre, correo)
        self.clientes[correo] = nuevo  # Guarda al cliente usando el correo.
        print(f" Cliente {nombre} registrado exitosamente.") # mensaje cuando el registro es valido
        # Une a un Cliente con un Servicio para generar una transacción final.
    def crear_reserva(self, correo_cli, id_serv, cantidad, **params):
        if correo_cli not in self.clientes:
            raise  ErrorClienteNoEncontrado("Cliente no registrado") # Mensaje cuando el cliente no se encuentra registrado.
        if id_serv not in self.servicios:
            raise ServicioNoDisponibleError("El codigo de servicio no existe")  # Mensaje cuando el codigo del servicio no existe.
        
        reserva = Reserva(self.clientes[correo_cli], self.servicios[id_serv], cantidad, **params) # Se crea el objeto Reserva uniendo los datos del cliente y el servicio
        try: 
            resultado = reserva.procesar() # Se llama al método que calcula costos, IVA y valida disponibilidad
            self.reservas_globales.append(reserva) # Se guarda la reserva en el historial global para reportes futuros
            print(resultado) # Muestra el recibo final o el error capturado
        except Exception as e :
            LoggerSistema.registrar_error (e, "crear_reserva")
            print( f" No se puede craer la reserva: {e}")

    def ejecutar_simulacion_10_ops(self):
        print("\n" + "="*20 + " INICIANDO SIMULACIÓN " + "="*20)
        ops = [
            ("1. Registro Cliente OK", lambda: self.registrar_cliente("Mateo Ruiz", "mateo@dev.com")), # Prueba registro exitoso.
            ("2. Registro Cliente Error", lambda: self.registrar_cliente("A", "error-mail")), # Prueba validacion de nombre corto o correo.
            ("3. Creación Servicio OK", lambda: self.registrar_servicio("1", "S10", "Auditorio", 200000)),# Prueba creacion de servicio.
            ("4. Reserva OK (Sala)", lambda: self.crear_reserva("mateo@dev.com", "S1", 4, aplicar_impuesto=True)),# Prueba venta con IVA.
            ("5. Reserva Error (Financiero)", lambda: self.crear_reserva("mateo@dev.com", "S1", 2, descuento=500000)),# Prueba descuento excesivo.
            ("6. Reserva OK (Equipo)", lambda: self.crear_reserva("mateo@dev.com", "S2", 3, incluye_seguro=True)),# Prueba venta con seguro.
            ("7. Reserva Error (Dato Inv)", lambda: self.crear_reserva("mateo@dev.com", "S2", -10)),# Prueba validacion de cantidad negativa.
            ("8. Reserva OK (Asesoría)", lambda: self.crear_reserva("mateo@dev.com", "S3", 2, tipo="PREMIUM")),# Prueba tarifa especial.
            ("9. Error (Cliente No Existe)", lambda: self.crear_reserva("desconocido@mail.com", "S1", 1)),# Prueba busqueda de cliente fallida.
            ("10. Cancelación Operativa", lambda: print(self.reservas_globales[0].cancelar() if self.reservas_globales else "No hay reservas")) # Prueba anulacion.
        ]
        # BUCLE DE PRUEBAS: Ejecuta cada operacion
        for desc, func in ops: # Itera sobre la lista 'ops' obteniendo descripcion y la funcion lambda.
            try:
                print(f"\n {desc}:") # Imprime el nombre del escenario actua.
                func() # Ejecuta la logica de la prueba.
            except Exception as e: # Captura cualquier error.
                print(f" Error Capturado: {e}") # Mensaje de error.
        print("\n" + "="*60)    
    def registrar_servicio(self, tipo, codigo, nombre, precio):
        cod = codigo.upper() # Convierte el codigo a mayusculas para estandarizar.
        if tipo == "1": nuevo = ReservaSala(nombre, precio) # Instancia objeto para reserva de salas.
        elif tipo == "2": nuevo = AlquilerEquipos(nombre, precio) # Instancia objeto para equipos.
        elif tipo == "3": nuevo = AsesoriaEspecializada(nombre, precio) # Instancia objeto para asesorias.
        else: raise DatosInvalidosError("Tipo de servicio no reconocido")  # Mensaje de error.
        self.servicios[cod] = nuevo
        print(f" Servicio '{nombre}' guardado con código {cod}.")    # Confirma el registro del servicio 
    # CREACION DE LA  INTERFAZ DE USUARIO (MENÚ) 
def menu():
    sistema = SistemaFJ()
    while True:
        print("\n" + "—"*15 + " SOFTWARE FJ - SISTEMA INTEGRAL " + "—"*15)
        print("1. [Cliente nuevo]      2. [ Nuevos Servicios]    3. [ Listar Servicios]")
        print("4. [ Crear Reserva]     5. [ Listar Reserva]      6. [ Canselar Reserva] ")
        print("7. [Ver historial]      8.  [Ejecutar Test Automatico]")
        print("9. [Salir]")
        
        op = input("\nSeleccione una opcion: ")
        try:
            if op == "1":
                sistema.registrar_cliente(input("Nombre completo: "), input("Correo electronico: "))
            elif op == "2":
                print("Tipos: 1.Sala | 2.Equipo | 3.Asesoría")
                sistema.registrar_servicio(input("Tipo: "), input("Código (ej. S5): "), 
                                         input("Nombre: "), float(input("Precio base: ")))
            elif op == "3":
                print("\nCATÁLOGO DE SERVICIOS:")
                for k, v in sistema.servicios.items(): print(f"[{k}] {v.mostrar_detalle()}")
            elif op == "4":
                correo = input("Correo del cliente: ")
                id_s = input("Código del servicio: ").upper()
                cant = float(input("Cantidad (horas/días/sesiones): "))
                sistema.crear_reserva(correo, id_s, cant)
            elif op == "5":
                print("\nHISTORIAL DE RESERVAS:")
                for r in sistema.reservas_globales: print(r.mostrar_detalle())
            elif op == "6":
                # Cancelar la última reserva como ejemplo o pedir ID
                if not sistema.reservas_globales:
                    print("No hay reservas para cancelar.")
                else:
                    idx = int(input(f"Ingrese índice de reserva (0 a {len(sistema.reservas_globales)-1}): "))
                    print(sistema.reservas_globales[idx].cancelar())
            elif op == "7":
                try:
                    with open("log_software_fj.txt", "r", encoding="utf-8") as f:
                        print("\n" + "—"*10 + " CONTENIDO DEL LOG " + "—"*10)
                        print(f.read())
                except FileNotFoundError: print("El archivo de log aún no se ha creado.")
            elif op == "8":
                sistema.ejecutar_simulacion_10_ops()
            elif op == "9":
                print("Cerrando sistema ¡Adios!")
                break
            else:
                print(" Opcion no valida, intente nuevamente.")
        except ValueError:
            mensage = "Error de entrada: Se esperaba un número y se recibió texto."
            print(f" {mensage}")
            LoggerSistema.registrar_evento(mensage, "ERROR")
        except Exception as e:
            print(f"Error inesperado: {e}")
            LoggerSistema.registrar_error(e, "Interfaz_Usuario")

if __name__ == "__main__":
    menu()


    