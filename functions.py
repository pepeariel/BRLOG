import boto3
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime as dt

class FileHandler:
    
    '''' This class is able to conect to aws bucket read files and send new ones '''
    def __init__(self):
        
        self.aws_access_key_id = os.getenv('aws_access_key_id')
        self.aws_secret_access_key = os.getenv('aws_secret_access_key')
        self.bucket_name = os.getenv('bucket_name')
        self.s3_region = os.getenv('s3_region')
        self.excel_file_path = r'/Users/pedroariel/Downloads/Relatório de entregas.xlsx' # Path to BRlog file
        self.parquet_file_path = f'relatorio_entregas{dt.now()}.parquet' 

    def create_s3_connection(self):
        # Connect to a s3 bucket
        s3 = boto3.resource(
        's3',
        aws_access_key_id = self.aws_access_key_id,
        aws_secret_access_key = self.aws_secret_access_key,
        region_name = self.s3_region)
        return s3
        
    def list_s3_files(self, s3):
        # Retrieve all the files from a s3 bucket and save it in a response variable
        responses = s3.Bucket(self.bucket_name).objects.all()
        print(responses)
        return responses

    # function to send file to s3 bucket
    def send_file_to_s3(self, s3):
        with open(self.parquet_file_path, 'rb') as f:
            s3.Bucket(self.bucket_name).upload_file(Filename=self.parquet_file_path, Key=self.parquet_file_path)
            # Remove parquet file from this folder
            os.remove(self.parquet_file_path)
            print('Arquivo carregado no bucket com sucesso!')    

    # Save the file in parquet format
    def excel_to_parquet(self):
        try:
            # Read Excel file using pandas use 2nd row as header
            df = pd.read_excel(self.excel_file_path, header=1)

            # Replace spaces with underscores in the header
            df.columns = df.columns.str.replace(' ', '_')

            # Convert columns to string
            for column in df.columns:
                df[column] = df[column].astype('string') 

            # Save DataFrame as Parquet file
            df.to_parquet(self.parquet_file_path)

            # Delete the temporary Excel file and parquet file
            os.remove(self.excel_file_path)
            
            return print('Arquivo parquet salvo com sucesso!')
        
        except Exception as e:
            print('Erro devido a:', e)

    
