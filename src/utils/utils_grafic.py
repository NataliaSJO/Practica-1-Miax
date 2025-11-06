import matplotlib.pyplot as plt

class UtilsGrafic:
    """Clase con métodos estáticos para generar gráficas."""
    
    def plot_averages(averages: dict, filename: str = "average.png"):
        """Genera un gráfico de barras con las medias por símbolo.
            - averages: diccionario {symbol: media}
            - filename: nombre del archivo de imagen a guardar."""

        symbols = list(averages.keys())
        values = list(averages.values())

        plt.figure(figsize=(10, 6))
        plt.bar(symbols, values, color='skyblue')
        plt.title("Media de precios ajustados por símbolo")
        plt.xlabel("Símbolo")
        plt.ylabel("Media")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()


    def plot_standard_deviations(deviations: dict, filename: str = "standard_deviations.png"):
        """Genera un gráfico de barras con las desviaciones estándar por símbolo.
            - deviations: diccionario {symbol: desviación}
            - filename: nombre del archivo de imagen a guardar."""
        symbols = list(deviations.keys())
        values = list(deviations.values())

        plt.figure(figsize=(10, 6))
        plt.bar(symbols, values, color='salmon')
        plt.title("Desviación típica de precios ajustados por símbolo")
        plt.xlabel("Símbolo")
        plt.ylabel("Desviación típica")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
