import shopping_cart
from conf.setting import BANK_DB_PATH
from core.logger import debug_log
from core.json_db import JsonDb


db = JsonDb(BANK_DB_PATH, ['name'])
db.add({'name':'zeno'})
db.update('1', {'name':'zeno40'})
print(db.select('1'))
