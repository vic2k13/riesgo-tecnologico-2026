# Guía de Creación: Proyecto Auditor de Redes con Django en Linux

## Objetivo y arquitectura inicial

### Tipos de usuario
- **Administrador:** Administra la configuración general con el panel predeterminado de Django.
- **Auditor responsable:** Administra al equipo de auditores JR y supervisa resultados.
- **Auditor JR:** Ejecuta auditorías asignadas y consulta sus métricas.

### Módulos a crear

| Aplicación | Responsabilidad |
| --- | --- |
| `usuarios` | Gestión de cuentas y credenciales. |
| `equipos` | Equipós y asignación de auditores responsables. |
| `activos_red` | Inventario de dispositivos, IPs y segmentos autorizados. |
| `auditorias` | Creación y ejecución de auditorías. |
| `reportes` | Consulta de resultados e informes. |
| `panel` | Interfaz principal y navegación. |

- **Configuración global:** `config`
- **Directorio base:** `auditor_redes`

---


## Crear la carpeta del proyecto

```bash
mkdir -p ~/Proyectos/auditor_redes
cd ~/Proyectos/auditor_redes
pwd
```
Crear el directorio de trabajo y posiciona la terminal en él.

---

## Crear y activar el entorno virtual

```bash
python3 -m venv riesgoT
source riesgoT/bin/activate
python -m pip install --upgrade pip
```
Crear un entorno aislado (`riesgoT`), lo activa y actualiza `pip`.



---

## Instalar Django y registrar dependencias

### Instalar Django
```bash
# Para Python 
python -m pip install Django


```

### Verificar y guardar requerimientos
```bash
python -m django --version
python -m pip freeze > requirements.txt
```
Guardar el estado de dependencias en `requirements.txt`.

---

## Crear el proyecto Django

```bash
django-admin startproject config .
```
Genera los archivos de configuración base (`config`) directamente en el directorio actual.

### Archivos  generados
- `manage.py`: Nuestro main ejecución.
- `config/settings.py`: Ajustes globales del proyecto.
- `config/urls.py`: Manejador de URLs globales.

---

## Crear las Módulos

```bash
python manage.py startapp usuarios
python manage.py startapp equipos
python manage.py startapp activos_red
python manage.py startapp auditorias
python manage.py startapp reportes
python manage.py startapp panel
```
Genera la estructura inicial por módulos.

---

## Registrar las Módulos en la configuración

Editar `config/settings.py` y añadir los módulos a `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # Módulos estándar de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Módulos del proyecto
    'usuarios.apps.UsuariosConfig',
    'equipos.apps.EquiposConfig',
    'activos_red.apps.ActivosRedConfig',
    'auditorias.apps.AuditoriasConfig',
    'reportes.apps.ReportesConfig',
    'panel.apps.PanelConfig',
]
```

---

## Comprobar e inicializar la base de datos

```bash
python manage.py check
python manage.py migrate
```
Validar que no haya errores de configuración y aplica las migraciones iniciales creando `db.sqlite3`.

---

## Crear cuenta administradora

```bash
python manage.py createsuperuser
```
Crea el usuario principal para acceder al panel de administración de Django.

---

## Ejecutar el servidor

```bash
python manage.py runserver
```
Inicia el servidor local :
- **Página principal:** `http://127.0.0.1:8000/`
- **Panel de administración:** `http://127.0.0.1:8000/admin/`

*Detener el servidor con `Ctrl+C`.*

---

## Configurar Git e ignorar archivos sensibles

Crea el archivo `.gitignore` en la raíz del proyecto ó alguna carpeta que lo englobe:

```gitignore
# ==== Entornos virtuales ====
venv/
.venv/
env/
ENV/

# ==== Python ====
__pycache__/
*.py[cod]
*$py.class
*.so

# ==== Django ====
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
#staticfiles/
#media/

# ==== Variables de entorno ====
.env
.env.*
!.env.example

# ==== Testing / cobertura ====
#.coverage
#htmlcov/
#.pytest_cache/

# ==== Editores / IDE ====
.vscode/
.idea/
*.swp

# ==== Sistema operativo ====
.DS_Store
Thumbs.db

# ==== Empaquetado ====
build/
dist/
*.egg-info/

# ==== Archivos temporales ====
*.tmp
*.bak

```



