# Prueba de Chi Cuadrado

## Fundamentación

El propósito de la prueba de Chi Cuadrado en nuestro sistema es evaluar si, al extraer el dígito final de cada número generado (sea por el método de Von Neumann o por congruencias mixtas), la frecuencia con que aparecen los dígitos (0, 1, 2… 9) se ajusta a lo que esperaríamos de un proceso verdaderamente aleatorio. Es decir, que cada uno de los diez posibles dígitos tenga, en promedio, la misma probabilidad de salir.

---

## Teoría

1. Para **N** números generados, la frecuencia esperada de cada dígito *i* ∈ {0,…,9} es:  
   <div align="center">
     E = N / 10
   </div>

2. Se cuenta, para cada dígito *i* (0…9), cuántas veces apareció como resto módulo 10 de los números generados. Llamamos a estas frecuencias **observadas** `O₀, O₁, …, O₉`.

3. Para cada dígito comparamos la frecuencia observada `Oᵢ` con la esperada `E` mediante la fórmula:  
   <div align="center">
     (O<sub>i</sub> – E)² / E
   </div>  
   Luego sumamos las diez contribuciones para obtener:  
   <div align="center">
     χ² = ∑<sub>i=0</sub>⁹ (O<sub>i</sub> – E)² / E
   </div>

4. Con *k* = 10 – 1 = 9 grados de libertad y un nivel de significancia α = 0.05, el valor crítico es:  
   <div align="center">
     χ²<sub>0.95</sub> ≈ 16.919
   </div>  
   Interpretación:  
   - Si χ² < 16.919 → desviación pequeña → aceptamos la hipótesis nula (homogeneidad).  
   - Si χ² ≥ 16.919 → desviación grande → rechazamos la hipótesis nula (sesgo en la generación).

---

## Implementación en el sistema

El método `run_chi_square_test(textbox, result_textbox)` de `MainService` sigue estos pasos:

1. Lee la cadena del textbox principal (lista separada por comas) y convierte cada fragmento a `int`.
2. Reduce cada número a su dígito final en base 10:  
   `numbers[i] = numbers[i] % 10`
3. Cuenta la frecuencia observada de cada dígito en un array de tamaño 10.
4. Calcula:
   - Frecuencia esperada.
   - Estadístico χ² con la fórmula estándar.
5. Hace una comparación contra el valor crítico **16.919** para decidir si los números pasan la prueba o no.
6. Muestra en `result_textbox`:
   - Lista de frecuencias observadas por dígito
   - Valor de χ²
   - Valor crítico
   - Resultado final

Además del método para la prueba, existen validaciones y mensajes que le informan al usuario si los números evaluados pasan la prueba o no.

---

# Casos de Uso

## CU 01: Ejecutar prueba de Chi Cuadrado

- **Actor:** Usuario  
- **Precondición:** El usuario ha generado números (Von Neumann o Mixto).  
- **Salida:** El resultado de la prueba realizada sobre los números generados.

#### Flujo principal

1. El usuario selecciona “Chi Cuadrado” en el grupo de radio buttons.
2. El usuario pulsa “Ejecutar Prueba”.
3. El controlador (a través de los métodos `on_test_von_neumann` / `on_test_mixed`) invoca al método  
   `MainService.run_chi_square_test(view.result_textbox, view.test_result_textbox)`.
4. El servicio calcula el estadístico χ², lo compara con **16.919** y retorna `True` (pasa) o `False` (no pasa).
5. Dependiendo del resultado, el sistema muestra un `messagebox` alertando al usuario del resultado de la prueba.
6. La pantalla colorea el radio (`chi_radio`) de verde si pasa o rojo si no, y muestra el detalle en `test_result_textbox`.

#### Flujo alternativo

- Si no hay ningún número válido en `view.result_textbox`, se invoca  
  `MessageBox.show_error("Error", "No se han generado números válidos…")` y se interrumpe el flujo.

---

## CU 02: Guardar resultado de la prueba

- **Actor:** Usuario  
- **Precondición:** La prueba de Chi Cuadrado ha pasado (radio verde).

#### Flujo principal

1. El usuario pulsa el botón “Guardar”.
2. El controlador invoca a los métodos  
   `MainService.save_von_neuman_result(...)` o  
   `MainService.save_mixed_congruence_result(...)`, incluyendo el flag `chi_result=True`.  
   (Es decir, solo se guardan los parámetros si los números generados pasaron la prueba).
3. Los datos se insertan en la tabla `vn_results` o `mixed_congruence_results`.
4. Se muestra un `Info Box` con “Resultados guardados en la base de datos.”

---

# Criterios de Aceptación

Para que la prueba programada sea de utilidad, deben satisfacerse los siguientes requisitos:

## 1. Validación de entrada

- Debe haber al menos un número entero en la caja de texto de la pantalla.
- Si no hay ningún número, se debe mostrar un error y no avanzar con el cálculo.

## 2. Cálculo correcto

- La frecuencia esperada **E** debe calcularse correctamente.
- El estadístico **χ²** debe calcularse correctamente.
- Se debe usar el valor crítico **16.919** para la decisión.

## 3. Interfaz de Usuario

- La interfaz debe ser capaz de mostrar un mensaje que le informe al usuario sobre el resultado de la prueba.
- También debe ser capaz de mostrar el resultado de la prueba y los valores que intervinieron.

## 4. Manejo de errores

- Si no hay números o la conversión falla, se debe mostrar un mensaje de error claro.