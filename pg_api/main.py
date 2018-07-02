from asyncpg import create_pool

from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS

# need to add-on for new table
from .blueprint.devices import bp as devices
from .blueprint.segments import bp as segments
from .blueprint.fields import bp as fields
from .blueprint.lscs import bp as lscs
from .blueprint.logs import bp as logs
from .blueprint.alarms import bp as alarms
from .blueprint.commands import bp as commands
from .blueprint.stations import bp as stations
from .blueprint.zones import bp as zones
from .blueprint.links import bp as links

DB_CONFIG = {
    # 'host': 'localhost',
    # 'user': 'postgres',
    # 'password': 'passwd+123',
    # 'database': 'test'
}

api_info = {
    'version': '1.0.0',
    'uri': ['/devices/<id:int>',
            '/fields/<id:int>',
            '/segments/<id:int>',
            '/lscs/<id:int>',
            '/logs/<id:int>',
            '/alarms/<id:int>',
            '/commands/<device_name:str>',
            '/stations/<id:int>',
            '/links/<id:int>',
            '/zones/<id:int>'],
    'cors': True,
    'database': 'PostgreSQL',
    'request_timeout': 60,
    'max_size': 100
}

app = Sanic(__name__)

# need to add-on for new table
app.blueprint(devices, url_prefix='/devices')
app.blueprint(segments, url_prefix='/segments')
app.blueprint(fields, url_prefix='/fields')
app.blueprint(lscs, url_prefix='/lscs')
app.blueprint(logs, url_prefix='/logs')
app.blueprint(alarms, url_prefix='/alarms')
app.blueprint(commands, url_prefix='/commands')
app.blueprint(stations, url_prefix='/stations')
app.blueprint(zones, url_prefix='/zones')
app.blueprint(links, url_prefix='/links')

CORS(app)


@app.listener('before_server_start')
async def register_db(app, loop):
    app.pool = await create_pool(**DB_CONFIG, loop=loop, max_size=100)

    # need to add-on for new table
    devices.pool = app.pool
    segments.pool = app.pool
    fields.pool = app.pool
    lscs.pool = app.pool
    logs.pool = app.pool
    alarms.pool = app.pool
    stations.pool = app.pool
    zones.pool = app.pool
    links.pool = app.pool


@app.listener('before_server_stop')
async def close_db(app, loop):
    await app.pool.close()


@app.route('/', methods=['OPTIONS'])
async def root_options(request):
    return json(api_info)


@app.route('/', methods=['GET'])
async def root_get(request):
    return json(api_info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
