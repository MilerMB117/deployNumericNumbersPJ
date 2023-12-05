from io import BytesIO
from flask import Flask, render_template, request
import webbrowser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from sympy import symbols, lambdify, solve
import base64
from sympy import N


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('result.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/calculate', methods=['POST'])
def calculate():
    equation_str = request.form['equation']
    method = request.form['method']

    x = symbols('x')
    equation_sym = lambdify(x, equation_str, 'numpy')
    equation_num = lambdify(x, equation_str, 'numpy')

    x_values = np.linspace(-10, 10, 100)
    y_values_f = equation_num(x_values)
    y_values_g = equation_sym(x_values)

    fig, ax = plt.subplots()
    ax.plot(x_values, y_values_f, label="f(x)")
    ax.plot(x_values, y_values_g, label="g(x)")
    ax.set_title("Gráfico de la Función")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()

    canvas = FigureCanvas(fig)
    img_data = BytesIO()
    canvas.print_png(img_data)
    img_data.seek(0)
    root, error = calculate_root_and_error(equation_sym, equation_num)

    # Agregado: Codificar la imagen en base64
    encoded_img_data = base64.b64encode(img_data.read()).decode('utf-8')

    # Agregado: Calcular puntos para la tabla
    x_values_table = np.linspace(-10, 10, 10)
    g_values_table = equation_num(x_values_table)
    f_values_table = equation_sym(x_values_table)

    # Agregado: Crear lista de puntos para pasar a la plantilla HTML
    points = [{'x': x, 'gx': gx, 'fx': fx} for x, gx, fx in zip(x_values_table, g_values_table, f_values_table)]
    
    # Agregado: Calcular la raíz utilizando SymPy
    x = symbols('x')
    try:
        root = N(solve(equation_sym(x), x)[0])
    except IndexError:
        root = "No se pudo calcular la raíz"

    # Agregado: Calcular el porcentaje de error
    error = np.abs((equation_num(root) - equation_sym(root)) / equation_sym(root)) if root != "No se pudo calcular la raíz" else float('nan')

    # Agregado: Presentar el porcentaje de error
    formatted_error = f"{error:.6%}" if isinstance(error, (int, float)) and not np.isnan(error) and not np.isinf(error) else "Error no válido"

    return render_template('result.html', encoded_img_data=encoded_img_data, root=root, error=formatted_error, points=points)
    

def calculate_root_and_error(equation_sym, equation_num):
    x = symbols('x')
    root = solve(equation_sym(x), x)[0]
    error = np.abs((equation_num(root) - equation_sym(root)) / equation_sym(root))
    return root, error

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
