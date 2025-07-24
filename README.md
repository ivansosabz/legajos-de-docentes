# 📌 Legajos de Docentes

## 📖 Descripción
Este es un sistema de gestión de legajos para docentes, desarrollado con **HTML, CSS, JavaScript, Django y PostgreSQL**. Su objetivo es administrar los documentos de los docentes, controlar su antigüedad y gestionar notificaciones sobre vencimientos de documentos.

## 🛠️ Tecnologías Usadas
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Backend**: Django
- **Base de Datos**: PostgreSQL
- **Control de Versiones**: Git & GitHub

## 📌 Metodología de Trabajo
Utilizaremos el modelo **Git Flow Simplificado**:
1. **Repositorio Principal (`main`)**: Contendrá la versión estable del proyecto.
2. **Forks Personales**: Cada colaborador hará un *fork* del repositorio.
3. **Ramas de Trabajo**: Trabajaremos en ramas separadas basadas en `main`.
   - `feature/nueva-funcionalidad`
   - `fix/correccion-bug`
4. **Pull Requests (PRs)**: Cuando un colaborador termine una tarea, enviará un *Pull Request* para revisión antes de fusionarlo en `main`.

## 🚀 Instrucciones para Ejecutar el Proyecto

```bash
1. Clonar el repositorio

git clone https://github.com/TU-USUARIO/legajos-de-docentes.git
cd legajos-de-docentes

2. Crear entorno virtual

python -m venv env

3. Activar entorno virtual

    En Windows:

env\Scripts\activate

4. Instalar dependencias

pip install -r requirements.txt

5. Crear la base de datos y aplicar migraciones

python manage.py makemigrations
python manage.py migrate

6. Crear superusuario (usuario administrador)

python manage.py createsuperuser

7. Ejecutar el servidor

python manage.py runserver
```
## 🚀 ¿Cómo Trabajar en el Proyecto?
1. **Haz un fork** del repositorio principal.
2. **Clona tu fork** en tu computadora:
   ```bash
   git clone https://github.com/TU-USUARIO/legajos-de-docentes.git
   ```
3. **Crea una nueva rama** para tu tarea:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
4. **Trabaja en tu código** y guárdalo con `commit`:
   ```bash
   git add .
   git commit -m "Descripción del cambio"
   ```
5. **Sube tu rama a GitHub**:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
6. **Crea un Pull Request** desde GitHub para revisión.
7. **Espera la revisión y aprobación** antes de fusionar.

## ✅ Qué Hacer
✔️ Comentar tu código adecuadamente.
✔️ Seguir las convenciones de nombres para ramas y commits.
✔️ Probar tu código antes de enviarlo.
✔️ Solicitar revisión en los Pull Requests.

## ❌ Qué NO Hacer
❌ No hacer cambios directamente en `main`.
❌ No fusionar tu propio Pull Request sin revisión.
❌ No subir código sin documentación básica.

## 📢 Contacto
Para dudas, comunícate por el canal del equipo en **WhatsApp/Discord/Correo**.

¡Bienvenidos al equipo y feliz coding! 🚀
