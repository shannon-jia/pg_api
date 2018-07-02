# -*- coding: utf-8 -*-

import json
from sanic import response
from sanic import Blueprint
from .query import Query

bp = Blueprint(__name__)
TABLE_NAME = 'devices'
query = Query(TABLE_NAME,
              key_type={
                  'layer': int,
                  'id': int
              })


def jsonify(records):
    """
    Parse asyncpg record response into JSON format
    """
    # return [dict(r.items()) for r in records]
    rs = [dict(r.items()) for r in records]
    for r in rs:
        actions = r.get('actions') or "{}"
        r['actions'] = json.loads(actions)
    return rs


@bp.route('', methods=['GET'])
async def root_get(request):
    args = request.raw_args
    async with bp.pool.acquire() as connection:
        try:
            (_qy, values) = query.get(args)
            results = await connection.fetch(_qy, *values)
            return response.json(jsonify(results))
        except Exception as e:
            return response.json({'error': e.args or e},
                                 status=500)
        finally:
            await bp.pool.release(connection)


@bp.route('', methods=['POST'])
async def root_post(request):
    datas = request.json
    if not datas:
        return response.json({'error': 'empty body'})
    async with bp.pool.acquire() as connection:
        try:
            (_qy, values) = query.post(datas=datas)
            results = await connection.execute(_qy, *values)
            return response.json({'results': results})
        except Exception as e:
            return response.json({'error': e.args or e},
                                 status=500)
        finally:
            await bp.pool.release(connection)


@bp.route('', methods=['OPTIONS'])
async def root_options(request):
    return response.json({'supported': True})


@bp.route('/<id:int>', methods=['GET'])
async def id_get(request, id):
    async with bp.pool.acquire() as connection:
        try:
            args = {'id': id}
            (_qy, values) = query.get(args)
            results = await connection.fetch(_qy, *values)
            return response.json(jsonify(results))
        except Exception as e:
            return response.json({'error': e.args or e},
                                 status=500)
        finally:
            await bp.pool.release(connection)


@bp.route('/<id:int>', methods=['DELETE'])
async def id_delete(request, id):
    async with bp.pool.acquire() as connection:
        try:
            args = {'id': id}
            (_qy, values) = query.delete(args)
            results = await connection.execute(_qy, *values)
            return response.json({'results': results})
        except Exception as e:
            return response.json({'error': e.args or e},
                                 status=500)
        finally:
            await bp.pool.release(connection)


@bp.route('', methods=['DELETE'])
async def root_delete(request):
    args = request.raw_args
    if not args:
        return response.json({'error': 'empty condition'})
    async with bp.pool.acquire() as connection:
        try:
            (_qy, values) = query.delete(args)
            results = await connection.execute(_qy, *values)
            return response.json({'results': results})
        except Exception as e:
            return response.json({'error': e.args or e},
                                 status=500)
        finally:
            await bp.pool.release(connection)


@bp.route('', methods=['PUT'])
async def root_update(request):
    args = request.raw_args
    datas = request.json
    if not datas or not args:
        return response.json({'error': 'empty body or empty condition'})
    async with bp.pool.acquire() as connection:
        try:
            (_qy, values) = query.update(args, datas)
            results = await connection.execute(_qy, *values)
            return response.json({'results': results})
        except Exception as e:
            return response.json({'error': e.args or e},
                                 status=500)
        finally:
            await bp.pool.release(connection)


@bp.route('/<id:int>', methods=['PUT'])
async def id_update(request, id):
    datas = request.json
    if not datas:
        return response.json({'error': 'empty body'})
    async with bp.pool.acquire() as connection:
        try:
            args = {'id': id}
            (_qy, values) = query.update(args, datas)
            results = await connection.execute(_qy, *values)
            return response.json({'results': results})
        except Exception as e:
            return response.json({'error': e.args or e},
                                 status=500)
        finally:
            await bp.pool.release(connection)


@bp.route('/<id:int>', methods=['OPTIONS'])
async def id_options(request, id):
    return response.json({'supported': True})
