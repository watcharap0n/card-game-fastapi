from fastapi import APIRouter, Response, Path, HTTPException, Body, Query
from db import MongoDB
import numpy as np
from numpy import random
from bson import ObjectId
from random import sample
from object_str import Foo
from typing import Optional

router = APIRouter()
# db = MongoDB(database_name='Poker', uri='mongodb://127.0.0.1:27017')
db = MongoDB(database_name='Poker',
             uri='mongodb://s5919410022:0834482040@cluster0-shard-00-00.hhtgp.mongodb.net:27017,'
                 'cluster0-shard-00-01.hhtgp.mongodb.net:27017,'
                 'cluster0-shard-00-02.hhtgp.mongodb.net:27017/line_bot?ssl=true&replicaSet=Cluster0-shard-0'
                 '&authSource=admin&retryWrites=true&w=majority')
collection = 'create_card'


def update_one_list(id, index, boolean, num: Optional[int] = None):
    sate = db.find_one(collection=collection, query={'card_id': id})
    if num:
        e = sate['num'] + 1
        sate['num'] = e
    data = sate['cards']
    iterate = [x for x in data if x['id'] == index]
    iterate[0]['matching'] = boolean
    query = {'card_id': id}
    values = {'$set': sate}
    db.update_one(collection=collection, values=values, query=query)


@router.get('/create_card/{name}')
async def create_card(
        response: Response,
        name: str
):
    n = np.arange(6)
    n[:] = sample(range(0, 6), 6)
    np.random.shuffle(n)
    Id = Foo(_id=ObjectId())
    Id = Id.dict()['id']
    fruits = ['apple', 'banana', 'strawberry', 'orange', 'pieapple', 'watermelon']
    correct_encoder = [
        {
            'name': fruits[int(v)],
            'id': int(v),
            'img': f'{fruits[int(v)]}.png',
            'matching': False, 'flipped': False,
        }
        for v in n]
    created = {'cards': correct_encoder, 'card_id': Id, 'num': 0, 'username': name}
    db.insert_one(collection=collection, data=created)
    user = db.find(collection=collection, query={'username': name})[1:]
    user = [u['num'] for u in user]
    user = [i for i in user if i >= 12]
    if user:
        best_user = db.find(collection='award', query={})[1:]
        best_user = [i['best'] for i in best_user]
        response.set_cookie(key='id_card', value=Id, expires=60 * 20)
        del created['_id']
        return {'cards': created['cards'], 'my_best': min(user), 'best': min(best_user)}
    best_user = db.find(collection='award', query={})[1:]
    best_user = [i['best'] for i in best_user]
    response.set_cookie(key='id_card', value=Id, expires=60 * 20)
    del created['_id']
    return {'cards': created['cards'], 'my_best': 0, 'best': min(best_user)}
    # return {'cards': created['cards'], }


@router.put('/{id}')
async def card_id(
        id: int = Path(..., title="The ID of the card to get"),
        q: str = None
):
    cards = db.find_one_lasted(collection=collection, query={'card_id': q})
    card = cards['cards'][id]
    if not cards:
        raise HTTPException(status_code=401, detail={'bad request'})
    return card


@router.post('/flippedCard')
async def flippedCard(
        payload: Optional[dict] = Body(None)
):

    update_one_list(id=payload['id'], index=payload['index'], boolean=payload['query'])
    card = db.find_one(collection=collection, query={'card_id': payload['id']})
    iterate = [x['matching'] for x in card['cards']]
    check = all(iterate)
    if check:
        db.insert_one(collection='award', data={'best': card['num'], 'user': payload['global']})
        user = db.find(collection='award', query={})
        user = [i['best'] for i in user]
        score = min(i for i in user if i >= 12)
        return {'num': card['num'], 'check': check, 'best': score}
    return {'message': 'success'}


@router.post('/updateCard')
async def updateCard(
        payload: Optional[dict] = Body(None)
):
    update_one_list(id=payload['id'], index=payload['index'], boolean=payload['query'], num=payload['num'])
    card = db.find_one(collection=collection, query={'card_id': payload['id']})
    del card['_id']
    return {'num': card['num']}


@router.get('/getFlipped/{id}')
async def getFlipped(id: str = None):
    data = db.find_one(collection=collection, query={'card_id': id})
    del data['_id']
    return data
