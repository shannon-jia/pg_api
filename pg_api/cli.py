# -*- coding: utf-8 -*-

"""Console script for pg_api."""

import click
from .main import app, DB_CONFIG


@click.command()
@click.option('--dsn', envvar='DB_DSN',
              default='postgresql://postgres:passwd+123@localhost/dev.samlite',
              help='PostgreSQL dsn, also ENV: DB_DSN')
@click.option('--port', default=8080,
              envvar='API_PORT',
              help='Api port, default=8080, ENV: API_PORT')
def main(dsn, port):
    """Console script for pg_api."""

    click.echo("See more documentation at http://www.mingvale.com")

    DB_CONFIG['dsn'] = dsn
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()
