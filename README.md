# Odoo 19 Docker
Entorno de desarrollo para Odoo 19 usando Docker y Docker Compose.

## Requisitos Previos
- Docker
- Docker Compose
- Make (opcional, para usar los comandos del Makefile)

## Arquitectura
Este proyecto incluye dos servicios principales:
- **PostgreSQL 16**: Base de datos para Odoo
- **Odoo 19**: Aplicación construida desde un Dockerfile personalizado basado en Ubuntu Noble

## Inicio Rápido
### 1. Clonar y Configurar

```bash
git clone <tu-repositorio>
cd odoo19_docker
```

El archivo `.env` ya está configurado con los valores predeterminados. Puedes modificarlo según tus necesidades.

### 2. Construir y Levantar los Servicios
**Usando Make:**
```bash
make build
make up
```

**Usando Docker Compose directamente:**
```bash
docker compose build
docker compose up -d
```

### 3. Acceder a Odoo
Una vez que los servicios estén en ejecución, accede a Odoo en:
- **URL Principal**: http://localhost:8099
- **Bus Port**: http://localhost:8091
- **Longpolling Port**: http://localhost:8092

## Configuración
### Variables de Entorno (.env)

```env
# PostgreSQL
POSTGRES_DB=postgres
POSTGRES_USER=odoo
POSTGRES_PASSWORD=odoo
POSTGRES_PORT=5432

# Odoo
ODOO_HOST=db
ODOO_PORT=8069
ODOO_PORT_MAP=8099:8069
ODOO_BUS_PORT_MAP=8091:8071
ODOO_LONGPOLLING_PORT_MAP=8092:8072
```

### Estructura de Directorios

```
.
├── docker-compose.yml    # Configuración de servicios Docker
├── Dockerfile           # Imagen personalizada de Odoo 19
├── .env                 # Variables de entorno
├── makefile             # Comandos útiles
├── entrypoint.sh        # Script de entrada del contenedor
├── wait-for-psql.py     # Script de espera para PostgreSQL
├── addons/              # Módulos adicionales de Odoo
└── config/              # Configuración de Odoo
    └── odoo.conf
```

## Comandos Disponibles (Makefile)

| Comando | Descripción |
|---------|-------------|
| `make build` | Construye la imagen de Odoo |
| `make up` | Levanta todos los servicios en segundo plano |
| `make down` | Detiene todos los servicios |
| `make rebuild` | Reconstruye la imagen desde cero y levanta los servicios |
| `make logs` | Muestra los logs de Odoo en tiempo real |
| `make shell-odoo` | Abre una shell bash dentro del contenedor de Odoo |
| `make shell-db` | Abre una shell bash dentro del contenedor de PostgreSQL |
| `make restart-odoo` | Reinicia solo el servicio de Odoo |
| `make clean` | Detiene y elimina contenedores y volúmenes |
| `make reset` | Reinicio completo (elimina todo y reconstruye) |

## Volúmenes

El proyecto utiliza los siguientes volúmenes Docker:

- **odoo19-db-data**: Datos persistentes de PostgreSQL
- **odoo19-filestore**: Archivos y attachments de Odoo
- **./addons**: Módulos personalizados (montado desde el host)
- **./config**: Configuración de Odoo (montado desde el host)

## Desarrollo
### Agregar Módulos Personalizados
Coloca tus módulos personalizados en el directorio `addons/`. Estos estarán disponibles automáticamente en Odoo.

```bash
addons/
├── mi_modulo_custom/
│   ├── __init__.py
│   ├── __manifest__.py
│   └── ...
```

Luego reinicia Odoo y actualiza la lista de aplicaciones desde la interfaz web.

### Modificar Configuración de Odoo

Edita el archivo `config/odoo.conf` para ajustar la configuración de Odoo según tus necesidades.

Después de modificarlo, reinicia el servicio:

```bash
make restart-odoo
```

### Ver Logs

Para monitorear los logs de Odoo en tiempo real:

```bash
make logs
```

O con Docker Compose:

```bash
docker compose logs -f odoo
```

### Acceder al Contenedor

Para ejecutar comandos dentro del contenedor de Odoo:

```bash
make shell-odoo
```

Desde ahí puedes ejecutar comandos de Odoo, por ejemplo:

```bash
odoo --help
```

## 🗃️ Base de Datos

### Credenciales de PostgreSQL

- **Host**: db (interno) o localhost:5432 (desde el host)
- **Base de datos**: postgres
- **Usuario**: odoo
- **Contraseña**: odoo

## 🔄 Actualización y Mantenimiento

### Reconstruir la Imagen

Si modificas el `Dockerfile`:

```bash
make rebuild
```

### Limpiar Recursos

Para eliminar contenedores, volúmenes y empezar de cero:

```bash
make clean
```

Para un reset completo (reconstruye todo):

```bash
make reset
```
