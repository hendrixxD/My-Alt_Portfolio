from dotenv import load_dotenv
import os

load_dotenv()

"""
fetches environment varibale
"""
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable {var_name} not set.")
    return value