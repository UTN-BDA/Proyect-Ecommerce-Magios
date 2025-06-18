# 🛒 Proyecto Ecommerce - Magios

Aplicación web de comercio electrónico basada en microservicios. Actualmente permite operar con un único producto, pero está preparada para escalar su complejidad según los requerimientos del proyecto.

---

## 🚀 Tecnologías principales

- **Backend:** Python, Flask
- **Base de datos:** PostgreSQL
- **Cache / Cola de tareas:** Redis
- **Contenedores:** Docker + Docker Compose
- **Orquestación de servicios:** Scripts en PowerShell
- **Control de versiones:** Git + GitHub

---

## ⚠️ Requisitos previos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- PowerShell 

---

## 📁 Estructura del repositorio

```
/docker-postgresql/    --> Configuración y datos persistentes de PostgreSQL
/docker-redis/         --> Configuración de Redis
/docker/               --> Archivos y configuración de los microservicios
setup_ecommerce_noemoji.ps1  --> Script automático para levantar todo
```

---

## 🛠️ Instalación y ejecución

### 🔹 Opción 1: Paso por paso (manual)

1. **Levantar PostgreSQL**

   ```powershell
   cd docker-postgresql
   docker-compose --env-file .env up --build -d
   ```

2. **Levantar Redis**

   ```powershell
   cd ../docker-redis
   docker compose up -d
   ```

3. **Levantar microservicios**

   ```powershell
   cd ../docker
   docker-compose --env-file .env up --build -d
   ```

4. **Verificar contenedores activos**

   ```bash
   docker ps
   ```

---

### 🔹 Opción 2: Automática (recomendada en Windows)

Ejecutar el siguiente script para que todo el entorno se levante automáticamente:

```powershell
.\setup_ecommerce_noemoji.ps1
```

Este script realiza los tres pasos anteriores sin intervención del usuario.

---

## 📌 Notas adicionales

- Asegurate de que el archivo `.env` esté bien configurado antes de ejecutar los servicios.
- Los servicios levantan en segundo plano (`-d`) y reconstruyen imágenes si es necesario (`--build`).
- Puede ser necesario para ejecutar "setup...ps1" en Windows habilitar la ejecucion de scrips para
  eso uar elsiguiente comando:
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
- Tener en ejecucion docker (docker desktop en windows)
---

## 👥 Miembros del equipo

- [Lucas Candia]
- [Fausto Basile]
- [Mauricio Valdés]
