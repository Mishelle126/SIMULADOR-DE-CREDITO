from flask import Flask, render_template, request, send_file
from utils.generar_pdf import generar_pdf
from utils.generar_excel import generar_excel
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"]
        monto = float(request.form["monto"])
        plazo = int(request.form["plazo"])
        tasa = float(request.form["tasa"])
        tipo_tabla = request.form["tipo_tabla"]

        tabla = []
        saldo = monto
        mes = 1

        if tipo_tabla == "francesa":
            cuota = monto * (tasa / 100) / (1 - (1 + tasa / 100) ** (-plazo))
            for i in range(plazo):
                interes = saldo * (tasa / 100)
                abono = cuota - interes
                saldo -= abono
                tabla.append({
                    "mes": mes,
                    "cuota": round(cuota, 2),
                    "interes": round(interes, 2),
                    "abono": round(abono, 2),
                    "saldo": round(max(saldo, 0), 2)
                })
                mes += 1

        elif tipo_tabla == "alemana":
            abono = monto / plazo
            for i in range(plazo):
                interes = saldo * (tasa / 100)
                cuota = abono + interes
                saldo -= abono
                tabla.append({
                    "mes": mes,
                    "cuota": round(cuota, 2),
                    "interes": round(interes, 2),
                    "abono": round(abono, 2),
                    "saldo": round(max(saldo, 0), 2)
                })
                mes += 1

        return render_template("index.html", nombre=nombre, tabla=tabla, tipo_tabla=tipo_tabla)

    return render_template("index.html")

@app.route("/descargar/pdf", methods=["POST"])
def descargar_pdf():
    tabla = request.json["tabla"]
    buffer = generar_pdf(tabla)
    return send_file(buffer, as_attachment=True, download_name="simulacion.pdf", mimetype="application/pdf")

@app.route("/descargar/excel", methods=["POST"])
def descargar_excel():
    tabla = request.json["tabla"]
    buffer = generar_excel(tabla)
    return send_file(buffer, as_attachment=True, download_name="simulacion.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    app.run(debug=True)
