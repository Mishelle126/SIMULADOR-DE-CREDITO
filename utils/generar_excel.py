from openpyxl import Workbook
import io

def generar_excel(tabla):
    wb = Workbook()
    ws = wb.active
    ws.title = "Simulación de Crédito"
    
    # Encabezados: Mes, Cuota, Capital, Interés, Saldo
    ws.append(["Mes", "Cuota", "Capital", "Interés", "Saldo"])
    
    for idx, fila in enumerate(tabla, start=1):
        ws.append([
            idx,
            fila["cuota"],
            fila["abono"],   # Capital
            fila["interes"],
            fila["saldo"]
        ])
    
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer
