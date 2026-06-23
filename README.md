# 🧾 Gestor de Gastos Personales

Aplicación de línea de comandos (CLI) para registrar, consultar y analizar gastos personales. Resuelve el problema de llevar un control ordenado del dinero gastado sin necesidad de planillas ni aplicaciones externas. Está dirigida a cualquier persona que quiera tener visibilidad sobre sus gastos desde la terminal, sin dependencias externas ni configuración compleja.

Toda la información se persiste localmente en un archivo `historial.json` que se crea automáticamente al iniciar la aplicación por primera vez.

---

## ✨ Características principales

| Opción | Funcionalidad |
|--------|---------------|
| 1 | Agregar un nuevo gasto (categoría + monto) |
| 2 | Ver resumen de gastos agrupados por categoría |
| 3 | Ver historial completo en consola |
| 4 | Exportar historial detallado a TXT (con fechas y montos) |
| 5 | Exportar resumen general a TXT (totales por categoría) |
| 6 | Borrar un gasto existente (con confirmación) |
| 7 | Modificar categoría y/o monto de un gasto existente |
| 8 | Filtrar y listar todos los gastos de una categoría |
| 9 | Ver porcentaje que representa cada categoría sobre el total |
| 10 | Ver gastos registrados en los últimos 7 días |
| 11 | Ver el día con mayor gasto acumulado del historial |
| 12 | Salir de la aplicación |

---

## 🏗️ Arquitectura del proyecto

El proyecto aplica un patrón de **capas desacopladas** (Layered Architecture). Cada módulo tiene una única responsabilidad y las capas superiores nunca contienen lógica de negocio.

```
finance_tracker/
│
├── main.py              → Punto de entrada. Loop principal que lee el historial,
│                          muestra el menú y delega cada opción a la vista correspondiente.
│
├── menu.py              → Capa de presentación del menú. Muestra las opciones al usuario
│                          y retorna la opción seleccionada como string.
│
├── vistas.py            → Capa de presentación y coordinación de flujos de usuario.
│                          Recibe datos ya procesados y los imprime en consola.
│                          Gestiona los inputs interactivos de agregar, borrar y modificar.
│
├── crud.py              → Capa de persistencia. Única responsable de leer y escribir
│                          historial.json. Expone: read_history, add_expense,
│                          delete_expense, modify_expense.
│
├── analytics.py         → Capa de lógica de negocio. Cálculos y transformaciones puras
│                          sobre los datos: porcentajes, resumen por categoría,
│                          filtro semanal, día de mayor gasto, promedios.
│
├── filters.py           → Helpers de filtrado stateless: obtener categorías únicas
│                          y filtrar gastos por categoría.
│
├── exports.py           → Capa de salida a archivos. Genera resumen_general.txt
│                          y resumen_detalado.txt a partir de los datos del historial.
│
├── historial.json       → Base de datos local (JSON). Se crea automáticamente.
│
├── tests/
│   ├── test_analytics.py
│   ├── test_crud.py
│   └── test_filters.py
│
├── resumen_general.txt  → Generado por la opción 5
└── resumen_detalado.txt → Generado por la opción 4
```

### Flujo de datos

```
Usuario
  └─→ menu.py     →  main.py (router por opción)
                        ├─→ crud.py        (R/W sobre historial.json)
                        ├─→ analytics.py   (cálculos sobre los datos)
                        ├─→ filters.py     (filtros helpers)
                        ├─→ exports.py     (escritura de archivos TXT)
                        └─→ vistas.py      (presentación en consola + inputs)
```

**Principio clave:** `vistas.py` nunca toca el archivo JSON directamente — llama a `crud.py` para escrituras. `analytics.py` y `filters.py` son funciones puras que reciben datos y devuelven resultados sin efectos secundarios.

---

## 📦 Modelo de datos

Cada gasto se almacena como un objeto dentro del array en `historial.json`:

