# -*- coding: utf-8 -*-

"""Console script for pg_api."""

import asyncio
import click
from .utils.create_device_table import main as device
from .utils.create_field_table import main as field
from .utils.create_segment_table import main as segment
from .utils.create_lsc_table import main as lsc
from .utils.create_log_table import main as log
from .utils.create_alarm_table import main as alarm
from .utils.create_station_table import main as station
from .utils.create_zone_table import main as zone
from .utils.create_link_table import main as link

tables = {'device': device,
          'field': field,
          'segment': segment,
          'lsc': lsc,
          'log': log,
          'alarm': alarm,
          'station': station,
          'link': link,
          'zone': zone
          }


@click.command()
@click.option('--dsn', envvar='DB_DSN',
              default='postgresql://postgres:passwd+123@localhost/dev.samlite',
              help='PostgreSQL dsn, also ENV: DB_DSN')
@click.option('--table',
              help='which table need to create')
def main(dsn, table):
    """Console script for pg_api."""

    click.echo("See more documentation at http://www.mingvale.com")
    loop = asyncio.get_event_loop()

    if table in tables:
        print('>>> create {} table...'.format(table))
        create_table = tables.get(table)
        loop.run_until_complete(create_table(dsn))
    elif table == 'all' or table == 'ALL':
        for k, v in tables.items():
            print('>>> create {} table...'.format(k))
            loop.run_until_complete(v(dsn))
    else:
        print('Error! need a table name')

    loop.close()


if __name__ == "__main__":
    main()
