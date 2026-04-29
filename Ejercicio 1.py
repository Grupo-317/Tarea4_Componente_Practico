# Create a system for a company dedicated to digital animation that requires a 
# specialized mathematical module to calculate surface areas and volumes 
# of different three-dimensional objects that will be rendered in 
# high-quality scenes.

import math
import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod

# --- 3D OBJECTS (OOP LOGIC) ---

class Figura3D(ABC):
    """Abstract Base Class for 3D Shapes."""
    @abstractmethod
    def calcular_volumen(self):
        pass

    @abstractmethod
    def calcular_area_superficial(self, factor_escala=1.0):
        pass

    @abstractmethod
    def dibujar(self):
        pass

class Cubo(Figura3D):
    def __init__(self, lado):
        self.lado = lado

    def calcular_volumen(self):
        return round(self.lado ** 3, 2)
    
    # Overloading implementation using an optional parameter
    def calcular_area_superficial(self, factor_escala=1.0):
        lado_escalado = self.lado * factor_escala
        return round(6 * (lado_escalado ** 2), 2)

    def dibujar(self):
        return f"Rendering a CUBE with side: {self.lado} units."

class Esfera(Figura3D):
    def __init__(self, radio):
        self.radio = radio

    def calcular_volumen(self):
        return round((4/3) * math.pi * (self.radio ** 3), 2)

    def calcular_area_superficial(self, factor_escala=1.0):
        radio_escalado = self.radio * factor_escala
        return round(4 * math.pi * (radio_escalado ** 2), 2)

    def dibujar(self):
        return f"Rendering a SPHERE with radius: {self.radio} units."

class Cilindro(Figura3D):
    def __init__(self, radio, altura):
        self.radio = radio
        self.altura = altura

    def calcular_volumen(self):
        return round(math.pi * (self.radio ** 2) * self.altura, 2)

    def calcular_area_superficial(self, factor_escala=1.0):
        r_esc = self.radio * factor_escala
        h_esc = self.altura * factor_escala
        return round(2 * math.pi * r_esc * (r_esc + h_esc), 2)

    def dibujar(self):
        return f"Rendering a CYLINDER (R: {self.radio}, H: {self.altura})."

# --- GRAPHICAL USER INTERFACE (TKINTER) ---

class AplicacionFiguras:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("3D Digital Animation System")
        self.ventana.geometry("600x650")
        
        # Mixed list to store different objects (Polymorphism)
        self.lista_mezclada = []
        self.crear_componentes()
        
    def crear_componentes(self):
        # Main Title
        tk.Label(self.ventana, text="Advanced 3D Shapes System", font=("Arial", 16, "bold")).pack(pady=10)

        # Shape Selection
        tk.Label(self.ventana, text="Select a Shape:").pack()
        self.variable_figura = tk.StringVar()
        self.combo_figuras = ttk.Combobox(self.ventana, textvariable=self.variable_figura, state="readonly")
        self.combo_figuras['values'] = ("Cube", "Sphere", "Cylinder")
        self.combo_figuras.pack(pady=5)
        self.combo_figuras.bind("<<ComboboxSelected>>", self.actualizar_entradas)

        # Dynamic Entry Container
        self.contenedor_entradas = tk.Frame(self.ventana)
        self.contenedor_entradas.pack(pady=10)
        self.entradas = {}

        # Scale Factor Slider
        tk.Label(self.ventana, text="Scale Factor (Dynamic Scaling):").pack()
        self.deslizador_escala = tk.Scale(self.ventana, from_=0.1, to=5.0, resolution=0.1, orient="horizontal")
        self.deslizador_escala.set(1.0)
        self.deslizador_escala.pack(pady=5)

        # Action Buttons
        self.boton_agregar = tk.Button(self.ventana, text="Add to Mixed List", command=self.agregar_figura, bg="#4CAF50", fg="white")
        self.boton_agregar.pack(pady=5)

        self.boton_procesar = tk.Button(self.ventana, text="Process All Shapes (Polymorphism)", command=self.procesar_todo, bg="#2e95cc", fg="white")
        self.boton_procesar.pack(pady=5)

        # Output Text Console
        self.texto_salida = tk.Text(self.ventana, height=18, width=70, state="disabled", bg="#f4f4f4")
        self.texto_salida.pack(pady=10)

    def actualizar_entradas(self, evento):
        # Clear previous input fields
        for widget in self.contenedor_entradas.winfo_children():
            widget.destroy()
        self.entradas = {}

        seleccion = self.variable_figura.get()
        
        if seleccion == "Cube":
            self.crear_campo_entrada("Side:")
        elif seleccion == "Sphere":
            self.crear_campo_entrada("Radius:")
        elif seleccion == "Cylinder":
            self.crear_campo_entrada("Radius:")
            self.crear_campo_entrada("Height:")

    def crear_campo_entrada(self, texto_label):
        label = tk.Label(self.contenedor_entradas, text=texto_label)
        label.pack()
        entrada = tk.Entry(self.contenedor_entradas)
        entrada.pack()
        self.entradas[texto_label] = entrada

    def agregar_figura(self):
        try:
            seleccion = self.variable_figura.get()
            if not seleccion:
                messagebox.showwarning("Warning", "Please select a shape first.")
                return

            if seleccion == "Cube":
                self.lista_mezclada.append(Cubo(float(self.entradas["Side:"].get())))
            elif seleccion == "Sphere":
                self.lista_mezclada.append(Esfera(float(self.entradas["Radius:"].get())))
            elif seleccion == "Cylinder":
                r = float(self.entradas["Radius:"].get())
                h = float(self.entradas["Height:"].get())
                self.lista_mezclada.append(Cilindro(r, h))
            
            messagebox.showinfo("Success", f"{seleccion} added to the list.")
            
            # Reset entries
            for ent in self.entradas.values():
                ent.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values.")

    def procesar_todo(self):
        if not self.lista_mezclada:
            messagebox.showwarning("Error", "The list is empty. Please add shapes first.")
            return

        valor_escala = self.deslizador_escala.get()
        self.texto_salida.config(state="normal")
        self.texto_salida.delete(1.0, tk.END)

        # Polymorphism in action
        for i, figura in enumerate(self.lista_mezclada, 1):
            self.texto_salida.insert(tk.END, f"--- Shape Object #{i} ---\n")
            self.texto_salida.insert(tk.END, f"STATUS: {figura.dibujar()}\n")
            self.texto_salida.insert(tk.END, f"VOLUME: {figura.calcular_volumen()} units³\n")
            self.texto_salida.insert(tk.END, f"SURFACE AREA (Scaled x{valor_escala}): {figura.calcular_area_superficial(valor_escala)} units²\n")
            self.texto_salida.insert(tk.END, "-"*50 + "\n")
        
        self.texto_salida.config(state="disabled")

if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacionFiguras(raiz)
    raiz.mainloop()