---

## Estructura obtenida

```text
auditor_redes/
├── riesgoT/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── usuarios/
├── equipos/
├── activos_red/
├── auditorias/
├── reportes/
├── panel/
├── .gitignore
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---
# Sesión 3 NOV

---

## 1. Registrar modelo Usuario

En `usuarios/models.py` agregar el siguiente código para generar nuestro tipo de usuario personalizado:

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# Clase usuario personalizada para tener nuestros tipos de usuario admin, auditor responsable y auditor JR
class Usuario(AbstractUser):
    # Clase para fijar las únicas opciones disponibles para el tipo de usuario a guardar en la base de datos
    class Rol(models.TextChoices):
        # var = 'valor_en_db' , 'cadena_a_mostrar_front' 
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
        RESPONSABLE = 'RESPONSABLE', 'Auditor responsable'
        JR = 'JR', 'Auditor Jr'

    # Atributo para indicar el rol del usuario. Se usa el modelo CharField para sólo permitir la selección de una opción
    rol = models.CharField(
        # Máximo tamaño en caracteres para cada opción 
        max_length=20,
        # Cargamos las 3 opciones de tipos de usuarios a la variable de opciones
        choices=Rol.choices,
        # Por default dejamos el privilegio más bajo por cuestiones de seguridad
        default=Rol.JR,
        # Cadena a mostrar en el front para este campo
        verbose_name="Rol en el sistema"
    )

    # Al momento de crear un usuario son obligatorios estos campos
    REQUIRED_FIELDS = ["email", "rol"]

    # Funciones para saber qué tipo de usuario se tiene
    def es_administrador(self):
        return self.rol == self.Rol.ADMINISTRADOR or self.is_superuser

    def es_responsable(self):
        return self.rol == self.Rol.RESPONSABLE

    def es_jr(self):
        return self.rol == self.Rol.JR
     
    # Función para legibilidad en módulo administrador y front
    def __str__(self):
        # Muestra 'Janperez - Auditor responsable'
        return f'{self.username} - {self.get_rol_display()}'

```

---

### Configuración en settings

En `config/settings.py` y debajo de `INSTALLED_APPS` agregar:

```python
# El modelo de autenticación será por medio del modelo Usuario ubicado en el módulo usuarios, ya no se usará el modelo de usuario con el que viene Django por defecto
AUTH_USER_MODEL = "usuarios.Usuario"

```

---

### Generación y aplicación de migraciones

1. **Escaneamos el archivo** `usuarios/models.py` para que Django encuentre nuevas clases o cambios. Este comando genera un archivo de historial dentro de la carpeta `usuarios/migrations` para traducir los cambios a instrucciones de base de datos.
```bash
python manage.py makemigrations usuarios

```


**Resultado:**
```bash
Migrations for 'usuarios':
  usuarios/migrations/0001_initial.py
    + Create model Usuario

```


2. **Aplicamos migraciones.** Se hace una búsqueda de las nuevas migraciones generadas para su traducción y ejecución en el contexto de SQL:
```bash
python manage.py migrate

```


**Resultado (Inconsistencia esperada):**
```text
raise InconsistentMigrationHistory(
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency usuarios.0001_initial on database 'default'.

```


*Nota: Ya teníamos una migración aplicada para la autenticación trabajando con el usuario por defecto de Django.*
3. Podemos revisar el estado actual de las migraciones (las que tienen `[X]` ya fueron aplicadas):
```bash
python manage.py showmigrations

```


4. **Borrar la base de datos:** Es necesario borrar el archivo `db.sqlite3` para generar la nueva base de datos limpia con el nuevo modelo de usuario.
5. Ejecutamos nuevamente las migraciones:
```bash
python manage.py migrate

```


6. Verificamos el estado final de las migraciones:
```bash
python manage.py showmigrations

```



---

### Crear usuario administrador

