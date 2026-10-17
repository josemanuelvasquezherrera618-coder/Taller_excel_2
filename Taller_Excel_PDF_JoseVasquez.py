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

def generar_datos():
    datos = []
    for i in range(1, 21):
        producto = random.choice(list(productos_disponibles.keys()))
        precio = productos_disponibles[producto]
        cantidad = random.randint(1, 5)
        vendedor = random.choice(vendedores)
        total = precio * cantidad
        datos.append([i, vendedor, producto, cantidad, precio, total])

    columnas = ["ID", "Vendedor", "Producto", "Cantidad", "Precio Unit.", "Total"]
    return pd.DataFrame(datos, columns=columnas)

def exportar_excel(df):
    df.to_excel(archivo_excel, index=False)
    print(f"\nArchivo {archivo_excel} generado con exito.")

def mostrar_resumen(df):
    total_general = df["Total"].sum()
    promedio_venta = df["Total"].mean()

    print("\n" + "="*30)
    print(" RESUMEN DE VENTAS EN CONSOLA ")
    print("="*30)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    print(f"\nTotal General de Ventas: ${total_general}")
    print(f"Promedio por Venta: ${promedio_venta:.2f}")
    print("="*30)

def ver_estadisticas_detalladas(df):
    print("\n" + "="*30)
    print("  ANALISIS DETALLADO")
    print("="*30)

    ventas_por_vendedor = df.groupby("Vendedor")["Total"].sum().reset_index()
    ventas_por_vendedor.columns = ["Vendedor", "Total Ventas"]
    mejor_vendedor_row = ventas_por_vendedor.loc[ventas_por_vendedor["Total Ventas"].idxmax()]

    productos_cant = df.groupby("Producto")["Cantidad"].sum().reset_index()
    productos_cant.columns = ["Producto", "Cantidad Total"]
    producto_mas_vendido_row = productos_cant.loc[productos_cant["Cantidad Total"].idxmax()]

    productos_ing = df.groupby("Producto")["Total"].sum().reset_index()
    productos_ing.columns = ["Producto", "Ingreso Total"]
    producto_mas_ingreso_row = productos_ing.loc[productos_ing["Ingreso Total"].idxmax()]

    tabla_mejor_vendedor = [[mejor_vendedor_row["Vendedor"], mejor_vendedor_row["Total Ventas"]]]
    tabla_prod_vendido = [[producto_mas_vendido_row["Producto"], producto_mas_vendido_row["Cantidad Total"]]]
    tabla_prod_ingreso = [[producto_mas_ingreso_row["Producto"], producto_mas_ingreso_row["Ingreso Total"]]]

    print("\nMejor Vendedor:")
    print(tabulate(tabla_mejor_vendedor, headers=["Vendedor", "Total"], tablefmt="grid"))

    print("\nProducto mas vendido (Cantidad):")
    print(tabulate(tabla_prod_vendido, headers=["Producto", "Cantidad"], tablefmt="grid"))

    print("\nProducto con mas ingresos:")
    print(tabulate(tabla_prod_ingreso, headers=["Producto", "Total"], tablefmt="grid"))
    print("="*30)

def exportar_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    pdf.cell(200, 10, txt="REPORTE EJECUTIVO DE VENTAS", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Estudiante: {nombre_estudiante}", ln=True, align='L')
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Detalle de Operaciones:", ln=True)
    pdf.set_font("Arial", size=10)

    pdf.cell(30, 10, "Vendedor", 1)
    pdf.cell(60, 10, "Producto", 1)
    pdf.cell(30, 10, "Cantidad", 1)
    pdf.cell(40, 10, "Total", 1, ln=True)

    for _, row in df.iterrows():
        pdf.cell(30, 10, str(row["Vendedor"]), 1)
        pdf.cell(60, 10, str(row["Producto"]), 1)
        pdf.cell(30, 10, str(row["Cantidad"]), 1)
        pdf.cell(40, 10, f"${row['Total']}", 1, ln=True)

    pdf.output(archivo_pdf)
    print(f"\nArchivo {archivo_pdf} generado con exito.")

def menu():
    df = None

    while True:
        print("\n" + "=" * 25)
        print("   SISTEMA DE VENTAS")
        print("=" * 25)
        print("1. Generar Datos de Ventas")
        print("2. Mostrar Tabla Resumen")
        print("3. Ver Estadisticas (Mejor Vendedor/Producto)")
        print("4. Exportar a Excel")
        print("5. Exportar a PDF")
        print("6. Generar Todo (Excel + PDF + Consola)")
        print("7. Salir")

        opcion = input("\nSeleccione una opcion (1-7): ")

        if opcion == "1":
            df = generar_datos()
            print("\nDatos generados exitosamente.")

        elif opcion == "2":
            if df is not None:
                mostrar_resumen(df)
            else:
                print("\nPrimero debe generar los datos (Opcion 1).")

        elif opcion == "3":
            if df is not None:
                ver_estadisticas_detalladas(df)
            else:
                print("\nPrimero debe generar los datos (Opcion 1).")

        elif opcion == "4":
            if df is not None:
                exportar_excel(df)
            else:
                print("\nPrimero debe generar los datos (Opcion 1).")

        elif opcion == "5":
            if df is not None:
                exportar_pdf(df)
            else:
                print("\nPrimero debe generar los datos (Opcion 1).")

        elif opcion == "6":
            if df is not None:
                exportar_excel(df)
                mostrar_resumen(df)
                ver_estadisticas_detalladas(df)
                exportar_pdf(df)
                print("\nProceso completo finalizado.")
            else:
                df = generar_datos()
                exportar_excel(df)
                mostrar_resumen(df)
                ver_estadisticas_detalladas(df)
                exportar_pdf(df)
                print("\nDatos generados y reportes creados.")

        elif opcion == "7":
            print("\nSaliendo del sistema.")
            break
        else:
            print("\nOpcion no valida, intente de nuevo.")

if __name__ == "__main__":
    menu()
