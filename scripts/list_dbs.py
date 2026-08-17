import os

env_file = r"C:\Users\91877\chronograph\.env"
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip("\"'")

from hydra_db import HydraDB
client = HydraDB(token=os.environ["HYDRA_DB_API_KEY"])
dbs = client.databases.list()
print("Databases:", getattr(dbs.data, "databases", dbs.data))
