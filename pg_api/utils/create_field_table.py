#!/usr/bin/env python3
import asyncio
import asyncpg
# import datetime


async def main(dsn='postgresql://postgres:passwd+123@localhost/test'):
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect(dsn)

    await conn.execute('''
        DROP TABLE IF EXISTS fields;
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS field_type;
        CREATE TYPE field_type AS ENUM (
            'FIELD',
            'AUXILIARY',
            'SENSOR'
       );
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS field_status;
        CREATE TYPE field_status AS ENUM (
            'SECURED',
            'ACCESSED',
            'COMM FAIL',
            'ALARMED'
       );
    ''')

    # Execute a statement to create a new table.
    await conn.execute('''
        DROP TABLE IF EXISTS fields;
        CREATE TABLE fields(
            id serial PRIMARY KEY,
            device_name text,
            type field_type NOT NULL,
            status field_status,
            field polygon,
            comment text,
            layer integer default 0,
            actions json
       );
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO fields(device_name, type, status, field, comment, actions)
                    VALUES($1, $2, $3, $4, $5, $6)
    ''', 'SENSOR_0_1', 'AUXILIARY', 'SECURED',
                       ((5.0, 5.0), (20, 20), (35, 35), (55, 55)),
                       'SENSOR 1', '{"布 防": "secure", "撤 防": "access"}')

    row = await conn.fetch(
        'SELECT * FROM fields')
    print(row)

    # Close the connection.
    await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
