# Fundamentación

La **Prueba de Rachas** tiene como objetivo verificar si, al convertir la lista de números generados en una secuencia binaria, la cantidad de “rachas” (cambios de 0 a 1 o de 1 a 0) se ajusta a lo que esperaríamos de una secuencia aleatoria con probabilidad *p = 0.5*. Aclaremos que se entiende por **racha** a una sucesión ininterrumpida de bits idénticos; su análisis estadístico es importante para ver si existen patrones de exceso o escasez de cambios que impliquen sesgos en el generador.

## Teoría

1. Cada número entero de la lista se convierte a su representación binaria con un ancho fijo igual al número mínimo de bits necesarios para representar el valor máximo en la lista.

2. Todas esas representaciones se concatenan para formar una única cadena de bits de longitud total *n*.

3. Recorremos la cadena de bits de izquierda a derecha contando desde 1 racha, luego cada vez que el bit cambie respecto al anterior incrementamos el contador de las rachas observadas *(Robs)*.

4. Se hacen los siguientes cálculos:

- **Media esperada de rachas**  
  μR = 1 + (n - 1) / 2

- **Varianza de rachas**  
  σR² = (n(n - 2)) / (4(n - 1))

- **Desvío estándar**  
  σR = √(σR²)

  5. A partir de estos datos, se puede calcular el estadístico Z:
   
- **Estadístico Z**  
  Z = (Robs - μR) / σR

6. Con nivel de confianza del 95% se compara contra ±1.96:
- Si |Z| ≤ 1.96, aceptamos la hipótesis nula de aleatoriedad.
- Si |Z| > 1.96, rechazamos la hipótesis y concluimos que hay demasiadas o muy pocas rachas.

---

# Implementación en el sistema

El método `run_rachas_test(view)` de `MainService` realiza exactamente estos pasos:

- Extrae del primer textbox la cadena de números separados por comas.
- La lista se filtra y convierte sus elementos a enteros; si no hay números *(n == 0)*, se muestra un error y se aborta.
- Se halla el valor máximo de la lista y se obtiene su tamaño en bits (`bits = max_number.bit_length()`), garantizando al menos 1 bit.
- Cada número se transforma a una cadena binaria de longitud fija `bits` con ceros a la izquierda.
- Todas esas cadenas se recorren bit a bit, comparando con el bit anterior (`prev_bit`), y cada vez que cambian se incrementa el contador de rachas. El contador siempre arranca en 1 (siempre hay al menos una racha).
- Se hacen los cálculos de **μR**, **σR²**, y **σR** siguiendo las fórmulas explicadas con anterioridad.
- Se calcula el valor de **Z** para luego tomar la decisión con un valor crítico de 1.96 (95% de confianza). Devuelve `True` (aceptado) si |Z| < 1.96 o `False` (rechazado) en caso contrario.
- Se vuelcan en `result_textbox` los siguientes resultados:
- `Rachas: {runs}`
- `Valor Z: {z}`
- `Valor crítico: 1.96`
- `Resultado: Aceptado` o `Rechazado`

---

# Casos de Uso

## CU 01: Ejecutar prueba de Rachas

- **Actor**: Usuario  
- **Precondición**: El usuario ha generado números (Von Neumann o Mixto).  
- **Salida**: El resultado de la prueba realizada sobre los números generados.

### Flujo principal

1. El usuario selecciona “Rachas” en el grupo de radio buttons.
2. El usuario pulsa “Ejecutar Prueba”.
3. El controlador (a través de los métodos `on_test_von_neumann` / `on_test_mixed`) invoca al método `MainService.run_rachas_test(view.result_textbox, view.test_result_textbox)`.
4. El servicio calcula el estadístico Z, lo compara con 1.96 y retorna `True` (pasa) o `False` (no pasa).
5. Dependiendo del resultado, el sistema muestra un `messagebox` alertando al usuario del resultado de la prueba.
6. La pantalla colorea el radio (`rachas_radio`) de verde si pasa o rojo si no, y muestra el detalle en `test_result_textbox`.

### Flujo alternativo

- Si no hay ningún número válido en `view.result_textbox`, se invoca:  
`MessageBox.show_error("Error", "No se han generado números válidos…")`  
y se interrumpe el flujo.

---

## CU 02: Guardar resultado de la prueba

- **Actor**: Usuario  
- **Precondición**: La prueba de Rachas ha pasado (radio verde).

### Flujo principal

1. El usuario pulsa el botón “Guardar”.
2. El controlador invoca a los métodos  
`MainService.save_von_neuman_result(...)` o  
`MainService.save_mixed_congruence_result(...)`,  
incluyendo el flag `rachas_result=True`.  
*(Es decir, solo se guardan los parámetros si los números generados pasaron la prueba).*
3. Los datos se insertan en la tabla `vn_results` o `mixed_congruence_results`.
4. Se muestra un `Info Box` con “Resultados guardados en la base de datos.”

---

# Criterios de Aceptación

Para que la prueba programada sea de utilidad, deben satisfacerse los siguientes requisitos:

1. **Validación de entrada**  
- La lista debe contener al menos un entero; de lo contrario se muestra un mensaje de error y no se realiza ningún cálculo.

2. **Cálculo correcto**  
- Se debe usar el ancho de bits mínimo necesario para representar al número más grande de la lista. Esto con la finalidad de evitar agregar bits innecesarios que alteren la prueba.
- El contador de rachas debe incrementarse exactamente en cada punto de cambio de bit.
- Los cálculos de **μR**, **σR²**, y **σR** deben seguir las fórmulas establecidas correctamente.
- El estadístico **Z** se debe calcular mediante la fórmula establecida.
- Se debe comparar **Z** contra 1.96, que representa un error del 0.05.

3. **Interfaz de Usuario**  
- La interfaz debe ser capaz de mostrar un mensaje que le informe al usuario sobre el resultado de la prueba.
- También debe ser capaz de mostrar el resultado de la prueba y los valores que intervinieron.

4. **Manejo de errores**  
- Si no hay números o la conversión falla, se debe mostrar un mensaje de error claro.
