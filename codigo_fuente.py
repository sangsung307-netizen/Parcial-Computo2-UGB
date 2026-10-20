import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLabel

class InventarioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consultoria de Inventario - UGB")
        self.setGeometry(100, 100, 800, 600)

        # 1. Cargar datos con Pandas
        try:
            self.df = pd.read_csv("datos.csv")
        except FileNotFoundError:
            print("Error: No se encontró el archivo datos.csv")
            sys.exit()

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta de título
        titulo = QLabel("Análisis de Inventario por Sucursal")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(titulo)

        # 2. Inspección de datos con Pandas (Mostrado en consola gráfica)
        self.consola = QTextEdit()
        self.consola.setReadOnly(True)
        self.mostrar_estadisticas_pandas()
        layout.addWidget(self.consola)

        # 3. Gráfico de Matplotlib en PyQt5
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.generar_grafico()

        # Configurar widget central
        widget_central = QWidget()
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

    def mostrar_estadisticas_pandas(self):
        # Imprimir en la terminal (Requisito del punto 3)
        print("--- Información del DataFrame ---")
        self.df.info()
        print("\n--- Estadísticas Básicas ---")
        print(self.df.describe())

        # Mostrar en la interfaz
        info_texto = "--- Estructura y Tipos de Datos (Pandas) ---\n"
        info_texto += str(self.df.dtypes) + "\n\n"
        info_texto += "--- Estadísticas Básicas ---\n"
        info_texto += str(self.df.describe())
        self.consola.setText(info_texto)

    def generar_grafico(self):
        # Agrupar datos por sucursal y sumar la cantidad de productos
        productos_por_sucursal = self.df.groupby('Sucursal')['Cantidad'].sum()
        
        # Crear gráfico de barras
        productos_por_sucursal.plot(kind='bar', ax=self.ax, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
        self.ax.set_title('Total de Productos en Inventario por Sucursal')
        self.ax.set_ylabel('Cantidad Total')
        self.ax.set_xlabel('Sucursales')
        plt.xticks(rotation=0)
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = InventarioApp()
    ventana.show()
    sys.exit(app.exec_())