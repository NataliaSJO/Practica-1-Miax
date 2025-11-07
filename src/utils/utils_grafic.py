import matplotlib.pyplot as plt

class UtilsGrafic:
    """Clase con métodos estáticos para generar gráficas."""
    
    def plot_averages(averages: dict, filename: str = "plot_average.png", annotate: bool = True):
        """Genera un gráfico de barras con las medias por símbolo.
            - averages: diccionario {symbol: media}
            - filename: nombre del archivo de imagen a guardar."""

        symbols = list(averages.keys())
        values = list(averages.values())

        plt.figure(figsize=(10, 6))
        bars = plt.bar(symbols, values, color=plt.cm.tab20.colors[: len(values)])
        plt.title("Media de precios ajustados por símbolo")
        plt.xlabel("Símbolo")
        plt.ylabel("Media")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        if annotate:
            for bar, v in zip(bars, values):
                height = bar.get_height()
                plt.annotate(f"{v:.2f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()


    def plot_standard_deviations(deviations: dict, filename: str = "plot_standard_deviations.png", annotate: bool = True):
        """Genera un gráfico de barras con las desviaciones estándar por símbolo.
            - deviations: diccionario {symbol: desviación}
            - filename: nombre del archivo de imagen a guardar."""
        symbols = list(deviations.keys())
        values = list(deviations.values())

        plt.figure(figsize=(10, 6))
        bars = plt.bar(symbols, values, color=plt.cm.tab20.colors[: len(values)])
        plt.title("Desviación típica de precios ajustados por símbolo")
        plt.xlabel("Símbolo")
        plt.ylabel("Desviación típica")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        if annotate:
            for bar, v in zip(bars, values):
                height = bar.get_height()
                plt.annotate(f"{v:.2f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()


    def plot_weights(weights, symbols: list = None, filename: str = "plot_weights.png", annotate: bool = True):
        """Genera un gráfico de barras para los pesos de un portfolio y lo guarda en archivo.

        Parámetros:
            - weights: dict {symbol: weight}, lista/tupla de valores numéricos
            - symbols: lista de etiquetas (si `weights` es lista/tupla)
            - filename: nombre del archivo a guardar
            - title: título del gráfico
            - annotate: si True anota cada barra con el porcentaje correspondiente

        Comportamiento:
            - Si se pasa un diccionario, las claves se usan como etiquetas.
            - Si se pasa una lista, se requieren `symbols` o se usarán índices como etiquetas.
            - Si la suma de pesos es 0, se mostrará 0% en las anotaciones para evitar división por cero.
        """

        # Normalizar entrada y etiquetas
        if isinstance(weights, dict):
            symbols = list(weights.keys())
            values = list(weights.values())
        else:
            # acepta listas o tuplas
            try:
                values = list(weights)
            except Exception:
                raise TypeError("weights debe ser un dict o una lista/tupla de números")

            if symbols is None:
                symbols = [str(i) for i in range(len(values))]
            if len(symbols) != len(values):
                raise ValueError("La longitud de 'symbols' debe coincidir con la de 'weights'")

        if len(values) == 0:
            raise ValueError("No hay datos en 'weights' para graficar")

        total = sum(values) if sum(values) is not None else 0

        # Preparar porcentajes (evitar división por cero)
        if total == 0:
            percentage = [0 for _ in values]
        else:
            percentage = [(v / total) * 100 for v in values]

        # Plot
        plt.figure(figsize=(10, 6))
        bars = plt.bar(symbols, values, color=plt.cm.tab20.colors[: len(values)])
        plt.title("Pesos de la Cartera")
        plt.xlabel("Símbolo")
        plt.ylabel("Peso")
        plt.grid(axis="y", linestyle="--", alpha=0.6)

        # Anotar con porcentajes encima de cada barra
        if annotate:
            for bar, p in zip(bars, percentage):
                height = bar.get_height()
                plt.annotate(f"{p:.2f}%", xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9)

        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
