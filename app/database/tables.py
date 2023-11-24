#Permet de créer un objet qui sera importé dans le main
from database.setup_db import BaseSQL
from sqlalchemy.util._collections import Properties

LogType = BaseSQL.classes.logtype
Log = BaseSQL.classes.log
ProductType = BaseSQL.classes.producttype
Product = BaseSQL.classes.product   
User = BaseSQL.classes.user