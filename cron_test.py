import os
from datetime import datetime as dt
from dotenv import load_dotenv

# Specify the file path and name
file_path = '/home/ec2-user/Documents/BRLOG/output.txt'
# Load local variable
load_dotenv()
var = os.environ['aws_secret_access_key']

 # Open the file in write mode
with open(file_path, 'w') as file:
    # Write the content to the file
    file.write(f'Test {var} succesfull at {dt.now()}')


print('File saved successfully.')
