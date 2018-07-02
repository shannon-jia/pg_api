#!/usr/bin/env python3
import asyncio
import asyncpg
# import datetime


async def main(dsn='postgresql://postgres:passwd+123@localhost/test'):
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect(dsn)

    await conn.execute('''
        DROP TABLE IF EXISTS alarms;
    ''')
    
    await conn.execute('''
        DROP TYPE IF EXISTS alarm_type;
        CREATE TYPE alarm_type AS ENUM (
            'CABLE ALARM',
            'TAMPER CLOSE',
            'AUXILIARY',
            'CABLE FAULT',
            'COMM FAIL'
       )
    ''')
    
    await conn.execute('''
        DROP TYPE IF EXISTS alarm_status;
        CREATE TYPE alarm_status AS ENUM (
            'OCCURRED'
       )
    ''')

    # Execute a statement to create a new table.
    await conn.execute('''
        DROP TABLE IF EXISTS alarms;
        CREATE TABLE alarms(
            id serial PRIMARY KEY,
            time text default now(),
            device_name text,
            type alarm_type,
            status alarm_status,
            coords point,
            comment text,
            layer integer default 1,
            actions json
       )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO alarms(device_name, type, status, coords, comment, actions)
                    VALUES($1, $2, $3, $4, $5, $6)
    ''', 'SBC_0_1_B_1', 'CABLE ALARM', 'OCCURRED', (99.0, 58.0),
                       'DISPLAY SBC_0_1_B_1','{"布 防": "secure", "撤 防": "access"}' )

    # Select a row from the table.
    row = await conn.fetch(
        'SELECT * FROM alarms')
    print(row)

    # Close the connection.
    await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
