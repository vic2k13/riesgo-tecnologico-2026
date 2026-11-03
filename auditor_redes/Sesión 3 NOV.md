Aquí tienes tu documento formateado limpiamente en **Markdown**, ideal para notas, documentación o control de versiones:

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