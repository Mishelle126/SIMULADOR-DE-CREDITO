from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generar_pdf(tabla):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 40, "Simulación de Crédito")

    y = height - 70
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Mes")
    c.drawString(100, y, "Cuota")
    c.drawString(170, y, "Capital")
    c.drawString(240, y, "Interés")
    c.drawString(310, y, "Saldo")
    c.setFont("Helvetica", 10)
    y -= 20

    for idx, fila in enumerate(tabla, start=1):
        c.drawString(50, y, str(idx))
        c.drawString(100, y, f"{fila['cuota']:.2f}")
        c.drawString(170, y, f"{fila['abono']:.2f}")
        c.drawString(240, y, f"{fila['interes']:.2f}")
        c.drawString(310, y, f"{fila['saldo']:.2f}")

        y -= 20
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
    buffer.seek(0)
    return buffer
