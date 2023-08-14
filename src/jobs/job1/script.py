#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

# In[2]:


sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)


# In[3]:


def load_env(environment):
    if environment == "local":        
        from dotenv import load_dotenv
        load_dotenv(".env")

# In[4]:


RELATIVE_PATH_PREFIX="./../../.."

# In[5]:


def getEnvOrArgs(env_name):
    try:
        if os.environ.get(env_name):
            return os.getenv(env_name)
        else:
            return getResolvedOptions(sys.argv,[env_name])[env_name]
    except:
        return ''
    

# In[6]:


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

# In[7]:


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
        tables = [table['Name'] for table in response['TableList']]
        table_name = tables[0]
        # Read data from Glue Data Catalog
        dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
            database=database_name,
            table_name=table_name
        )

        # Convert to a Spark DataFrame (or Pandas DataFrame if needed)
        data = dynamic_frame.toDF()

    return data

# In[8]:


def getEnvOrArgs(env_name):
    if os.environ.get(env_name):
        return os.getenv(env_name)
    else:
        return getResolvedOptions(sys.argv,[env_name])[env_name]
    

# In[9]:


environment = getEnvOrArgs("ENVIRONMENT_NAME")
load_env(environment)
local_file_path = f"{RELATIVE_PATH_PREFIX}/data/raw/sample.csv"
crawler_name = getEnvOrArgs("SOURCE_CRAWLER")
data = read_data(getEnvOrArgs("ENVIRONMENT_NAME"), local_file_path, crawler_name)

# In[10]:


print(data.show())

target_bucket = getEnvOrArgs("BUCKET_NAME")

target_directory = f"{RELATIVE_PATH_PREFIX if environment == 'local' else target_bucket}/landing/{getEnvOrArgs('JOB_NAME')}"
data = transform_and_write_data(data, target_bucket, target_directory, environment)

print(data.show())
job.commit()

# In[ ]:




# In[ ]:



