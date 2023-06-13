from functions import FileHandler
from dotenv import load_dotenv
import os
import pandas as pd

# Save some random file from excel to parquet format
excel_file_path = r'/Users/pedroariel/Downloads/relatorio_entregas_historico.xlsx'
parquet_file_path = r'/Users/pedroariel/Downloads/relatorio_entregas_historico.parquet'

#excel_to_parquet(excel_file_path, parquet_file_path)

# Load local variables
load_dotenv()

Pipeline = FileHandler()

s3 = Pipeline.create_s3_connection()

files = Pipeline.list_s3_files(s3)



