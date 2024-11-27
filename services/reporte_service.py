import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle

from services.habitacion_service import HabitacionService


class ReporteService:
    def __init__(self, db):
        self.db = db
        self.habitacion_service = HabitacionService(db)
        self.habitaciones = self.habitacion_service.get_all()

    def procesar_habitaciones(self):
        """Clasifica habitaciones según su tipo y estado."""
        ocupacion_por_tipo = {
            'simple': {'ocupadas': 0, 'disponibles': 0},
            'doble': {'ocupadas': 0, 'disponibles': 0},
            'suite': {'ocupadas': 0, 'disponibles': 0}
        }

        for habitacion in self.habitaciones:
            tipo = habitacion.tipo.lower()
            estado = habitacion.estado.lower()
            if tipo in ocupacion_por_tipo:
                if estado == "ocupada":
                    ocupacion_por_tipo[tipo]['ocupadas'] += 1
                elif estado == "disponible":
                    ocupacion_por_tipo[tipo]['disponibles'] += 1

        print("Datos procesados:", ocupacion_por_tipo)
        return ocupacion_por_tipo

    def generar_reporte_ocupacion_promedio(self):
        """Genera un PDF con un gráfico de ocupación promedio de habitaciones."""
        doc = SimpleDocTemplate("reporte_ocupacion_promedio.pdf", pagesize=letter)
        elements = []

        estilo_titulo = ParagraphStyle(
            name="Titulo",
            fontSize=18,
            leading=22,
            alignment=1,
            spaceAfter=20
        )
        estilo_subtitulo = ParagraphStyle(
            name="Subtitulo",
            fontSize=14,
            leading=18,
            spaceAfter=12
        )

        elements.append(Paragraph("Informe de Ocupación Promedio", estilo_titulo))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Distribución de ocupación por tipo de habitación", estilo_subtitulo))
        elements.append(Spacer(1, 12))

        ocupacion_por_tipo = self.procesar_habitaciones()

        # Preparar datos para el gráfico de torta
        tipos = ['Simple', 'Doble', 'Suite']
        ocupadas = [
            ocupacion_por_tipo['simple']['ocupadas'],
            ocupacion_por_tipo['doble']['disponibles'],
            ocupacion_por_tipo['suite']['ocupadas']
        ]

        total_ocupadas = sum(ocupadas)

        # Verificar si hay datos válidos para graficar
        if total_ocupadas > 0:
            # Asignar un tamaño mínimo a los sectores para evitar que se superpongan
            ocupadas_ajustadas = [x if x > 0 else 0.01 for x in ocupadas]

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(ocupadas_ajustadas, labels=tipos, autopct='%1.1f%%', startangle=90)

            # Ajustar el título con más espacio
            ax.set_title("Habitaciones Ocupadas por Tipo", pad=20)  # Aumentar el valor de 'pad' para más espacio
            ax.axis('equal')

            # Guardar el gráfico en un buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            elements.append(Image(buffer, width=400, height=300))

        else:
            elements.append(
                Paragraph("No hay datos suficientes para generar un gráfico de ocupación.", estilo_subtitulo)
            )

        elements.append(Spacer(1, 12))

        # Agregar información adicional sobre habitaciones disponibles
        elements.append(Paragraph("Habitaciones Ocupadas por Tipo", estilo_subtitulo))
        for tipo, cantidad in zip(tipos, ocupadas):
            elements.append(Paragraph(f"{tipo}: {cantidad} ocupadas", estilo_subtitulo))
            elements.append(Spacer(1, 8))

        doc.build(elements)
        print("Reporte generado: reporte_ocupacion_promedio.pdf")

    def generar_reporte_ingresos_por_habitaciones(self):
        pass