```json
[
  {
    "id": "a3f2c1d4e5b67890abcdef1234567890",
    "category": "Comida",
    "value": 500,
    "date": "2026-06-23T14:30:00.123456"
  }
]
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | `string` | Identificador único generado con `uuid.uuid4().hex`. 32 caracteres hexadecimales. |
| `category` | `string` | Categoría del gasto. Se almacena capitalizada y sin espacios sobrantes. Solo letras. |
| `value` | `int` | Monto del gasto. Se valida como entero positivo al momento de la carga. |
| `date` | `string` | Fecha y hora de registro en formato ISO 8601, generada con `datetime.now().isoformat()`. |

---

## ⚙️ Instalación y requisitos

**Requisitos del sistema:**
- Python **3.8** o superior
- No requiere dependencias externas — utiliza únicamente la biblioteca estándar de Python (`json`, `os`, `uuid`, `datetime`)

**Pasos de instalación:**

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd finance_tracker

# 2. (Recomendado) Crear y activar un entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 3. No hay dependencias que instalar
# El proyecto funciona con la stdlib de Python directamente
```

> Para correr los tests necesitás `pytest`. Instalarlo con:
> ```bash
> pip install pytest
> ```

---

## ▶️ Cómo ejecutar

```bash
python main.py
```

Al iniciarse, si `historial.json` no existe en el directorio actual, se crea automáticamente con un array vacío. El menú interactivo aparece de inmediato en la consola.

> **Importante:** el archivo `historial.json` se crea en el directorio desde donde se corre el comando, no necesariamente en la raíz del proyecto. Se recomienda siempre ejecutar desde la raíz del repositorio.

---

## 🧪 Tests

Los tests están escritos con `unittest` y son compatibles con `pytest` como runner.

```bash
# Desde la raíz del proyecto
pytest tests/

# Con salida detallada
pytest tests/ -v
```

### Cobertura actual

| Archivo de test | Módulo testeado | Casos cubiertos |
|-----------------|----------------|-----------------|
| `test_crud.py` | `crud.py` | Agregar gasto, eliminar gasto, modificar categoría, modificar monto, modificar ambos campos simultáneamente |
| `test_analytics.py` | `analytics.py` | Cálculo de porcentaje por categoría, filtro de gastos semanales, día con mayor gasto, resumen por categoría, promedio diario de la semana, promedio histórico por días únicos |
| `test_filters.py` | `filters.py` | Obtener categorías únicas, filtrar gastos por categoría exacta |

**Nota sobre aislamiento:** `test_crud.py` limpia `historial.json` antes de cada test mediante `setUp`, garantizando que los casos no se interfieran entre sí.

**Nota sobre fechas en tests:** `test_analytics.py` usa fechas fijas (febrero 2026). El test `test_get_week_expenses` puede devolver una lista vacía si se corre hoy, ya que esas fechas caen fuera de la ventana de 7 días. El resto de los tests no dependen de la fecha actual.

---

## 📄 Archivos generados

La aplicación puede generar dos archivos de texto en el directorio de ejecución:

### `resumen_general.txt` — Opción 5

Contiene el total gastado por categoría y el gran total acumulado.

```
Comida : 1200

Transporte : 450

Total Gastado 1650
```

### `resumen_detalado.txt` — Opción 4

Contiene cada gasto individual con su fecha completa en formato ISO, categoría y monto.

```
2026-06-20T10:00:00.000000 | Comida : 500

2026-06-21T15:30:00.000000 | Transporte : 300
```

> El nombre `resumen_detalado.txt` (con una sola `l`) corresponde al nombre definido en `exports.py`. Si se corrige el typo en el código, el archivo generado cambiará de nombre.

---

## 🤝 Contribuir

1. Hacé un fork del repositorio
2. Creá una rama descriptiva:
   ```bash
   git checkout -b feature/nombre-de-la-funcionalidad
   ```
3. Seguí las convenciones del proyecto:
   - `snake_case` para variables y funciones en Python
   - Type hints en todos los argumentos y retornos
   - Funciones de no más de 20 líneas
   - Guard clauses para validar inputs antes de la lógica principal
4. Agregá tests unitarios para cualquier función de lógica nueva en `tests/`
5. Verificá que los tests existentes siguen pasando:
   ```bash
   pytest tests/ -v
   ```
6. Abrí un Pull Request con una descripción clara del cambio y qué problema resuelve

---

*Desarrollado en Python puro · Sin dependencias externas · Persistencia local en JSON*
