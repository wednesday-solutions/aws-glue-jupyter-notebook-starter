#!/usr/bin/env python
# coding: utf-8

# In[8]:


import os
import pandas as pd
import boto3
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext


# In[9]:


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
        database_name = crawler_metadata['Crawler']['DatabaseName']
        table_name = crawler_metadata['Crawler']['Tables']

        # Read data from Glue Data Catalog
        dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
            database=database_name,
            table_name=table_name
        )

        # Convert to a Spark DataFrame (or Pandas DataFrame if needed)
        data = dynamic_frame.toDF()

    return data


# In[10]:


# Example usage:
environment = os.getenv("ENVIRONMENT", "local")
local_file_path = "./../../../data/raw/sample.csv"
crawler_name = "your-crawler-name"

data = read_data(environment, local_file_path, crawler_name)
print(data)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




