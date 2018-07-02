#!/usr/bin/env python3
import asyncio
import asyncpg
# import datetime


async def main(dsn='postgresql://postgres:passwd+123@localhost/test'):
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect(dsn)

    await conn.execute('''
        DROP TABLE IF EXISTS stations;
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS selected_type;
        CREATE TYPE selected_type AS ENUM (
            'TRUE',
            'FALSE'
       )
    ''')    

    # Execute a statement to create a new table.
    await conn.execute('''
        DROP TABLE IF EXISTS stations;
        CREATE TABLE stations(
            id serial PRIMARY KEY,
            value text,
            name text,
            selected selected_type
       )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO stations(value, name, selected)
                    VALUES($1, $2, $3)
    ''', 'EEDS', '鄂尔多斯', 'FALSE')

    await conn.execute('''
        INSERT INTO stations(value, name, selected)
                    VALUES($1, $2, $3)
    ''', 'WLCB', '乌兰察布', 'FALSE')

    await conn.execute('''
        INSERT INTO stations(value, name, selected)
                    VALUES($1, $2, $3)
    ''', 'ZJK', '张家口', 'FALSE')

    await conn.execute('''
        INSERT INTO stations(value, name, selected)
                    VALUES($1, $2, $3)
    ''', 'TKT', '托克托', 'FALSE')

    await conn.execute('''
        INSERT INTO stations(value, name, selected)
                    VALUES($1, $2, $3)
    ''', 'YQ', '延庆', 'TRUE')
    # Select a row from the table.
    row = await conn.fetch(
        'SELECT * FROM stations')
    print(row)

    # Close the connection.
    await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
