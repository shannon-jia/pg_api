# -*- coding: utf-8 -*-

from sanic import response
from sanic import Blueprint


class Cruds(Blueprint):

    def __init__(self, name, query, pool=None, call_back=None):
        super().__init__(name)
        self.query = query
        self.pool = pool
        self.call_back = call_back
        self.add_route(self.root_get, '', methods=['GET'])

    def jsonify(self, records):
        """
        Parse asyncpg record response into JSON format
        """
        # return [dict(r.items()) for r in records]
        rs = [dict(r.items()) for r in records]
        if self.call_back:
            rs = self.call_back(rs)
        return rs

    async def root_get(self, request):
        args = request.raw_args
        async with self.pool.acquire() as connection:
            try:
                (_qy, values) = self.query.get(args)
                results = await connection.fetch(_qy, *values)
                return response.json(self.jsonify(results))
            except Exception as e:
                return response.json({'error': e.args or e},
                                     status=500)
            finally:
                await self.pool.release(connection)

    async def root_post(self, request):
        datas = request.json
        if not datas:
            return response.json({'error': 'empty body'})
        async with self.pool.acquire() as connection:
            try:
                (_qy, values) = self.query.post(datas=datas)
                results = await connection.execute(_qy, *values)
                return response.json({'results': results})
            except Exception as e:
                return response.json({'error': e.args or e},
                                     status=500)
            finally:
                await self.pool.release(connection)

    async def root_options(self, request):
        return response.json({'supported': True})

    async def id_get(self, reqeust, id):
        async with self.pool.acquire() as connection:
            try:
                args = {'id': id}
                (_qy, values) = self.query.get(args)
                results = await connection.fetch(_qy, *values)
                return response.json(self.jsonify(results))
            except Exception as e:
                return response.json({'error': e.args or e},
                                     status=500)
            finally:
                await self.pool.release(connection)

    async def id_delete(self, request, id):
        async with self.pool.acquire() as connection:
            try:
                args = {'id': id}
                (_qy, values) = self.query.delete(args)
                results = await connection.execute(_qy, *values)
                return response.json({'results': results})
            except Exception as e:
                return response.json({'error': e.args or e},
                                     status=500)
            finally:
                await self.pool.release(connection)

    async def root_delete(self, request):
        args = request.raw_args
        if not args:
            return response.json({'error': 'empty condition'})
        async with self.pool.acquire() as connection:
            try:
                (_qy, values) = self.query.delete(args)
                results = await connection.execute(_qy, *values)
                return response.json({'results': results})
            except Exception as e:
                return response.json({'error': e.args or e},
                                     status=500)
            finally:
                await self.pool.release(connection)

    async def root_update(self, request):
        args = request.raw_args
        datas = request.json
        if not datas or not args:
            return response.json({'error': 'empty body or empty condition'})
        async with self.pool.acquire() as connection:
            try:
                (_qy, values) = self.query.update(args, datas)
                results = await connection.execute(_qy, *values)
                return response.json({'results': results})
            except Exception as e:
                return response.json({'error': e.args or e},
                                     status=500)
            finally:
                await self.pool.release(connection)

    async def id_update(self, request, id):
        datas = request.json
        if not datas:
            return response.json({'error': 'empty body'})
        async with self.pool.acquire() as connection:
            try:
                args = {'id': id}
                (_qy, values) = self.query.update(args, datas)
                results = await connection.execute(_qy, *values)
                return response.json({'results': results})
            except Exception as e:
                return response.json({'error': e.args or e},
                                     status=500)
            finally:
                await self.pool.release(connection)

    async def id_options(self, request, id):
        return response.json({'supported': True})
