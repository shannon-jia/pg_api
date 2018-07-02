# -*- coding: utf-8 -*-

"""Console script for pg_api."""

import asyncio
import click
import asyncpg


@click.group()
def main():
    """Manage PostgreSQL"""
    pass


schemas = {
    'hardware': 'pg_api/utils/hardware.sql',
    'map': 'pg_api/utils/map.sql',
    'snippet': 'pg_api/utils/snippet.sql'
}


@main.command('create')
@click.option('--dsn', envvar='DB_DSN',
              default='postgresql://postgres:passwd+123@localhost/test',
              help='PostgreSQL dsn, also ENV: DB_DSN')
@click.argument('name')
def create(dsn, name):
    """create PostgreSql schema and table."""

    print('Database: {}'.format(dsn))
    loop = asyncio.get_event_loop()

    if name in schemas:
        sql_file = schemas.get(name)
        print('>>> create schema: {} with file: {}...'.format(name, sql_file))
        loop.run_until_complete(exec_sql(dsn, sql_file))
    elif name == 'all' or name == 'ALL':
        for k, v in schemas.items():
            print('>>> create schema: {} with file: {} ...'.format(k, v))
            loop.run_until_complete(exec_sql(dsn, v))
    else:
        print('Error! need a schema name')

    loop.close()


async def exec_sql(dsn, schema_filename):
    conn = await asyncpg.connect(dsn)
    with open(schema_filename, 'rt') as f:
        schema = f.read()
        await conn.execute(schema)
        print('>>> Finish!')
        f.close()

    await conn.close()

if __name__ == "__main__":
    main()
