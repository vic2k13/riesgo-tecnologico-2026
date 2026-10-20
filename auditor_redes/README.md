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



