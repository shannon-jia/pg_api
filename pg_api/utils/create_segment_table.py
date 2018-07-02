#!/usr/bin/env python3
import asyncio
import asyncpg
# import datetime


async def main(dsn='postgresql://postgres:passwd+123@localhost/test'):
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect(dsn)

    await conn.execute('''
        DROP TABLE IF EXISTS segments;
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS seg_type;
        CREATE TYPE seg_type AS ENUM (
            'SEGMENT'
       )
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS seg_status;
        CREATE TYPE seg_status AS ENUM (
            'SECURED',
            'ACCESSED',
            'CABLE FAULT'
       )
    ''')

    # Execute a statement to create a new table.
    await conn.execute('''
        DROP TABLE IF EXISTS segments;
        CREATE TABLE segments(
            id serial PRIMARY KEY,
            device_name text,
            type seg_type,
            status seg_status,
            path path,
            comment text,
            layer integer default 1,
            actions json
       )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO segments(device_name, type, status, path, comment, actions)
                    VALUES($1, $2, $3, $4, $5, $6)
    ''', 'SEG_0_1', 'SEGMENT', 'SECURED', ((5.0, 5.0), (20, 20)),
                       'DISPLAY SEGMENT 1','{"布 防": "secure", "撤 防": "access"}' )

    # Select a row from the table.
    row = await conn.fetch(
        'SELECT * FROM segments')
    print(row)

    # Close the connection.
    await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
