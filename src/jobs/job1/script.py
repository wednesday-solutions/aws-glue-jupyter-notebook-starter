#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import pandas as pd
import boto3
import sys
from dotenv import load_dotenv
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions


# In[ ]:





# In[ ]:


sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
load_dotenv(".env")


# In[ ]:


def read_data(environment, local_file_path, crawler_name):
    if environment == "local":
        # Read data from local file (e.g., using Pandas)
        data = pd.read_csv(local_file_path)
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


# In[ ]:


environment = os.getenv("ENVIRONMENT", "local")
local_file_path = "./../../../data/raw/sample.csv"
crawler_name = os.GetEnv("SOURCE_CRAWLER")

data = read_data(environment, local_file_path, crawler_name)


# In[ ]:


print(data.show())
job.commit()


# In[ ]:


env_vars = os.environ

for key, value in env_vars.items():
    print(f'{key}: {value}')
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