Ahora podemos crear usuarios administradores usando el siguiente comando:

```bash
python manage.py createsuperuser

```

```text
Username: vf2k13
Email address: vf2k13@gmail.com
Rol en el sistema: ADMINISTRADOR
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.

```

---

## 2. Registrar modelo Equipo

Dentro de `equipos/models.py` pegar lo siguiente:

```python
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# Clase que modela un Equipo y que extiende a Model
class Equipo(models.Model):
    nombre = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name='Nombre del equipo'
    )
    
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    
    # Relación uno a uno (un equipo sólo tiene un único responsable y viceversa)
    responsable = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        limit_choices_to={'rol': 'RESPONSABLE'},
        related_name='equipo_liderado',
        verbose_name='Auditor Responsable'
    )

    activo = models.BooleanField(
        default=True,
        verbose_name='Equipo activo'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.responsable_id:
            if self.responsable.rol != 'RESPONSABLE':
                raise ValidationError({
                    'responsable': 'El usuario seleccionado no es auditor responsable.'
                })

    def __str__(self):
        return f'{self.nombre} (Líder: {self.responsable.username})'
     
    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['nombre']


class IntegranteEquipo(models.Model):
    # Llave foránea, un equipo puede tener muchos integrantes JR
    equipo = models.ForeignKey(
        Equipo, 
        on_delete=models.PROTECT,
        related_name='integrantes_jr'
    )
    
    # Relación uno a uno, un auditor JR sólo puede pertenecer a un único equipo
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'JR'},
        related_name='integrante_equipo',
        verbose_name='Auditor Jr'
    )

    fecha_ingreso = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de ingreso'
    )

    def clean(self):
        super().clean()
        if self.usuario_id:
            if self.usuario.rol != 'JR':
                raise ValidationError({
                    'usuario': 'Solamente se pueden agregar auditores JR.'
                })

    def __str__(self):
        return f'{self.usuario.username} -> {self.equipo.nombre}'
     
    class Meta:
        verbose_name = 'Integrante del equipo'
        verbose_name_plural = 'Integrantes del equipo'
        ordering = ['equipo__nombre', 'usuario__username']

```

Generamos y aplicamos migraciones para la app de equipos:

```bash
python manage.py makemigrations equipos
python manage.py migrate

```

---

## 3. Creación y edición de usuarios y equipos desde el panel de administración

### Formularios personalizados (`usuarios/forms.py`)

Debemos crear el archivo `usuarios/forms.py` para definir formularios basados en nuestros modelos predefinidos:

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

# Formulario para crear nuevos usuarios
class UsuarioCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Correo electrónico"
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "rol",
        )


# Formulario para modificar usuarios existentes
class UsuarioChangeForm(UserChangeForm):
    email = forms.EmailField(
        required=True,
        label="Correo electrónico"
    )

    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = "__all__"

```

---

### Configuración del Admin (`usuarios/admin.py`)

Modificamos `usuarios/admin.py` para integrar los formularios anteriores en el panel de administración:

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "rol",
        "is_active",
    )

    list_filter = (
        "rol",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("username",)

    fieldsets = UserAdmin.fieldsets + (
        ("Información del sistema", {
            "fields": ("rol",)
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "first_name",
                "last_name",
                "rol",
                "password1",
                "password2",
            ),
        }),
    )

```

---

### Configuración del Admin para Equipos (`equipos/admin.py`)

Para gestionar los equipos y sus integrantes de forma eficiente, modificamos `equipos/admin.py`:

```python
from django.contrib import admin
from .models import Equipo, IntegranteEquipo


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'responsable',
        'activo',
        'fecha_creacion',
    )

    search_fields = (
        'nombre',
        'responsable__username',
    )

    list_filter = (
        'activo',
    )


@admin.register(IntegranteEquipo)
class IntegranteEquipoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'equipo',
        'fecha_ingreso',
    )

    search_fields = (
        'usuario__username',
        'equipo__nombre',
    )

    list_filter = (
        'equipo',
    )

    list_select_related = (
        'usuario',
        'equipo',
    )

```


