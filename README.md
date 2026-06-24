# Finance Tracker 🧾

Gestor de gastos personales por línea de comandos escrito en Python puro. Permite registrar, consultar, modificar, filtrar y exportar gastos de forma persistente sin necesidad de base de datos ni dependencias externas.

Está pensado para quienes quieren un control simple de sus finanzas personales directamente desde la terminal, con datos almacenados localmente en un archivo JSON.

---

## Características principales

- **Agregar gastos** — Registra un gasto con categoría, monto y fecha/hora automática.
- **Ver historial completo** — Lista todos los gastos con fecha, categoría y monto.
- **Resumen por categoría** — Muestra el total acumulado agrupado por categoría.
- **Porcentaje por categoría** — Calcula qué porcentaje del total representa cada categoría.
- **Gastos de los últimos 7 días** — Filtra y ordena los gastos de la última semana del más reciente al más antiguo.
- **Día con mayor gasto** — Identifica el día del historial con mayor desembolso acumulado.
- **Filtrar por categoría** — Muestra todos los gastos de una categoría elegida.
- **Modificar un gasto** — Cambia la categoría y/o el monto de un gasto existente, con preview y confirmación antes de persistir.
- **Borrar un gasto** — Elimina un gasto del historial con confirmación previa.
- **Exportar resumen general a TXT** — Genera `resumen_general.txt` con el total por categoría y el gran total acumulado.
- **Exportar historial detallado a TXT** — Genera `resumen_detallado.txt` con fecha, categoría y monto de cada gasto.

---

## Arquitectura del proyecto

```
finance_tracker/
├── main.py           # Punto de entrada. Loop principal y enrutamiento de opciones.
├── menu.py           # Presentación del menú y captura de input del usuario.
├── vistas.py         # Capa de presentación: flujos interactivos y output en consola.
├── crud.py           # Capa de persistencia: lectura y escritura sobre historial.json.
├── analytics.py      # Capa de negocio: cálculos y análisis sobre los datos.
├── filters.py        # Helpers de filtrado stateless sobre la lista de gastos.
├── exports.py        # Capa de exportación: generación de reportes TXT.
├── validator.py      # Validación y normalización de inputs del usuario.
├── historial.json    # Base de datos local con el historial de gastos.
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
| `main.py` | Punto de entrada. Lee el historial en cada iteración, muestra el menú y delega cada opción a la vista correspondiente. No contiene lógica de negocio. |
| `menu.py` | Exclusivamente muestra el menú en consola y retorna la opción elegida como string. |
| `vistas.py` | Capa de presentación. Gestiona los flujos interactivos (inputs, confirmaciones, output formateado). Delega toda persistencia a `crud.py` y todos los cálculos a `analytics.py`. |
| `crud.py` | Única capa que accede a `historial.json`. Expone funciones para leer, agregar, modificar y eliminar gastos. |
| `analytics.py` | Funciones puras de análisis: porcentajes, promedios, agrupaciones y filtros temporales. No accede a archivos ni modifica estado global. |
| `filters.py` | Helpers stateless para obtener categorías únicas y filtrar la lista por categoría. |
| `exports.py` | Genera archivos TXT de reporte. Delega los cálculos a `analytics.py` y no accede a `historial.json` directamente. |
| `validator.py` | Valida y normaliza los inputs del usuario (categoría y monto) antes de que lleguen a la capa de persistencia. |

---

## Modelo de datos

Los gastos se persisten en `historial.json` como un array de objetos JSON:

```json
[
  {
    "id": "a3f1c2d4e5b67890abcdef1234567890",
    "category": "Comida",
    "value": 850,
    "date": "2026-06-15T14:32:10.123456"
  }
]
```

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `string` | Identificador único generado con `uuid4().hex`. Garantiza que cada gasto sea distinguible incluso con los mismos datos. |
| `category` | `string` | Categoría del gasto, capitalizada y sin espacios sobrantes (ej: `"Transporte"`, `"Comida"`). |
| `value` | `integer` | Monto del gasto como entero positivo. No se admiten decimales ni valores negativos. |
| `date` | `string` | Fecha y hora de registro en formato ISO 8601 (`YYYY-MM-DDTHH:MM:SS.ffffff`), generada automáticamente al momento de agregar el gasto. |

---

## Instalación y requisitos

**Requisitos:**
- Python 3.10 o superior (se utiliza la sintaxis `str | None` de union types, disponible desde 3.10).
- No requiere dependencias externas. Todo el proyecto usa la biblioteca estándar de Python.
- Para correr los tests se necesita `pytest`:

```bash
pip install pytest
```

**Instalación:**

```bash
git clone https://github.com/tu-usuario/finance_tracker.git
cd finance_tracker
```

---

## Cómo ejecutar

Desde la raíz del proyecto:

```bash
python main.py
```

Se abrirá el menú interactivo en la terminal. Ingresá el número de la opción deseada y presioná Enter.

```
=====================================
     GESTOR DE GASTOS 🧾
