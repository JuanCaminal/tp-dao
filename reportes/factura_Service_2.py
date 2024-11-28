from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm

def generar_factura(
    facturar_a,
    numero_factura,
    fecha,
    fecha_vencimiento,
    items,
    subtotal,
    iva,
    total,
):
    # Definir valores fijos
    nombre_archivo = "factura_A.pdf"
    logo_path = r"C:\Users\fabricio_alanie\Documents\GitHub\tp-dao\recursos\foto_logo.jpg"
    hotel_nombre = "Hotel Royal."
    hotel_direccion = "Nueva Cordoba 38<br/>5000 Cordoba, Argentina"

    # Crear documento PDF
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']

    # Logo en la parte superior derecha
    try:
        logo = Image(logo_path, width=3 * cm, height=3 * cm)
        logo.hAlign = 'RIGHT'
        elements.append(logo)
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

    # Título "Factura A" centrado
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>Factura A</b>", title_style))
    elements.append(Spacer(1, 24))

    # Información del encabezado de la factura
    header_data = [
        [Paragraph(f"{hotel_nombre}<br/>{hotel_direccion}", normal_style),
         Paragraph(f"<b>FACTURAR A:</b><br/>{facturar_a}", normal_style)]
    ]
    header_table = Table(header_data, colWidths=[10 * cm, 8 * cm])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 12))

    # Información adicional
    info_data = f"""
    <b>N° DE FACTURA:</b> {numero_factura}<br/>
    <b>FECHA:</b> {fecha}<br/>
    <b>FECHA VENCIMIENTO:</b> {fecha_vencimiento}<br/>
    """
    elements.append(Paragraph(info_data, normal_style))
    elements.append(Spacer(1, 12))

    # Tabla de artículos
    table_data = [["NRO", "DESCRIPCIÓN", "PRECIO UNITARIO", "IMPORTE"]] + items
    table = Table(table_data, colWidths=[1.5 * cm, 8 * cm, 4 * cm, 4 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    elements.append(table)

    # Totales
    totals = [
        ["", "Subtotal", f"${subtotal:.2f}"],
        ["", "IVA 21%", f"${iva:.2f}"],
        ["", "TOTAL", f"${total:.2f}"]
    ]
    totals_table = Table(totals, colWidths=[12.5 * cm, 4 * cm, 4 * cm])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (1, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (1, -1), (-1, -1), 1, colors.black),
    ]))
    elements.append(totals_table)

    # Generar el PDF
    doc.build(elements)
    print(f"Factura generada: {nombre_archivo}")



