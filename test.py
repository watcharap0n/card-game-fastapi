from db import MongoDB
from typing import Optional
db = MongoDB(database_name='Poker',
             uri='mongodb://s5919410022:0834482040@cluster0-shard-00-00.hhtgp.mongodb.net:27017,'
                 'cluster0-shard-00-01.hhtgp.mongodb.net:27017,'
                 'cluster0-shard-00-02.hhtgp.mongodb.net:27017/line_bot?ssl=true&replicaSet=Cluster0-shard-0'
                 '&authSource=admin&retryWrites=true&w=majority')
collection = 'create_card'
user = db.find(collection=collection, query={'username': 'kane'})[1:]
user = [u['num'] for u in user]
user = [i for i in user if i >= 12]
if user:
    print(min(user))
print('ok')