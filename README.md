# Finance Tracker 💰

Aplicación web de gestión de gastos personales construida con **Streamlit** y **Python**. Permite registrar, consultar, modificar, filtrar y exportar gastos de forma persistente, con almacenamiento en **AWS S3**.

Está pensada para quienes quieren un control simple y visual de sus finanzas personales desde el navegador, sin necesidad de base de datos ni infraestructura compleja.

---

## Características principales

- **Agregar gastos** — Registra un gasto con categoría, monto y fecha/hora automática.
- **Ver historial completo** — Tabla interactiva con selección de filas para editar o eliminar.
- **Resumen por categoría** — Total acumulado agrupado por categoría con visualización en tabla.
- **Porcentaje por categoría** — Gráfico de barras con el peso relativo de cada categoría sobre el total.
- **Gastos de la última semana** — Gráfico de barras con los gastos de los últimos 7 días.
- **Día récord** — Métrica destacada con el día de mayor desembolso acumulado del historial.
- **Filtrar por categoría** — Selector interactivo para ver todos los gastos de una categoría.
- **Modificar un gasto** — Formulario inline para cambiar categoría y/o monto de un gasto existente.
- **Eliminar un gasto** — Borrado directo desde la tabla con confirmación visual.
- **Exportar resumen general a TXT** — Descarga `Historial_general.txt` con el total por categoría y gran total.
- **Exportar historial detallado a TXT** — Descarga `Historial_detallado.txt` con fecha, categoría y monto de cada gasto.

---

## Arquitectura del proyecto

```
finance_tracker/
├── main.py                  # Punto de entrada Streamlit. Routing de vistas.
├── requirements.txt         # Dependencias del proyecto.
├── .env                     # Variables de entorno (credenciales AWS, no commitear).
├── src/
│   ├── __init__.py
│   ├── analytics.py         # Capa de negocio: cálculos y análisis puros.
│   ├── config.py            # Configuración centralizada via pydantic-settings.
│   ├── crud.py              # Capa de persistencia: lectura/escritura en S3.
│   ├── exports.py           # Capa de exportación: generación de reportes TXT.
│   ├── filters.py           # Helpers de filtrado stateless.
│   ├── validator.py         # Validación y normalización de inputs.
│   ├── vistas.py            # Capa de presentación: componentes Streamlit.
│   └── storage/
│       ├── __init__.py
│       └── s3_storage.py    # Wrapper de AWS S3 (boto3).
└── tests/
    ├── test_analytics.py
    ├── test_crud.py
    ├── test_exports.py
    ├── test_filters.py
    ├── test_validator.py
    └── test_vistas.py
```

### Patrón de capas

El proyecto aplica **responsabilidad única por módulo**: cada capa tiene una sola razón para cambiar y no cruza sus fronteras.

| Módulo | Responsabilidad |
|---|---|
| `main.py` | Punto de entrada. Lee el historial al iniciar, muestra el sidebar de navegación y delega cada vista a `vistas.py`. No contiene lógica de negocio. |
| `vistas.py` | Capa de presentación. Renderiza todos los componentes Streamlit (tablas, gráficos, formularios). Delega persistencia a `crud.py` y cálculos a `analytics.py`. |
| `crud.py` | Única capa que accede al storage. Expone funciones para leer, agregar, modificar y eliminar gastos. Usa lazy initialization para el cliente S3. |
| `analytics.py` | Funciones puras de análisis: porcentajes, resúmenes, filtros temporales y día récord. No accede a archivos ni modifica estado global. |
| `filters.py` | Helpers stateless para obtener categorías únicas y filtrar listas por categoría. |
| `exports.py` | Genera strings de texto formateados para descargar como TXT. Delega cálculos a `analytics.py`. |
| `validator.py` | Valida y normaliza los inputs del usuario (categoría y monto) antes de que lleguen a la capa de persistencia. |
| `storage/s3_storage.py` | Wrapper de boto3. Encapsula todas las llamadas a la API de AWS S3 con manejo granular de errores. |
| `config.py` | Carga y valida las variables de entorno usando `pydantic-settings`. Falla rápido si falta una variable crítica. |

---

## Modelo de datos

Los gastos se persisten en `historial.json` dentro del bucket S3 configurado, como un array de objetos JSON:

