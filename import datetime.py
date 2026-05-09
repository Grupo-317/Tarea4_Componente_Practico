import datetime
from abc import ABC, abstractmethod

# --- 1. GESTIÓN DE ERRORES ESPECÍFICOS ---
class ErrorSistemaFJ(Exception):
    """Clase base para errores del sistema"""
    pass

class DatosInvalidosError(ErrorSistemaFJ):
    """Indica cuando los datos de entrada no cumplen las validaciones"""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Indica cuando el servicio solicitado no puede ser procesado"""
    pass

class ErrorFinanciero(ErrorSistemaFJ):
    """Indica inconsistencias en cálculos de costos o descuentos"""
    pass

# --- 2. CREACIÓN DE LA CLASE ABSTRACTA ---
class EntidadSistema(ABC):
    def __init__(self):
        self.fecha_registro = datetime.datetime.now()

    @abstractmethod
    def mostrar_detalle(self):
        pass

# --- 3. CLASES DE SERVICIOS (Polimorfismo) ---
class Servicio(EntidadSistema, ABC):
    def __init__(self, nombre, precio_base):
        super().__init__()
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass

    def aplicar_iva(self, base, iva=0.19):
        return base * (1 + iva)

class ReservaSala(Servicio):
    def calcular_costo(self, horas, descuento=0, aplicar_impuesto=False):
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise DatosInvalidosError(f"Horas inválidas: {horas}")
        
        costo = (self.precio_base * horas) - descuento
        if costo < 0:
            raise ErrorFinanciero("El descuento es mayor al costo.")
            
        if aplicar_impuesto:
            costo = self.aplicar_iva(costo)
        return costo

    def mostrar_detalle(self):
        return f"[SERVICIO] Sala: {self.nombre} | Tarifa: ${self.precio_base}/hr"

class AlquilerEquipos(Servicio):
    def calcular_costo(self, dias, incluye_seguro=False):
        if not isinstance(dias, (int, float)) or dias <= 0:
            raise DatosInvalidosError(f"Días inválidos: {dias}")
        
        recargo = 1.15 if incluye_seguro else 1.0
        return (self.precio_base * dias) * recargo

    def mostrar_detalle(self):
        return f"[SERVICIO] Equipo: {self.nombre} | Tarifa: ${self.precio_base}/día"

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, sesiones, tipo_cliente="ESTANDAR"):
        if not isinstance(sesiones, (int, float)) or sesiones <= 0:
            raise DatosInvalidosError(f"Sesiones inválidas: {sesiones}")
        
        descuento = 0.85 if tipo_cliente.upper() == "PREMIUM" else 1.0
        return (self.precio_base * sesiones) * descuento

    def mostrar_detalle(self):
        return f"[SERVICIO] Asesoría: {self.nombre} | Tarifa: ${self.precio_base}/sesión"

# --- 4. CLASE CLIENTE (Encapsulación) ---
class Cliente(EntidadSistema):
    def __init__(self, nombre, correo):
        super().__init__()
        self.nombre = nombre  # Llama al setter
        self.correo = correo  # Llama al setter

    @property
    def nombre(self): return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor) < 3:
            raise DatosInvalidosError("Nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor

    @property
    def correo(self): return self.__correo

    @correo.setter
    def correo(self, valor):
        if "@" not in valor or "." not in valor:
            raise DatosInvalidosError(f"Formato de correo '{valor}' es incorrecto.")
        self.__correo = valor

    def mostrar_detalle(self):
        return f"[CLIENTE] {self.nombre} ({self.correo})"

# --- 5. CLASE RESERVA ---
class Reserva(EntidadSistema):
    def __init__(self, cliente, servicio, cantidad, **params):
        super().__init__()
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Objetos Cliente o Servicio inválidos.")
        
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.params = params
        self.estado = "Registrada"

    def procesar(self):
        print(f"Procesando: {self.servicio.nombre} para {self.cliente.nombre}...")
        try:
            total = self.servicio.calcular_costo(self.cantidad, **self.params)
            self.estado = "PROCESADA"
            return f"Éxito: Total a pagar: ${total:,.2f}"
        except (DatosInvalidosError, ErrorFinanciero) as e:
            self.estado = "ERROR_DATOS"
            raise ErrorSistemaFJ(f"Fallo en validación de negocio: {e}")
        except Exception as e:
            self.estado = "ERROR_SISTEMA"
            raise ErrorSistemaFJ(f"Error inesperado: {e}")
        finally:
            print(f"Resultado final: {self.estado}")

    def mostrar_detalle(self):
        return f"[RESERVA] {self.cliente.nombre} - {self.servicio.nombre} ({self.estado})"

# --- 6. UTILIDADES DE LOGS ---
def registrar_log(mensaje, nivel="INFO"):
    try:
        with open("log_software_fj.txt", "a", encoding="utf-8") as f:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{ts}] [{nivel}] {mensaje}\n")
    except IOError as e:
        print(f"No se pudo escribir en log: {e}")

# --- 7. SIMULACIÓN (10 OPERACIONES) ---
def ejecutar_sistema():
    print("=== SISTEMA INTEGRAL SOFTWARE FJ - UNAD ===\n")
    
    # 1. Instanciar servicios
    s1 = ReservaSala("Auditorio A", 100000)
    s2 = AlquilerEquipos("Proyector 4K", 45000)
    s3 = AsesoriaEspecializada("Sistemas Operativos", 80000)
    
    # 2. Instanciar clientes válidos
    try:
        c1 = Cliente("Gertrudiz Carvajal Cuchimba", "gertrudiz@unad.edu.co")
        c2 = Cliente("Usuario Prueba", "prueba@correo.com")
    except ErrorSistemaFJ as e:
        print(f"Error fatal en clientes iniciales: {e}")
        return

    # 3. Definir 10 operaciones (Mezcla de válidas e inválidas)
    operaciones = [
        lambda: Reserva(c1, s1, 3, aplicar_impuesto=True).procesar(), # Válida
        lambda: Reserva(c1, s1, 1, descuento=150000).procesar(),      # Error Financiero
        lambda: Reserva(c2, s2, 2, incluye_seguro=True).procesar(),   # Válida
        lambda: Reserva(c1, s2, -1).procesar(),                       # Dato inválido (días < 0)
        lambda: Reserva(c1, s3, 5, tipo_cliente="PREMIUM").procesar(),# Válida
        lambda: Reserva(c2, s1, "muchas horas").procesar(),           # Error de tipo
        lambda: Reserva(c2, s2, 1, incluye_seguro=False).procesar(),  # Válida
        lambda: Reserva(c1, s1, 10, descuento=50000).procesar(),      # Válida
        lambda: Cliente("Ab", "error@test.com"),                      # Error Nombre corto
        lambda: Cliente("Pedro", "correo_sin_punto@com"),             # Error Formato correo
    ]

    for i, op in enumerate(operaciones, 1):
        print(f"\n--- OPERACIÓN #{i} ---")
        try:
            resultado = op()
            if resultado:
                print(resultado)
                registrar_log(f"Op {i}: {resultado}")
            else:
                # Caso de creación de clientes exitosa (aunque en la lista fallan)
                print("Operación de creación completada.")
                registrar_log(f"Op {i}: Creación exitosa")
        except ErrorSistemaFJ as e:
            msg = f"CAPTURADA: {e}"
            print(msg)
            registrar_log(msg, "ERROR")
        except Exception as e:
            msg = f"INESPERADO: {e}"
            print(msg)
            registrar_log(msg, "CRITICAL")

    print("\n" + "="*40)
    print("PROCESO FINALIZADO. Revise 'log_software_fj.txt'.")
    print("="*40)

if __name__ == "__main__":
    ejecutar_sistema()