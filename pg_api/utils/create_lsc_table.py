#!/usr/bin/env python3
import asyncio
import asyncpg
# import datetime


async def main(dsn='postgresql://postgres:passwd+123@localhost/test'):
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect(dsn)

    await conn.execute('''
        DROP TABLE IF EXISTS lscs;
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS lsc_type;
        CREATE TYPE lsc_type AS ENUM (
            'LAMP',
            'SPEAKER',
            'CAMERA',
            'UNDEFINED'
       )
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS lsc_status;
        CREATE TYPE lsc_status AS ENUM (
            'ON',
            'OFF',
            'DISABLED'
       )
    ''')

    # Execute a statement to create a new table.
    await conn.execute('''
        DROP TABLE IF EXISTS lscs;
        CREATE TABLE lscs(
            id serial PRIMARY KEY,
            device_name text,
            type lsc_type,
            status lsc_status,
            coords point,
            comment text,
            layer integer default 1,
            actions json
       )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO lscs(device_name, type, status, coords, comment, actions)
                    VALUES($1, $2, $3, $4, $5, $6)
    ''', 'SPEAKER_1', 'SPEAKER', 'ON', (5.0, 20),
                       'DISPLAY SPEAKER 1','{"布 防": "secure", "撤 防": "access"}' )

    # Select a row from the table.
    row = await conn.fetch(
        'SELECT * FROM lscs')
    print(row)

    # Close the connection.
    await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
