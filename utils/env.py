import os
import sys
from awsglue.utils import getResolvedOptions

def load_env(environment):
    if environment == "local":        
        from dotenv import load_dotenv
        load_dotenv(".env")
        
def get_env_or_args(env_name):
    try:
        if os.environ.get(env_name):
            return os.getenv(env_name)
        else:
            return getResolvedOptions(sys.argv,[env_name])[env_name]
    except:
        return ''