```json
[
  {
    "id": "a3f1c2d4e5b67890abcdef1234567890",
    "category": "Comida",
    "value": 850.0,
    "date": "2026-06-15T14:32:10.123456"
  }
]
```

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `string` | Identificador único generado con `uuid4().hex`. Garantiza que cada gasto sea distinguible incluso con los mismos datos. |
| `category` | `string` | Categoría del gasto, capitalizada y sin espacios sobrantes (ej: `"Transporte"`, `"Comida"`). |
| `value` | `float` | Monto del gasto como número positivo mayor a cero. |
| `date` | `string` | Fecha y hora de registro en formato ISO 8601 (`YYYY-MM-DDTHH:MM:SS.ffffff`), generada automáticamente al momento de agregar el gasto. |

---

## Instalación y requisitos

**Requisitos:**
- Python 3.10 o superior (se usa la sintaxis `str | None` de union types, disponible desde 3.10).
- Cuenta de AWS con un bucket S3 creado y credenciales con permisos `s3:GetObject` y `s3:PutObject`.

**Instalación:**

```bash
git clone https://github.com/tu-usuario/finance_tracker.git
cd finance_tracker
pip install -r requirements.txt
```

**Configuración del entorno:**

Creá un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_DEFAULT_REGION=us-east-1
AWS_S3_BUCKET=nombre-de-tu-bucket
```

> ⚠️ Nunca commitees el archivo `.env`. Ya está incluido en `.gitignore`.

---

## Cómo ejecutar

Desde la raíz del proyecto con el entorno virtual activo:

```bash
streamlit run main.py
```

Streamlit abrirá automáticamente `http://localhost:8501` en el navegador. El sidebar de la izquierda contiene el menú de navegación.

---

## Tests

Los tests están escritos con `unittest` y son compatibles con `pytest`. El cliente S3 es mockeado en todos los tests — no se realizan llamadas reales a AWS.

```bash
# Correr todos los tests
pytest tests/

# Con output detallado
pytest tests/ -v
```

### Cobertura por archivo

| Archivo | Módulo bajo prueba | Qué cubre |
|---|---|---|
| `test_analytics.py` | `analytics.py` | Happy path y casos borde de las cuatro funciones: porcentajes, gastos semanales, día récord y resumen por categoría. Los tests con ventana temporal usan fechas relativas a `datetime.now()`. |
| `test_crud.py` | `crud.py` | Agregar, leer, modificar y borrar gastos con S3 mockeado. Verifica generación de IDs únicos, conversión de `value` a float, retorno en caso de fallo del storage y errores de índice. |
| `test_exports.py` | `exports.py` | Retorno de strings con categorías y totales correctos, gran total acumulado, comportamiento con data vacía, fechas formateadas y separador de columnas. |
| `test_filters.py` | `filters.py` | Categorías únicas, filtrado exacto por categoría, comparación case-sensitive y manejo de lista vacía. |
| `test_validator.py` | `validator.py` | `validate_category`: capitalización, strip, rechazo de vacíos, dígitos y caracteres especiales. `validate_mount`: valores positivos, rechazo de cero, negativos y `None`. |
| `test_vistas.py` | `vistas.py` | `show_summary_cat` y `show_history` con Streamlit mockeado. Verifica retornos, llamadas a `st.dataframe`, `st.warning` y transformación de datos (fechas, capitalización, filtrado de ítems sin categoría). |

---

## Archivos descargables

Al usar las opciones de exportación, el usuario descarga los siguientes archivos directamente desde el navegador:

### `Historial_general.txt`

Reporte agregado con el total por categoría y el gran total acumulado al final.

```
Comida : 700
Transporte : 300
Total Gastado 1000
```

### `Historial_detallado.txt`

Reporte línea por línea con la fecha formateada, categoría y monto de cada gasto.

```
20-06-2026 10:00 | Comida : 500
21-06-2026 15:30 | Transporte : 300
22-06-2026 18:45 | Comida : 200
```

---

## Contribuir

1. Hacé un fork del repositorio y creá una rama descriptiva:
   ```bash
   git checkout -b feature/nombre-de-la-feature
   ```
2. Seguí las convenciones del proyecto: `snake_case` en Python, type hints en todas las funciones, docstrings estilo Google.
3. Mantené las funciones por debajo de 20 líneas. Si crece más, tiene más de una responsabilidad.
4. Toda función nueva de lógica de negocio debe venir con sus tests, cubriendo happy path y casos borde (lista vacía, valores inválidos, fallo del storage).
5. Las credenciales y variables de entorno siempre desde `.env` — nunca hardcodeadas.
6. Abrí un Pull Request con una descripción clara de qué cambia y por qué.
