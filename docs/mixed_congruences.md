# Generador de Congruencias Mixtas

## Fundamentación

El generador de números aleatorios basado en el método de **Congruencias Mixtas** utiliza la siguiente fórmula iterativa:

<div align="center">
  V<sub>i+1</sub> = (A × V<sub>i</sub> + C) mod M
</div>

donde:
- **V<sub>i</sub>** es la semilla o número generado en la iteración *i*.
- **A** es el multiplicador.
- **C** es el incremento.
- **M** es el módulo.

El algoritmo comienza con una semilla inicial y, para cada iteración, calcula un nuevo número basándose en la fórmula anterior. Este proceso se repite *n* veces hasta satisfacer la cantidad de números aleatorios solicitados.

En nuestro sistema, el método de congruencias mixtas está implementado mediante el uso de un esquema **Modelo – Vista – Controlador (MVC)**, donde la lógica del generador se encuentra en el controlador, dentro de la función `mixed_congruence` de la clase `MainController`. El código realiza lo siguiente:

1. Se reciben como parámetros la semilla y los valores **A**, **M** y **C**, junto con el número de dígitos a generar.
2. En cada iteración, se actualiza el valor de la semilla aplicando la fórmula mencionada y se agrega el nuevo número a la lista de números generados.
3. La lista completa de números generados se retorna para ser mostrada en la interfaz.

En el apartado de las vistas, la interfaz correspondiente al método de congruencias mixtas se encuentra en el archivo `mixed_congruence_view.py`. La pantalla dispone de campos de entrada para la semilla, los parámetros **A**, **M** y **C**, un campo para definir la cantidad de números a generar y un botón **"Generar"** que conecta con el controlador para iniciar el proceso de generación.

## Criterios de Aceptación

El generador de números pseudoaleatorios mediante el método mixto de congruencias debe cumplir lo siguiente:

1. **Validación de Entradas:**
   - La semilla debe ser un valor numérico entero mayor que 0.
   - Los parámetros **A**, **M** y **C** deben ser valores numéricos enteros y deben cumplir:
     - **A**: debe ser impar y no divisible por 3 ni por 5.
     - **M**: debe ser mayor que **A** y mayor que la semilla.
     - **C**: debe ser impar y relativamente primo a **M**.
   - La cantidad de números a generar debe ser un entero positivo y no exceder el límite de 10,000 números.

2. **Generación Correcta:**
   - El programa debe generar exactamente la cantidad de números solicitados.
   - Cada número generado debe calcularse aplicando la fórmula del método de congruencias mixtas.

3. **Interfaz de Usuario:**
   - La interfaz debe contar con los campos para la entrada de la semilla, los parámetros y la cantidad de números a generar.
   - Debe tener un botón **"Generar"** para iniciar el proceso.
   - En caso de error, la pantalla debe mostrar un mensaje de error.

4. **Manejo de Errores:**
   - El sistema debe detener la ejecución e informar al usuario acerca del error que se ha producido.

## Casos de Uso

### CU 1: Generación de Números Aleatorios
- **Actor:** Usuario final / Operador del sistema  
- **Precondición:**
  - El usuario debe disponer de una semilla válida.
  - Los parámetros **A**, **M** y **C** deben cumplir las reglas para el funcionamiento del método.
- **Postcondición:**
  - Se muestra en la interfaz la lista de números pseudoaleatorios generados por el método de congruencias mixtas.

**Flujo Principal:**

1. El usuario ingresa la semilla y los parámetros **A**, **M** y **C** en sus respectivos campos de la interfaz.
2. El usuario ingresa la cantidad de números a generar.
3. El usuario pulsa el botón **"Generar"**.
4. El sistema valida los datos:
   - Verifica que la semilla y los parámetros sean numéricos y cumplan las reglas.
   - Verifica que la cantidad de números a generar sea un entero positivo y esté dentro del rango permitido.
5. Si la validación es correcta, el sistema muestra un mensaje de **"Generando números..."** y deshabilita temporalmente el botón para evitar múltiples invocaciones.
6. Se genera la lista de números utilizando el método de congruencias mixtas.
7. El sistema muestra la lista de números generados en el área de resultados y vuelve a habilitar el botón.

**Flujo Alternativo:**

- Si el usuario ingresa datos inválidos, el sistema detecta el error, muestra un mensaje al usuario y detiene la ejecución para permitir la corrección.

## Documentación de las Pruebas

A continuación, se describe brevemente cada grupo de pruebas realizadas (ver `test_main_controller.py`):

- **Pruebas Unitarias de Validación:**
  - **`test_validate_mixed_parameters_valid` y `test_validate_mixed_parameters_invalid`:**  
    Aseguran que los parámetros **A**, **M** y **C** cumplan las reglas establecidas.
  - **`test_validate_digits_valid` y `test_validate_digits_invalid`:**  
    Verifican que la cantidad de dígitos se valide correctamente, aceptando valores dentro del rango permitido y rechazando valores fuera de rango o no numéricos.

- **Pruebas de Generación:**
  - **`test_mixed_congruence`:**  
    Verifica que el método de congruencias mixtas devuelva la cantidad correcta de números aleatorios con parámetros válidos.

- **Pruebas de Manejo de Errores:**
  - **`test_on_generate_mixed_invalid_parameters`:**  
    Simula entradas inválidas para los parámetros **A**, **M** y **C** y verifica que se muestre el mensaje de error adecuado.

- **Otros Aspectos:**
  - Se utiliza un controlador dummy (simulado con `MagicMock`) para testear la interacción sin depender de la interfaz gráfica real.
  - Se verifica que las funciones de actualización de la interfaz (como `error_message`, `loading` y `paste_result`) actualicen correctamente el TextBox.

