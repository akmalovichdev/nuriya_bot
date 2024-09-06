import os
from dotenv import load_dotenv

load_dotenv()

botTOKEN = os.getenv("botTOKEN")
mysqlHost = os.getenv("mysqlHost")
mysqlUser = os.getenv("mysqlUser")
mysqlPassword = os.getenv("mysqlPassword")
mysqlDB = os.getenv("mysqlDB")