import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Excepciones personalizadas
class UsuarioNoAutenticado(Exception):
    def __init__(self, mensaje="Nombre de usuario o contraseña incorrectos."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class LibroNoDisponible(Exception):
    def __init__(self, mensaje="El libro no está disponible para préstamo."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class LibroNoEncontrado(Exception):
    def __init__(self, mensaje="No se encontraron libros con los criterios especificados."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class Usuario:
    def __init__(self, nombre_usuario: str, contrasena: str):
        self.nombre_usuario = nombre_usuario
        self.__contrasena = contrasena

    def verificar_credenciales(self, nombre_usuario, contrasena):
        return self.nombre_usuario == nombre_usuario and self.__contrasena == contrasena

class Biblioteca:
    def __init__(self):
        self.usuarios = []
    
    def crear_perfil_usuario(self, nombre_usuario: str, contrasena: str):
        for usuario in self.usuarios:
            if usuario.nombre_usuario == nombre_usuario:
                print(f"El usuario {nombre_usuario} ya existe.")
                return
        nuevo_usuario = Usuario(nombre_usuario, contrasena)
        self.usuarios.append(nuevo_usuario)
        print(f"Usuario {nombre_usuario} creado con éxito.")
    
    def autenticar_usuario(self, nombre_usuario, contrasena):
        for usuario in self.usuarios:
            if usuario.verificar_credenciales(nombre_usuario, contrasena):
                print(f"Bienvenido {nombre_usuario}")
                return usuario
        raise UsuarioNoAutenticado()  # Lanzar excepción si no hay coincidencia

class Libro:
    def __init__(self, titulo: str, autor: str, genero: str, ISBN: int):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.ISBN = ISBN
        self.disponible = True

class Catalogo:
    def __init__(self):
        self.libros = []
    
    def anadir_libro(self, titulo: str, autor: str, genero: str, ISBN: int):
        nuevo_libro = Libro(titulo, autor, genero, ISBN)
        self.libros.append(nuevo_libro)
        print(f"Libro '{titulo}' añadido al catálogo con éxito.")
    
    def visualizar_libros(self):
        if not self.libros:
            print("No hay libros en el catálogo.")
        else:
            for libro in self.libros:
                disponibilidad = "Disponible" if libro.disponible else "Prestado"
                print(f"Título: {libro.titulo}, Autor: {libro.autor}, Género: {libro.genero}, ISBN: {libro.ISBN}, Disponibilidad: {disponibilidad}")
    
    def buscar_libros(self, filtro: str, valor: str):
        resultados = [libro for libro in self.libros if getattr(libro, filtro, "").lower() == valor.lower()]
        if resultados:
            for libro in resultados:
                disponibilidad = "Disponible" if libro.disponible else "Prestado"
                print(f"Título: {libro.titulo}, Autor: {libro.autor}, Género: {libro.genero}, ISBN: {libro.ISBN}, Disponibilidad: {disponibilidad}")
        else:
            raise LibroNoEncontrado()  # Lanzar excepción si no se encuentran libros

class Prestamo:
    def __init__(self, fecha_prestamo: datetime.date, fecha_devolucion: datetime.date, libro: Libro, usuario: Usuario):
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.libro:Libro = libro
        self.usuario = usuario
    
    def registrar_devolucion(self):
        if not self.libro.disponible:
            self.libro.disponible = True
            print(f"El libro '{self.libro.titulo}' ha sido devuelto por {self.usuario.nombre_usuario}.")
        else:
            print(f"El libro '{self.libro.titulo}' ya estaba disponible.")

    def generar_reporte_prestamos(self, prestamos, nombre_archivo="reporte_prestamos.pdf"):
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        c.setTitle("Reporte de Préstamos")
        width, height = letter

        c.drawString(100, height - 50, "Reporte de Préstamos Actuales")
        c.drawString(100, height - 80, f"Fecha de generación: {datetime.date.today()}")

        y = height - 120
        c.drawString(50, y, "Título del Libro")
        c.drawString(200, y, "Usuario")
        c.drawString(350, y, "Fecha de Préstamo")
        c.drawString(450, y, "Fecha de Devolución")
        y -= 20

        for prestamo in prestamos:
            c.drawString(50, y, prestamo.libro.titulo)
            c.drawString(200, y, prestamo.usuario.nombre_usuario)
            c.drawString(350, y, str(prestamo.fecha_prestamo))
            c.drawString(450, y, str(prestamo.fecha_devolucion))
            y -= 20
            if y < 50:  
                c.showPage()
                y = height - 50

        c.save()
        print(f"Reporte generado: {nombre_archivo}")

class BibliotecaGestion:
    def __init__(self):
        self.catalogo = Catalogo()
        self.prestamos: list[Prestamo] = []
    
    def registrar_prestamo(self, libro: Libro, usuario: Usuario, dias_prestamo: int):
        if libro.disponible:
            fecha_prestamo = datetime.date.today()
            fecha_devolucion = fecha_prestamo + datetime.timedelta(days=dias_prestamo)
            prestamo = Prestamo(fecha_prestamo, fecha_devolucion, libro, usuario)
            libro.disponible = False
            self.prestamos.append(prestamo)
            print(f"Préstamo registrado: '{libro.titulo}' prestado a {usuario.nombre_usuario} hasta {fecha_devolucion}.")
        else:
            raise LibroNoDisponible()  # Lanzar excepción si el libro no está disponible
    
    def devolver_libro(self, libro: Libro):
        for prestamo in self.prestamos:
            if prestamo.libro == libro:
                prestamo.registrar_devolucion()
                self.prestamos.remove(prestamo)
                return
        print(f"El libro '{libro.titulo}' no estaba en préstamo.")
    
    def generar_reporte(self):
        if self.prestamos:
            prestamo = Prestamo(None, None, None, None)
            prestamo.generar_reporte_prestamos(self.prestamos)
        else:
            print("No hay préstamos registrados para generar un reporte.")
