import os
import json
import csv
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import asdict

class FileUtils:
    """Clase con métodos estáticos para guardar archivos de salida."""
    
    def _save_to_json(data: List[dict], filename: str):
    
       # Si es DataFrame, convertirlo
        if isinstance(data, pd.DataFrame):
            data = data.reset_index().to_dict(orient="records")
    
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
          
    def _save_to_csv(data: List[dict], filename: str):
        if not data:
            print("No hay datos para guardar.")
            return
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
    def _ensure_folder_exists(folder_name: str):
        os.makedirs(folder_name, exist_ok=True)
    
    def save_output(data: List[Dict[str, Any]], symbol: str, source: str, format: str, folder: str):
       #folder = f"{source}_original".lower()
    
        FileUtils._ensure_folder_exists(folder)
    
        filename = f"{symbol}_{source}_{datetime.now().strftime('%Y%m%d')}.{format}"
    
        filepath = os.path.join(folder, filename)
    
        if format == "json":
            FileUtils._save_to_json(data, filepath)
        elif format == "csv":
            FileUtils._save_to_csv(data, filepath)
        else:
            print(f"Formato no soportado: {format}")