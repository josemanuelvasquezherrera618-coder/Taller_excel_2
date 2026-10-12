import pandas as pd
import random 
from tabulate import tabulate 
from fpdf import FPDF

nombre_estudiante = "Jose Vásquez"
archivo_excel = "datos_ventas.xlsx"
archivo_pdf = "reporte_ejecutivo_ventas.pdf"

productos_disponibles = {
    "Laptop Gamer": 1200,
    "Mouse Óptico": 25,
    "Teclado Mecánico": 80,
    "Monitor 24'": 150,
    "Audífonos Bluetooth": 60,
    "Impresora Láser": 200
}

vendedores = ["Ana", "Carlos", "Beatriz", "David"]

datos = []
for i in range(1, 21):  # Generamos 20 ventas
    producto = random.choice(list(productos_disponibles.keys()))
    precio = productos_disponibles[producto]
    cantidad = random.randint(1, 5)
    vendedor = random.choice(vendedores)
    total = precio * cantidad
    datos.append([i, vendedor, producto, cantidad, precio, total])

columnas = ["ID", "Vendedor", "Producto", "Cantidad", "Precio Unit.", "Total"]
df = pd.DataFrame(datos, columns=columnas)

df.to_excel(archivo_excel, index=False)
print(f" Archivo {archivo_excel} generado con éxito.\n")

total_general = df["Total"].sum()
promedio_venta = df["Total"].mean()
vendedor_top = df.groupby("Vendedor")["Total"].sum().idxmax()
venta_top_valor = df.groupby("Vendedor")["Total"].sum().max()

print("--- RESUMEN DE VENTAS EN CONSOLA ---")
print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
print(f"\nTotal General de Ventas: ${total_general}")
print(f"Promedio por Venta: ${promedio_venta:.2f}")
print(f"Mejor Vendedor: {vendedor_top} con ${venta_top_valor}")

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", "B", 16)

pdf.cell(200, 10, txt="REPORTE EJECUTIVO DE VENTAS", ln=True, align='C')
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt=f"Estudiante: {nombre_estudiante}", ln=True, align='L')
pdf.ln(10)

pdf.ln(10)
pdf.set_font("Arial", "B", 12)
pdf.cell(200, 10, txt="Detalle de Operaciones:", ln=True)
pdf.set_font("Arial", size=10)

pdf.cell(30, 10, "Vendedor", 1)
pdf.cell(60, 10, "Producto", 1)
pdf.cell(30, 10, "Cantidad", 1)
pdf.cell(40, 10, "Total", 1, ln=True)

for index, row in df.iterrows():
    pdf.cell(30, 10, str(row["Vendedor"]), 1)
    pdf.cell(60, 10, str(row["Producto"]), 1)
    pdf.cell(30, 10, str(row["Cantidad"]), 1)
    pdf.cell(40, 10, f"${row['Total']}", 1, ln=True)

pdf.output(archivo_pdf)
print(f"\n Archivo {archivo_pdf} generado con éxito.")