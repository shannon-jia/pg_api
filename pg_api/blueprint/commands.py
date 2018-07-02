# -*- coding: utf-8 -*-

import json
from sanic import response
from sanic import Blueprint

bp = Blueprint(__name__)


@bp.route('/<device_name>', methods=['POST'])
async def root_post(request, device_name):
    body = request.json
    print(body)
    try:
        command = body.get("command")
        return response.json({'results': command})
    except Exception as e:
        return response.json({'error': e.args or e},
                             status=500)
    finally:
        pass


