import boto3
import pandas as pd
from io import BytesIO

# Initialize a Boto3 session
# session = boto3.Session(
#     aws_access_key_id='AKIATCKAN534L6ME6UUB',
#     aws_secret_access_key='YOUR_SECRET_KEY',
#     region_name= 'us-east-2'
# )

# Create an S3 client
s3 = session.client('s3')

def s3_downloader(bucket_name, key):
    response = s3.get_object(Bucket=bucket_name, Key=key)
    return pd.read_csv(BytesIO(response['Body'].read()))

def s3_downloade(bucket_name, key, dataframe):
    csv_buffer = BytesIO()
    s3_downloader.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=key, Body=csv_buffer.getvalue())

def transform_data(s3_uploader):
    # Example transformation: filtering and aggregating
    s3_uploader[' kwh_consumption'] = s3_uploader['kwh_consumption'] * 2
    transformed_df = s3.groupby('kwh_consumption').sum().reset_index()
    return transformed_df

def main():
    bucket_name = 'tkh-nyc-energy'
    input_key = '../data/processed/energy_clean.csv'
    output_key = '../data/raw/Electric_Consumption_And_Cost__2010_-_Feb_2023__20240417.csv'

    # Read the CSV file from S3
    df = s3_downloader(bucket_name, input_key)

    # Apply data transformations
    transformed_df = transform_data(df)

    # Write the transformed data back to S3
    s3_downloader(bucket_name, output_key, transformed_df)

if __name__ == '__main__':
    main()