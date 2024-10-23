from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    combinaciones = set()  # Usamos un set para evitar combinaciones duplicadas
    error_message = ""

    if request.method == 'POST':
        try:
            # Obtener los números enviados desde el formulario
            impares_bajos = list(map(int, filter(None, request.form['impares_bajos'].split(','))))
            pares_bajos = list(map(int, filter(None, request.form['pares_bajos'].split(','))))
            impares_altos = list(map(int, filter(None, request.form['impares_altos'].split(','))))
            pares_altos = list(map(int, filter(None, request.form['pares_altos'].split(','))))

            # Validar que se seleccionaron las cantidades correctas
            if len(impares_bajos) != 3 or len(pares_bajos) != 3 or len(impares_altos) != 3 or len(pares_altos) != 2:
                raise ValueError("Por favor, selecciona los números correctos: 3 impares bajos, 3 pares bajos, 3 impares altos y 2 pares altos.")

            # Generar combinaciones de números
            intentos = 0  # Añadido para evitar un bucle infinito en caso de que no se generen suficientes combinaciones

            while len(combinaciones) < 50 and intentos < 1000:  # Limitar los intentos a 1000 para prevenir un bucle infinito
                intentos += 1
                combinacion = []
                # Elegir 2 impares bajos
                combinacion.extend(random.sample(impares_bajos, 2))
                # Elegir 1 par bajo
                combinacion.append(random.choice(pares_bajos))
                # Elegir 1 impar alto
                combinacion.append(random.choice(impares_altos))
                # Elegir 1 par alto
                combinacion.append(random.choice(pares_altos))

                # Comprobar si hay números consecutivos en la combinación
                if not any(abs(combinacion[i] - combinacion[j]) == 1 for i in range(len(combinacion)) for j in range(i + 1, len(combinacion))):
                    combinacion.sort()  # Ordenar los números de menor a mayor
                    combinaciones.add(tuple(combinacion))  # Añadir la combinación como una tupla para evitar duplicados

            if len(combinaciones) == 0:
                error_message = "No se pudieron generar combinaciones válidas. Intenta nuevamente con otros números."

        except ValueError as e:
            error_message = str(e)

    return render_template('index.html', combinaciones=list(combinaciones), error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
