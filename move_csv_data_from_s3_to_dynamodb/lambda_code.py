import json
import boto3
import csv

def lambda_handler(event, context):
  bucket_name = 'gb1212'
  file_name = "Project1.csv"
  s3 = boto3.client('s3')
  csv_obj = s3.get_object(Bucket=bucket_name, Key=file_name)
  csv_obj_data = csv_obj['Body'].read().decode('utf-8').splitlines()
  
  data = {}
  csvReader = csv.DictReader(csv_obj_data)
  for rows in csvReader:

    key = rows['id']
    data[key] = rows

# Convert dict to list
  dictlist = []
  for __, value in data.items():
    dictlist.append(value)
  dynamodb_client = boto3.client('dynamodb')
  for val in dictlist:
    temp_dic = {
        "id": {'N': f"{val['id']}"},
        "first_name": {'S': f"{val['first_name']}"},
        "last_name": {'S': f"{val['last_name']}"},
        "email": {'S': f"{val['email']}"},
        "gender": {'S': f"{val['gender']}"},
        "ip_address": {'S': f"{val['ip_address']}"}
    }
    
    dynamodb_client.put_item(TableName="promax", Item=temp_dic)


