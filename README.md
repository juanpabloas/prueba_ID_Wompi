# prueba_ID_Wompi

## 🚀 Objetivo

Construir un script en Python que:

- Lea un archivo de transacciones (transactions_50k.jsonl).
- Procese los registros para obtener una vista agregada.
- Genere un resumen con los siguientes campos:

| Campo              | Descripción                                                    |
| ------------------ | -------------------------------------------------------------- |
| `bin`              | Bank Identification Number (primeros 6 dígitos de la tarjeta). |
| `transaction_date` | Fecha de la transacción (día).                                 |
| `approved_count`   | Cantidad de transacciones aprobadas.                           |
| `approved_amount`  | Suma total aprobada.                                           |

- Guarde la salida en un archivo Parquet (summary.parquet).


## 📁 Estructura del Proyecto
```
transaction-summary/
├── src/
│   └── process_transactions.py
├── data/
│   ├── transactions_50k.jsonl
│   └── summary_transactions_50k.parquet
├── requirements.txt
└── README.md
```

## ⚙️ Requisitos

- Python 3.9 o superior
- Librerías indicadas en requirements.txt

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

- Desde la raíz del proyecto, ejecutar:

```bash
python src/process_transactions.py --input ./data/transactions_50k.jsonl --output ./data/summary.parquet
```

## Parámetros

- --input: Ruta del archivo de entrada .jsonl.
- --output: Ruta del archivo de salida .parquet.


```bash
python src/process_transactions.py --input data/transactions_50k.jsonl --output data/summary.parquet
```

## 🧠 Supuestos y consideraciones

- El archivo de entrada contiene un registro JSON por línea.

- Cada registro incluye, al menos, los campos:
    - bin
    - date
    - status
    - amount
  
- Solo se consideran transacciones aprobadas (status == "APPROVED").
- La agregación se realiza por día (YYYY-MM-DD) y BIN.
- El script es idempotente: al ejecutarse varias veces sobre los mismos datos produce el mismo resultado.
- Si el archivo de salida ya existe, será reemplazado.