=====================================

Elija una opción:

1) Agregar un nuevo gasto
2) Ver resumen por categoría
3) Ver historial completo en consola
...
12) Salir
```

---

## Tests

Los tests están escritos con `unittest` y son compatibles con `pytest`. Para ejecutarlos desde la raíz del proyecto:

```bash
# Correr todos los tests
pytest tests/

# Con output detallado
pytest tests/ -v
```

> **Nota:** los tests de `test_crud.py` y `test_exports.py` leen y escriben archivos en el directorio desde donde se ejecuta `pytest`. Correrlos desde la raíz garantiza que encuentren `historial.json` correctamente.

### Cobertura por archivo

| Archivo | Módulo bajo prueba | Qué cubre |
|---|---|---|
| `test_analytics.py` | `analytics.py` | Happy path y casos borde de las seis funciones públicas: porcentajes, gastos semanales, día con mayor gasto, resumen por categoría, promedio diario e histórico. Los tests que dependen de la ventana temporal usan `datetime.now() - timedelta(...)` para no fallar con el paso del tiempo. |
| `test_crud.py` | `crud.py` | Agregar, leer, modificar y borrar gastos. Verifica generación de IDs únicos, manejo de JSON corrupto, creación automática del archivo si no existe, y que el borrado no afecte ítems adyacentes. |
| `test_exports.py` | `exports.py` | Creación de archivos, contenido correcto de categorías y totales, grand total acumulado, y comportamiento con data vacía para ambas funciones de exportación. Limpia los archivos generados después de cada test con `tearDown`. |
| `test_filters.py` | `filters.py` | Obtención de categorías únicas y filtrado por categoría. |
| `test_validator.py` | `validator.py` | `validate_category`: capitalización, strip de espacios, rechazo de strings vacíos, solo espacios, con dígitos y caracteres especiales. `validate_mount`: retorno como entero, rechazo de cero, string vacío, floats, negativos y texto. |
| `test_vistas.py` | `vistas.py` | `process_expense_modification`: índice fuera de rango, no numérico, cero, modificación con confirmación Y/N, campos vacíos. Funciones de display (`show_history`, `show_top_expenses`, `show_summary_cat`, `show_percentage`) verificadas con mocks de `print()` e `input()`. |

---

## Archivos generados

Al usar las opciones de exportación, el proyecto genera los siguientes archivos en el directorio raíz:

### `resumen_general.txt`

Reporte agregado con el total gastado por categoría y el gran total acumulado al final.

```
Comida : 700

Transporte : 300

Total Gastado 1000
```

### `resumen_detallado.txt`

Reporte línea por línea con la fecha completa ISO 8601, categoría y monto de cada gasto registrado.

```
2026-06-20T10:00:00 | Comida : 500

2026-06-21T15:30:00 | Transporte : 300

2026-06-22T18:45:00 | Comida : 200
```

Ambos archivos se sobreescriben completamente cada vez que se ejecuta la exportación correspondiente.

---

## Contribuir

1. Hacé un fork del repositorio y creá una rama descriptiva:
   ```bash
   git checkout -b feature/nombre-de-la-feature
   ```
2. Seguí las convenciones del proyecto: `snake_case` en Python, type hints en todas las funciones y retornos, docstrings estilo Google.
3. Mantené las funciones por debajo de 20 líneas. Si una función crece más, es señal de que tiene más de una responsabilidad.
4. Toda función nueva de lógica de negocio debe venir acompañada de sus tests en `tests/`, cubriendo el happy path y los casos borde principales (lista vacía, valores inválidos, etc.).
5. Abrí un Pull Request con una descripción clara de qué cambia y por qué.
