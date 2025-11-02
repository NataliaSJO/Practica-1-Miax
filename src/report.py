from typing import List
from datetime import date
import pandas as pd

class DailyPrice:
    def __init__(self, date: date, open: float, high: float, low: float, close: float, adj_close: float, volume: int):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.adj_close = adj_close
        self.volume = volume

class Portfolio:
    def __init__(self, prices: List[DailyPrice]):
        self.prices = prices
        print(prices)

    def report(self, data, include_warnings: bool = True, markdown: bool = True) -> str:
        lines = []

        print(data)
        print("REPORT GENERATED")
        # Encabezado
        lines.append("# Informe de Serie de Precios\n")
        lines.append(f"Total de tickers: **{len(self.prices)}**\n")

        #Convertir a DataFrame
        df = pd.DataFrame([{
            "Fecha": p.date,
            "Apertura": p.open,
            "Máximo": p.high,
            "Mínimo": p.low,
            "Cierre": p.close,
            "Cierre Ajustado": p.adj_close,
            "Volumen": p.volume,
            "Variación (%)": ((p.close - p.open) / p.open * 100) if p.open else None
        } for p in self.prices])

        df.sort_values("Fecha", inplace=True)
        df.reset_index(drop=True, inplace=True)

      #  # Rentabilidad total
      #  try:
      #      total_return = ((df["Cierre"].iloc[-1] - df["Apertura"].iloc[0]) / df["Apertura"].iloc[0]) * 100
      #  except Exception:
      #      total_return = None
#
      #  lines.append("## 📊 Evolución de Precios\n")
      #  lines.append(df[["Fecha", "Apertura", "Cierre", "Variación (%)", "Volumen"]].to_markdown(index=False))
#
      #  lines.append("\n## 💰 Rentabilidad Total\n")
      #  if total_return is not None:
      #      lines.append(f"**Rentabilidad desde el primer día hasta el último:** {total_return:.2f}%\n")
      #  else:
      #      lines.append("**Rentabilidad total:** No disponible (faltan datos)\n")

        # Advertencias
      #  if include_warnings:
      #      lines.append("\n## ⚠️ Advertencias\n")
      #      if df.isnull().any().any():
      #          lines.append("- Hay registros con valores nulos.\n")
      #      if (df["Volumen"] < 1000).any():
      #          fechas = df[df["Volumen"] < 1000]["Fecha"].dt.strftime("%Y-%m-%d").tolist()
      #          lines.append(f"- Volumen bajo en: {', '.join(fechas)}\n")
      #      if (df["Variación (%)"].abs() > 10).any():
      #          fechas = df[df["Variación (%)"].abs() > 10]["Fecha"].dt.strftime("%Y-%m-%d").tolist()
      #          lines.append(f"- Variaciones diarias superiores al 10% en: {', '.join(fechas)}\n")
#
        return "\n".join(lines)