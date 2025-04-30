# Sistema de Biblioteca BCF

Una aplicación web Django para la gestión de biblioteca, diseñada específicamente para bibliotecarios con un enfoque en la usabilidad móvil.

## Características

- 🔍 **Búsqueda eficiente de libros** por título, autor, ISBN o código Dewey
- 📚 **Gestión completa de inventario** de libros
- 🏷️ **Administración de códigos Dewey** para clasificación de libros
- 📱 **Diseño responsive** optimizado para dispositivos móviles

## Requisitos

- Python 3.8+
- Django 5.2+

## Instalación

1. Clonar el repositorio:
```
git clone https://github.com/su-usuario/biblioteca-bcf.git
cd biblioteca-bcf
```

2. Crear y activar un entorno virtual (opcional pero recomendado):
```
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

3. Instalar dependencias:
```
pip install -r requirements.txt
```

4. Realizar migraciones de la base de datos:
```
python manage.py makemigrations
python manage.py migrate
```

5. Crear un superusuario:
```
python manage.py createsuperuser
```

6. Iniciar el servidor:
```
python manage.py runserver
```

7. Acceder a la aplicación en: http://127.0.0.1:8000/

## Uso

- **Página principal**: Acceso rápido a las principales funciones
- **Libros**: Lista, búsqueda, creación y edición de libros
- **Códigos Dewey**: Gestión de los códigos de clasificación

## Contribuir

Las contribuciones son bienvenidas. Por favor, siéntase libre de enviar un Pull Request o abrir un Issue para discutir cambios propuestos.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo LICENSE para más detalles. 