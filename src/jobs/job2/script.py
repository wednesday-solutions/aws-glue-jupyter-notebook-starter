#!/usr/bin/env python
# coding: utf-8

# In[38]:


import os
import pandas as pd
import boto3
import sys
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql import functions as F
from pyspark.sql.functions import col, lit, current_date, year

# In[39]:


sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)


# In[ ]:


def load_env(environment):
    if environment == "local":        
        from dotenv import load_dotenv
        load_dotenv(".env")

# In[40]:


RELATIVE_PATH_PREFIX="./../../.."

# In[41]:


def calculate_age(data_frame):
    # Calculating the current year using the current date
    current_year = year(current_date())

    # Calculating the age by subtracting the year_of_birth from the current year
    age_column = current_year - col("year_of_birth")

    # Adding the calculated age as a new column to the DataFrame
    data_frame_with_age = data_frame.withColumn("age", age_column)

    return data_frame_with_age

# In[42]:


def transform_and_write_data(data_frame, target_bucket, target_directory, environment):
    # Converting all column names to lower snake_case
    for col_name in data_frame.columns:
        snake_case_name = col_name.lower().replace(" ", "_")
        data_frame = data_frame.withColumnRenamed(col_name, snake_case_name)

    # Computing full_name by concatenating first_name and last_name
    data_frame = data_frame.withColumn("full_name", F.concat_ws(" ", data_frame["first_name"], data_frame["last_name"]))

    # Determine the output path based on the environment
    if environment == 'local':

        output_path = os.path.join(target_directory, 'output.csv')
        print(output_path)
        data_frame.write.csv(output_path, mode='overwrite', header=True)
    else:
        output_path = f"s3://{target_bucket}/{target_directory}"
        data_frame.write.csv(output_path, mode='overwrite', header=True)
    return data_frame

# In[43]:


def read_data(environment, local_file_path, crawler_name):
    if environment == "local":
        # Read data from local file (e.g., using Pandas)
        data = spark.read.csv(local_file_path, header=True)
    else:
        # Create or retrieve a Spark context
        sc = SparkContext.getOrCreate()
        glueContext = GlueContext(sc)
        glue_client = boto3.client('glue')

        # Get the crawler metadata
        crawler_metadata = glue_client.get_crawler(Name=crawler_name)

        # keys = list(crawler_metadata['Crawler'].keys())

        database_name = crawler_metadata['Crawler']['DatabaseName']
        prefix = crawler_metadata['Crawler']['Targets']['S3Targets'][0]['Path'] if 'S3Targets' in crawler_metadata['Crawler']['Targets'] else None

        # Get table names from the Glue Data Catalog using the database and prefix
        response = glue_client.get_tables(DatabaseName=database_name)
        # error_message = f"The keys are: {response['TableList']}, {prefix}"
        # raise Exception(error_message)
        tables = [table['Name'] for table in response['TableList']]

        # Assuming the first table name matches the prefix, use it for reading data
        table_name = tables[0]
        print("crawler_metadata")



        # Read data from Glue Data Catalog
        dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
            database=database_name,
            table_name=table_name
        )

        # Convert to a Spark DataFrame (or Pandas DataFrame if needed)
        data = dynamic_frame.toDF()

    return data

# In[44]:


environment = os.getenv("ENVIRONMENT", "local")
local_file_path = f"{RELATIVE_PATH_PREFIX}/data/raw/sample.csv"
crawler_name = os.getenv("SOURCE_CRAWLER")
data = read_data(environment, local_file_path, crawler_name)

# In[45]:


print(data.show())

target_bucket = os.getenv("BUCKET_NAME", "default")
target_directory = f"{RELATIVE_PATH_PREFIX}/landing/{os.getenv('JOB_NAME')}"
transformed_data = transform_and_write_data(data, target_bucket, target_directory, environment)

final_data_with_age = calculate_age(transformed_data)
print(final_data_with_age.show())
job.commit()

# In[ ]:




# In[ ]:



