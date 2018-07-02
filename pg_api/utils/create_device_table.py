#!/usr/bin/env python3
import asyncio
import asyncpg


async def main(dsn='postgresql://postgres:passwd+123@localhost/test'):
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect(dsn)
    await conn.execute('''
        DROP TABLE IF EXISTS devices;
    ''')
    # Execute a statement to create a new table.
    await conn.execute('''
        DROP TYPE IF EXISTS dev_status;
        CREATE TYPE dev_status AS ENUM (
            'SECURED',
            'ACCESSED',
            'TAMPER',
            'NORMAL',
            'COMM FAIL',
            'CABLE FAULT'
       )
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS dev_type;
        CREATE TYPE dev_type AS ENUM (
            'PM',
            'CABLE',
            'SENSOR',
            'TU',
            'LU',
            'ILU',
            'ROM08',
            'ROM16',
            'RM',
            'RCM',
            'AIM',
       )
    ''')

    await conn.execute('''
        DROP TABLE IF EXISTS devices;
        CREATE TABLE devices(
            id serial PRIMARY KEY,
            device_name text,
            type dev_type,
            status dev_status,
            coords point,
            comment text,
            layer integer default 1,
            actions json
       )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO devices(device_name, type, status, coords, comment, actions)
                    VALUES($1, $2, $3, $4, $5, $6)
    ''', 'PM_0_1', 'PM', 'NORMAL', (5.0, 5.0), 'PM_1',
                       '{"布 防": "secure", "撤 防": "access"}')

    await conn.execute('''
        INSERT INTO devices(device_name, type, status, coords, comment, actions)
                    VALUES($1, $2, $3, $4, $5, $6)
    ''', 'ROM08_0_2', 'ROM08', 'NORMAL', (15.0, 25.0), 'ROM08_1',
                       "{ \"secure\": \"secure\", \"access\": \"access\"}")

    row = await conn.fetch(
        'SELECT * FROM devices')
    print(row)

    # Close the connection.
    await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
