<h1 align="center">Pruebas de Endpoints en Producción - Azure Container Apps</h1>

<div align="center">
  <img src="https://img.shields.io/badge/Environment-Production-brightgreen?style=for-the-badge&logo=azure" alt="Production Environment"/>
  <img src="https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi" alt="FastAPI Badge"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status Badge"/>
</div>

<p align="center">
  <i>Documentación de pruebas funcionales ejecutadas directamente contra el entorno de producción en Microsoft Azure Container Apps.</i>
</p>

---

## Información del Entorno

* **URL Base de Producción:**  
  `https://app-cicdfundev.nicebush-06dcb993.brazilsouth.azurecontainerapps.io`
* **Swagger / OpenAPI Documentation:**  
  `https://app-cicdfundev.nicebush-06dcb993.brazilsouth.azurecontainerapps.io/docs`

---

## Resumen de Endpoints Disponibles

| Método | Endpoint | Descripción | Estado Esperado |
| :---: | :--- | :--- | :---: |
| `GET` | `/health` | Verificación de estado del servicio | `200 OK` |
| `POST` | `/credit-applications` | Crear una nueva solicitud de crédito | `201 Created` |
| `GET` | `/credit-applications` | Listar todas las solicitudes registradas | `200 OK` |
| `GET` | `/credit-applications/{id}` | Consultar detalle de una solicitud por ID | `200 OK` / `404 Not Found` |
| `PUT` | `/credit-applications/{id}/status` | Actualizar estado (`APPROVED`, `REJECTED`, etc.) | `200 OK` / `422 Unprocessable` |

---

## Comandos cURL de Prueba & Respuestas de Producción

A continuación se presentan los comandos cURL listos para ejecutar y la evidencia de las respuestas retornadas por la API en vivo.

### 1. Verification Health Check (`GET /health`)

**Comando cURL:**
```bash
curl -X GET "https://app-cicdfundev.nicebush-06dcb993.brazilsouth.azurecontainerapps.io/health" \
  -H "accept: application/json"
```

**Respuesta Obtenida:**
```json
{
  "status": "ok"
}
```

---

### 2. Crear Solicitud de Crédito (`POST /credit-applications`)

**Comando cURL:**
```bash
curl -X POST "https://app-cicdfundev.nicebush-06dcb993.brazilsouth.azurecontainerapps.io/credit-applications" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Ana Torres",
    "document_number": "1020304050",
    "requested_amount": 15000000
  }'
```

**Respuesta Obtenida (`201 Created`):**
```json
{
	"customer_name": "Ana Torres",
	"document_number": "1020304050",
	"requested_amount": 15000000.0,
	"application_id": "1f20936e-0287-421f-8d32-9b3583c1c908",
	"status": "PENDING"
}
```

---

### 3. Listar Solicitudes de Crédito (`GET /credit-applications`)

**Comando cURL:**
```bash
curl -X GET "https://app-cicdfundev.nicebush-06dcb993.brazilsouth.azurecontainerapps.io/credit-applications" \
  -H "accept: application/json"
```

**Respuesta Obtenida (`200 OK`):**
```json
[
	{
		"customer_name": "Ana Torres",
		"document_number": "1020304050",
		"requested_amount": 15000000.0,
		"application_id": "1f20936e-0287-421f-8d32-9b3583c1c908",
		"status": "PENDING"
	}
]
```

---

### 4. Consultar Solicitud por ID (`GET /credit-applications/{application_id}`)

**Comando cURL:**
```bash
curl -X GET "https://app-cicdfundev.nicebush-06dcb993.brazilsouth.azurecontainerapps.io/credit-applications/:id" \
  -H "accept: application/json"
```

**Respuesta Obtenida (`200 OK`):**
```json
{
	"customer_name": "Ana Torres",
	"document_number": "1020304050",
	"requested_amount": 15000000.0,
	"application_id": "1f20936e-0287-421f-8d32-9b3583c1c908",
	"status": "PENDING"
}
```

---

### 5. Actualizar Estado de Solicitud (`PUT /credit-applications/{application_id}/status`)

**Comando cURL:**
```bash
curl -X PUT "https://app-cicdfundev.nicebush-06dcb993.brazilsouth.azurecontainerapps.io/credit-applications/REEMPLAZAR_CON_APPLICATION_ID/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "APPROVED"
  }'
```

**Respuesta Obtenida (`200 OK`):**
```json
{
	"customer_name": "Ana Torres",
	"document_number": "1020304050",
	"requested_amount": 15000000.0,
	"application_id": "1f20936e-0287-421f-8d32-9b3583c1c908",
	"status": "APPROVED"
}
```

---

