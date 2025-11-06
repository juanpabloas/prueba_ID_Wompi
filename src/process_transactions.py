import json
import pandas as pd

def generar_vista_aggregada(ruta_json: str, ruta_parquet: str) -> None:
    """
    Lee un archivo JSONL con transacciones, procesa los datos y genera una vista
    agregada por BIN y fecha de transacción. El resultado se guarda en formato Parquet.
    """

    registros = []

    # Leer archivo JSONL línea por línea
    with open(ruta_json, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            registro = json.loads(linea)
            registros.append({
                "id": registro.get("id"),
                "created_at": registro.get("created_at"),
                "updated_at": registro.get("updated_at"),
                "status": registro.get("status"),
                "amount_in_cents": registro.get("amount_in_cents"),
                "payment_type": registro.get("payment_method_type", {}).get("type"),
                "installments": registro.get("payment_method_type", {}).get("installments"),
                "bin": registro.get("payment_method_type", {}).get("extra", {}).get("bin"),
                "card_holder": registro.get("payment_method_type", {}).get("extra", {}).get("card_holder"),
                "is_three_ds": registro.get("payment_method_type", {}).get("extra", {}).get("is_three_ds"),
                "unique_code": registro.get("payment_method_type", {}).get("extra", {}).get("unique_code"),
                "three_ds_auth_type": registro.get("payment_method_type", {}).get("extra", {}).get("three_ds_auth_type"),
                "external_identifier": registro.get("payment_method_type", {}).get("extra", {}).get("external_identifier"),
                "processor_response_code": registro.get("payment_method_type", {}).get("extra", {}).get("processor_response_code"),
                "authorizer_transaction_id": registro.get("payment_method_type", {}).get("extra", {}).get("authorizer_transaction_id")
            })

    # Convertir a DataFrame
    df = pd.DataFrame(registros)
    df["fecha"] = pd.to_datetime(df["created_at"]).dt.date

    # Filtrar transacciones aprobadas
    df_aprobadas = df[df["status"] == "APPROVED"]

    # Generar vista agregada
    vista_agregada = (
        df_aprobadas
        .groupby(["bin", "fecha"], as_index=False)
        .agg(
            cantidad_transacciones=("id", "count"),
            monto_total_aprobado=("amount_in_cents", "sum")
        )
    )

    # Guardar en Parquet
    vista_agregada.to_parquet(ruta_parquet, index=False)
    print(f"✅ Vista agregada guardada en: {ruta_parquet}")


if __name__ == "__main__":
    ruta_json = "../data/transactions_50k.jsonl"
    ruta_parquet = "../data/summary_transactions_50k.parquet"
    generar_vista_aggregada(ruta_json, ruta_parquet)