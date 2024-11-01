import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
from modelo.mundo import Biblioteca, BibliotecaGestion, Libro, Usuario, UsuarioNoAutenticado, LibroNoDisponible, LibroNoEncontrado

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.biblioteca = Biblioteca()
        self.biblioteca_gestion = BibliotecaGestion()
        
        # Widgets para la autenticación
        self.crear_widgets_autenticacion()
        
        # Variable de usuario autenticado
        self.usuario_actual = None

    def crear_widgets_autenticacion(self):
        """Widgets para autenticar o crear usuario."""
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        # Crear usuario
        tk.Label(frame, text="Nombre de Usuario:").grid(row=0, column=0)
        self.nombre_usuario = tk.Entry(frame)
        self.nombre_usuario.grid(row=0, column=1)

        tk.Label(frame, text="Contraseña:").grid(row=1, column=0)
        self.contrasena = tk.Entry(frame, show="*")
        self.contrasena.grid(row=1, column=1)

        tk.Button(frame, text="Crear Usuario", command=self.crear_usuario).grid(row=2, column=0, pady=5)
        tk.Button(frame, text="Iniciar Sesión", command=self.iniciar_sesion).grid(row=2, column=1, pady=5)

    def crear_usuario(self):
        nombre = self.nombre_usuario.get()
        contrasena = self.contrasena.get()
        try:
            self.biblioteca.crear_perfil_usuario(nombre, contrasena)
            messagebox.showinfo("Éxito", f"Usuario '{nombre}' creado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def iniciar_sesion(self):
        nombre = self.nombre_usuario.get()
        contrasena = self.contrasena.get()
        try:
            self.usuario_actual = self.biblioteca.autenticar_usuario(nombre, contrasena)
            messagebox.showinfo("Éxito", f"Bienvenido, {nombre}")
            self.crear_widgets_biblioteca()
        except UsuarioNoAutenticado as e:
            messagebox.showerror("Error", str(e))

    def crear_widgets_biblioteca(self):
        """Crea widgets para administrar libros y préstamos."""
        for widget in self.root.winfo_children():
            widget.destroy()  # Limpiar pantalla

        # Widgets para libros
        tk.Label(self.root, text="Gestión de Biblioteca", font=("Arial", 14)).pack(pady=10)
        
        # Añadir libro
        frame_libro = tk.Frame(self.root)
        frame_libro.pack(pady=10)
        
        tk.Label(frame_libro, text="Título:").grid(row=0, column=0)
        self.titulo_libro = tk.Entry(frame_libro)
        self.titulo_libro.grid(row=0, column=1)
        
        tk.Label(frame_libro, text="Autor:").grid(row=1, column=0)
        self.autor_libro = tk.Entry(frame_libro)
        self.autor_libro.grid(row=1, column=1)
        
        tk.Label(frame_libro, text="Género:").grid(row=2, column=0)
        self.genero_libro = tk.Entry(frame_libro)
        self.genero_libro.grid(row=2, column=1)
        
        tk.Label(frame_libro, text="ISBN:").grid(row=3, column=0)
        self.isbn_libro = tk.Entry(frame_libro)
        self.isbn_libro.grid(row=3, column=1)

        tk.Button(frame_libro, text="Añadir Libro", command=self.anadir_libro).grid(row=4, columnspan=2, pady=5)
        tk.Button(frame_libro, text="Visualizar Libros", command=self.visualizar_libros).grid(row=5, columnspan=2, pady=5)

        # Widgets para préstamos
        frame_prestamo = tk.Frame(self.root)
        frame_prestamo.pack(pady=10)
        
        tk.Label(frame_prestamo, text="ISBN del Libro a Prestar:").grid(row=0, column=0)
        self.isbn_prestamo = tk.Entry(frame_prestamo)
        self.isbn_prestamo.grid(row=0, column=1)
        
        tk.Label(frame_prestamo, text="Días de Préstamo:").grid(row=1, column=0)
        self.dias_prestamo = tk.Entry(frame_prestamo)
        self.dias_prestamo.grid(row=1, column=1)

        tk.Button(frame_prestamo, text="Registrar Préstamo", command=self.registrar_prestamo).grid(row=2, columnspan=2, pady=5)
        tk.Button(frame_prestamo, text="Devolver Libro", command=self.devolver_libro).grid(row=3, columnspan=2, pady=5)
        tk.Button(frame_prestamo, text="Generar Reporte de Préstamos", command=self.generar_reporte_prestamos).grid(row=4, columnspan=2, pady=5)

    def anadir_libro(self):
        titulo = self.titulo_libro.get()
        autor = self.autor_libro.get()
        genero = self.genero_libro.get()
        try:
            isbn = int(self.isbn_libro.get())
            self.biblioteca_gestion.catalogo.anadir_libro(titulo, autor, genero, isbn)
            messagebox.showinfo("Éxito", f"Libro '{titulo}' añadido al catálogo.")
        except ValueError:
            messagebox.showerror("Error", "El ISBN debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualizar_libros(self):
        try:
            libros = self.biblioteca_gestion.catalogo.visualizar_libros()
            messagebox.showinfo("Libros en el Catálogo", libros)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def registrar_prestamo(self):
        try:
            isbn = int(self.isbn_prestamo.get())
            dias = int(self.dias_prestamo.get())
            libro = self.obtener_libro_por_isbn(isbn)
            if libro:
                self.biblioteca_gestion.registrar_prestamo(libro, self.usuario_actual, dias)
                messagebox.showinfo("Éxito", f"Préstamo registrado para '{libro.titulo}'.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ISBN y días válidos.")
        except (LibroNoDisponible, LibroNoEncontrado) as e:
            messagebox.showerror("Error", str(e))

    def devolver_libro(self):
        try:
            isbn = int(self.isbn_prestamo.get())
            libro = self.obtener_libro_por_isbn(isbn)
            if libro:
                self.biblioteca_gestion.devolver_libro(libro)
                messagebox.showinfo("Éxito", f"Libro '{libro.titulo}' devuelto.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ISBN válido.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generar_reporte_prestamos(self):
        try:
            self.biblioteca_gestion.generar_reporte()
            messagebox.showinfo("Éxito", "Reporte generado en 'reporte_prestamos.pdf'.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def obtener_libro_por_isbn(self, isbn):
        """Devuelve el libro del catálogo por ISBN si existe, de lo contrario lanza una excepción."""
        for libro in self.biblioteca_gestion.catalogo.libros:
            if libro.ISBN == isbn:
                return libro
        raise LibroNoEncontrado("El libro con el ISBN proporcionado no fue encontrado.")

# Inicializar la interfaz gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()
