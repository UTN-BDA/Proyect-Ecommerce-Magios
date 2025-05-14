# Proyect-Ecommerce-Magios
Por el momento hemos decidido hacer un proyecto de comercio electrónico y en principi de un solo producto
Dejamos la posibilidad de que el proyecto se tranforme de a cuerdo a la complejidad que requiera

Write-Host "PASO 1: Entrando a docker-postgresql"
Set-Location "./docker-postgresql"

Write-Host "PASO 2: Levantando PostgreSQL"
docker-compose --env-file .env up --build -d

Write-Host "PASO 3: Volviendo al directorio base y entrando a docker-redis"
Set-Location "../docker-redis"

Write-Host "PASO 4: Levantando Redis"
docker compose up -d

Write-Host "PASO 5: Entrando a la carpeta docker (microservicios)"
Set-Location "../docker"

Write-Host "PASO 6: Levantando microservicios"
docker-compose --env-file .env up --build -d

Write-Host "Todos los servicios están levantados correctamente."