# Persistencia

El componente de persistencia de nuestro sistema está a cargo de la clase `Database`, que utiliza `psycopg2` para conectarse a un servidor **PostgreSQL** y garantizar que tanto los resultados de **Von Neumann** como los de **Congruencias Mixtas** queden guardados de forma estructurada.

---

## Conexión inicial

Al instanciar `Database()`, en el constructor (`__init__`) se intenta abrir una conexión con `psycopg2.connect(...)`, usando los siguientes parámetros:

- `host`: `"localhost"`
- `port`: `"5432"`
- `database`: `"RandomNumbersDB"`
- `user`: `"postgres"`
- `password`: `"magna"`

Si la conexión falla (credenciales incorrectas, servidor caído, etc.), se muestra un `MessageBox` de error:

> “No se pudo conectar a la base de datos: <mensaje de excepción>”

Y `self.connection` queda en `None`.

Por otra parte, si la conexión es exitosa, se crea también:  
`self.cursor = self.connection.cursor()`

---

## Creación de tablas

Justo después de abrir la conexión, se invoca `create_tables()`.  
En este método, utilizando el cursor, se ejecutan dos sentencias `CREATE TABLE IF NOT EXISTS`:

### `vn_results`

- `id SERIAL PRIMARY KEY`
- `seed INTEGER NOT NULL`
- `random_numbers TEXT NOT NULL` (cadena con los números separados por comas)
- `chi_square_result BOOLEAN`
- `rachas_result BOOLEAN`
- `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`

### `mixed_congruence_results`

- Mismos campos que `vn_results` más:
  - `a INTEGER NOT NULL`
  - `m INTEGER NOT NULL`
  - `c INTEGER NOT NULL`

Tras cada bloque de creación de tablas, se hace `self.connection.commit()` para asegurar que las tablas queden persistidas.

Si ocurre un error al crear las tablas, se muestra un `MessageBox` de error y se invoca `self.connection.rollback()` para deshacer cambios parciales.

---

## Ejecución general de consultas

Además del constructor y la creación de tablas, la clase expone un método `execute(query, params=None)`:

- Si `self.cursor` existe, intenta ejecutar la consulta SQL recibida;  
  si `params` está presente, llama a `cursor.execute(query, params)`,  
  de lo contrario `cursor.execute(query)`.
- Retorna `True` si la ejecución fue exitosa; en caso de excepción, se muestra un `MessageBox` detallando el error y devuelve `False`.
- Este método puede usarse para cualquier operación de lectura o escritura,  
  aunque en nuestro diseño los métodos de guardado usan directamente `cursor.execute` y `commit`.

---

## Integración con los servicios y el controlador

Los servicios `MainService.save_von_neuman_result(...)` y `save_mixed_congruence_result(...)` reciben como primer argumento la conexión (`db_connection`) proporcionada por `Database().connection`.

Internamente:

- Abren su propio cursor (`db_connection.cursor()`).
- Ejecutan la sentencia `INSERT INTO … VALUES(%s,…)` con los parámetros adecuados:  
  semilla, parámetros, lista de números convertida a cadena, resultados booleanos de las pruebas.
- Luego hacen `db_connection.commit()`.

El controlador (`MainController`) se encarga de:

- Desactivar temporalmente botones en la UI mientras guarda.
- Pasar la semilla, parámetros y los flags `chi_result` y `rachas_result` (`True` o `False`) al servicio.
- Informar al usuario con un `MessageBox` de éxito o error según el valor booleano que retorne el método de guardado.