from collections import Counter
from io import BytesIO
from matplotlib import pyplot as plt
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, SimpleDocTemplate, Table, \
    TableStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter




def generar_reporte_ocupacion_promedio(self, tipo, estado):
    # Configuración básica del documento
    doc = BaseDocTemplate("ocupacion_promedio.pdf", pagesize=letter)
    frame = Frame(0.5 * inch, 0.5 * inch, 7.5 * inch, 10 * inch, id='normal')
    template = PageTemplate(id='test', frames=[frame])
    doc.addPageTemplates([template])
    elements = []

    # Estilos
    estilo_titulo = ParagraphStyle(
        name="Titulo",
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=22,
        alignment=1,  # Centrado
        spaceAfter=20
    )
    estilo_subtitulo = ParagraphStyle(
        name="Subtitulo",
        fontSize=14,
        leading=18,
        spaceAfter=12
    )
    estilo_normal = ParagraphStyle(name="Normal", fontSize=10, leading=12)

    # Logo y encabezado en la parte superior izquierda
    logo_img = Image(r"C:\Users\fabricio_alanie\Documents\GitHub\tp-dao\recursos\foto_logo.jpg", width=70, height=70)
    header_data = [
        [
            logo_img,
            Paragraph("Hotel Royal.<br/>Nueva Cordoba 38<br/>5000 Cordoba, Argentina", estilo_normal)
        ]
    ]
    header_table = Table(header_data, colWidths=[1.5 * inch, 5.5 * inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ]))
    elements.append(header_table)

    elements.append(Spacer(1, 20))  # Espaciador

    # Título principal
    elements.append(Paragraph("Informe de Ocupación Promedio", estilo_titulo))
    elements.append(Spacer(1, 12))
    tipo = [tipo]
    estado = [estado]
    # Procesar ocupación promedio
    ocupacion_por_tipo = Counter()
    for t, e in zip(tipo, estado):
        if e.lower() == "ocupada":
            ocupacion_por_tipo[t] += 1

    tipos = ['Simple', 'Doble', 'Suite', 'Salon']
    ocupadas = [ocupacion_por_tipo.get(t, 0) for t in tipos]
    total_ocupadas = sum(ocupadas)

    # Verificar si hay datos para el gráfico
    if total_ocupadas > 0:
        ocupadas_ajustadas = [x if x > 0 else 0.01 for x in ocupadas]

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(ocupadas_ajustadas, labels=tipos, autopct='%1.1f%%', startangle=90)
        ax.set_title("Habitaciones Ocupadas por Tipo", pad=20)
        ax.axis('equal')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        elements.append(Image(buffer, width=400, height=300))
    else:
        elements.append(
            Paragraph("No hay datos suficientes para generar un gráfico de ocupación.", estilo_subtitulo)
        )

    elements.append(Spacer(1, 20))  # Espaciador

    # Información adicional sobre ocupación como tabla
    ocupacion_data = [['Tipo de Habitación', 'Habitaciones Ocupadas']]
    for t, o in zip(tipos, ocupadas):
        ocupacion_data.append([t, f"{o} ocupadas"])

    ocupacion_table = Table(ocupacion_data, colWidths=[3 * inch, 3 * inch])
    ocupacion_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado con fondo gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco en encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para encabezado
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior en encabezado
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordes de la tabla
    ]))

    elements.append(ocupacion_table)

    elements.append(Spacer(1, 20))  # Espaciador

    # Logo inferior izquierdo
    logo_utn = Image(r"C:\Users\fabricio_alanie\Documents\GitHub\tp-dao\recursos\UTN_logo.ico", width=70, height=70)
    footer_table = Table([[logo_utn]], colWidths=[1.5 * inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ]))
    elements.append(Spacer(1, 10))  # Ajustar espacio
    elements.append(footer_table)

    # Generar PDF
    doc.build(elements)
    print("Reporte generado: ocupacion_promedio.pdf")