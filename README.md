# Sistema de Gestión de Tarjetas de Circulación

Este es un sistema cliente-servidor con interfaz gráfica diseñado para gestionar el registro, emisión y control de tarjetas de circulación vehicular, simulando las operaciones de una entidad de tránsito.

## Tecnologías utilizadas
* **Lenguaje:** Python 3
* **Interfaz Gráfica:** Tkinter (Nativo de Python)
* **Base de Datos:** PostgreSQL
* **Librerías principales:** * `psycopg2` (Conector de base de datos)
  * `python-dotenv` (Gestión de variables de entorno y seguridad)

## Instrucciones de instalación
1. Clone este repositorio en su máquina local:
   ```bash
   git clone [https://github.com/TuUsuario/tu-repositorio.git](https://github.com/TuUsuario/tu-repositorio.git)
2. Accceda a la carpeta del proyecto:
   cd tu-repositorio
3. Cree un entorno virtual para aislar las dependencias:
   python -m venv env
4. Active el entorno virtual:
   Windows: env\Scripts\activate
   Mac/Linux: source env/bin/activate
5. Instale las dependencias necesarias:
   pip install psycopg2 python-dotenv
6. Ejecuta los scripts SQL proporcionados en tu gestor de base de datos (pgAdmin o DataGrip) para crear las tablas, relaciones y triggers.

## Cómo ejecutar el proyecto
Una vez instaladas las dependencias y configurada la base de datos, ejecuta el archivo principal de la interfaz desde la terminal:
python interfaz.py

## Credenciales necesarias
Por razones de seguridad, las credenciales de la base de datos no están incluidas en este repositorio. Debes crear un archivo llamado .env en la raíz del proyecto con la siguiente estructura:
DB_HOST=localhost
DB_USER=postgres
DB_PASS="solosielingemepidelacontraseña"
DB_NAME=Proyecto1db

## Puerto Utilizado
PostgreSQL: El sistema se conecta a través del puerto por defecto 5432.

## Nombre de la base de datos:
Proyecto1db


