# Turtlector 


##  Descripción

Una versión tortuga del sobrero seleccionador para saber a que facultad y a que carrera eres mas posible de pertenecer.

##  Arquitectura del Proyecto

### Backend
- **Framework**: FastAPI (Python)
- **IA**: Google Gemini para análisis de imágenes
- **Audio**: Whisper para procesamiento de audio
- **Estructura**: API REST modular

### Frontend
- **Framework**: React + TypeScript
- **3D Engine**: React Three Fiber
- **Utilidades 3D**: Drei
- **Build Tool**: Vite
- **Styling**: CSS/Styled Components

##  Estructura del Proyecto

```
Turtlector/
├── backend/
│   ├── app/
│   │   ├── config/     # Configuraciones
│   │   ├── models/     # Modelos de datos
│   │   ├── routers/    # Endpoints de API
│   │   ├── services/   # Lógica de negocio
│   │   └── main.py     # Punto de entrada
│   ├── uploads/        # Archivos subidos
│   └── .env.example    # Variables de entorno
├── frontend/
│   ├── src/            # Código fuente React
│   ├── public/         # Archivos estáticos
│   └── package.json    # Dependencias Node.js
└── docker-compose.yml  # Orquestación de contenedores
```

##  Instalación y Ejecución

### Prerrequisitos
- Docker y Docker Compose
- Node.js 18+ (para desarrollo local)
- Python 3.11+ (para desarrollo local)

### Ejecución con Docker (Recomendado)

1. Clona el repositorio:
```bash
git clone <repository-url>
cd Turtlector
```

2. Configura las variables de entorno:
```bash
cp backend/.env.example backend/.env
# Edita backend/.env con tus claves de API
```

3. Ejecuta con Docker Compose:
```bash
docker-compose up --build
```

4. Accede a la aplicación:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentación API: http://localhost:8000/docs

### Desarrollo Local

#### Backend
```bash
cd backend
python -m venv env

uv venv env #en caso de tener Ultraviolet

source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

uv pip install -r requirements.txt #en caso de tener Ultraviolet

uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

##  Configuración

### Variables de Entorno (Backend)

Copia `.env.example` a `.env` y configura:

```env
GEMINI_API_KEY=tu_clave_de_gemini
WHISPER_MODEL=base
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
```

##  Documentación de APIs y Tecnologías

### Tecnologías Principales
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno para Python
- **[React Three Fiber](https://docs.pmnd.rs/react-three-fiber/getting-started/introduction)** - React renderer para Three.js
- **[Drei](https://github.com/pmndrs/drei)** - Utilidades para React Three Fiber
- **[Google Gemini](https://ai.google.dev/docs)** - API de IA de Google
- **[OpenAI Whisper](https://openai.com/research/whisper)** - Modelo de reconocimiento de voz

### APIs de Desarrollo
- **[Vite](https://vitejs.dev/)** - Build tool para frontend
- **[Three.js](https://threejs.org/docs/)** - Biblioteca 3D para JavaScript
- **[TypeScript](https://www.typescriptlang.org/docs/)** - Superset tipado de JavaScript

## Docker

### Contenedores Incluidos

- **Backend**: FastAPI + Python 3.11
- **Frontend**: Node.js + Nginx para producción
- **Volúmenes**: Persistencia de uploads y configuraciones

### Comandos Docker Útiles

```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Limpiar volúmenes
docker-compose down -v
```



## Licencia

Me imagino que para TAWS. Ver el archivo `LICENSE` sabra dios donde esta.

## 👥 Autores

- No olvidar poner los nombres


