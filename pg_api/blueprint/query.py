# -*- coding: utf-8 -*-
import json


class Query():
    """ About SQL query string and values"""

    def __init__(self, table_name, key_type={}):
        self.table = table_name
        self.key_type = key_type

    def convert_args(self, k, v):
        if k in self.key_type:
            return self.key_type[k](v)
        else:
            return v

    def convert(self, v):
        if isinstance(v, list):
            if isinstance(v[0], list):
                v = tuple((p[0], p[1]) for p in v)
            else:
                v = tuple(v)
        elif isinstance(v, dict):
            v = json.dumps(v, ensure_ascii=False)
        return v

    def get_set_str(self, datas, offset=0):
        x = zip(datas.keys(), range(len(datas)))
        set_item = ["{}=${}".format(k, n+1+offset) for k, n in x]
        set_str = ", ".join(set_item)
        return set_str

    def get_where_str(self, args, offset=0):
        x = zip(args.keys(), range(len(args)))
        where = ["{}=${}".format(k, n+1+offset) for k, n in x]
        where_str = " AND ".join(where)
        return where_str

    # Create
    def post(self, args=None, datas=None):
        _qy = '''INSERT INTO {}('''.format(self.table)
        name = ["{}".format(k) for k in datas.keys()]
        key_str = ", ".join(name)
        val = ["${}".format(n+1) for n in range(len(datas))]
        val_str = ", ".join(val)
        _qy += key_str + ") VALUES ( " + val_str + " );"
        values = [self.convert(v) for v in datas.values()]
        return (_qy, values)

    # Retieve
    def get(self, args=None, datas=None):
        if args:
            _qy = 'SELECT * FROM {} WHERE '.format(self.table)
            values = [self.convert_args(k, v) for k, v in args.items()]
            where = self.get_where_str(args)
            _qy += where + "; "
            return (_qy, values)
        else:
            _qy = 'SELECT * FROM {}'.format(self.table)
            return (_qy, ())

    # Update
    def update(self, args=None, datas=None):
        _qy = '''UPDATE {} SET '''.format(self.table)
        set_str = self.get_set_str(datas)
        set_values = [self.convert(v) for v in datas.values()]
        where_values = [self.convert_args(k, v) for k, v in args.items()]
        where_str = self.get_where_str(args, len(datas))
        _qy += set_str + " WHERE " + where_str + ";"
        values = set_values + where_values
        return (_qy, values)

    # Delete
    def delete(self, args=None, datas=None):
        _qy = 'DELETE FROM {} WHERE '.format(self.table)
        values = [self.convert_args(k, v) for k, v in args.items()]
        where = self.get_where_str(args)
        _qy += where + "; "
        return (_qy, values)
