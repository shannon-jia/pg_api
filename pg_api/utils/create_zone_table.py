#!/usr/bin/env python3
import asyncio
import asyncpg
# import datetime


async def main(dsn='postgresql://postgres:passwd+123@localhost/test'):
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect(dsn)

    await conn.execute('''
        DROP TABLE IF EXISTS zones;
    ''')
    # Execute a statement to create a new table.
    await conn.execute('''
        DROP TYPE IF EXISTS zone_type;
        CREATE TYPE zone_type AS ENUM (
            'CABLE A',
            'CABLE B',
            'AUX',
            'PM',
            'ROM08',
            'ROM16',
            'AIM',
            'MTP',
            'Model310',
            'CABLE ALARM',
            'Model330'
       )
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS config_type;
        CREATE TYPE config_type AS ENUM (
            'SECURE',
            'ACCESS',
            'dISABLE'
       )
    ''')    
    
    # Execute a statement to create a new table.
    await conn.execute('''
        DROP TABLE IF EXISTS zones;
        CREATE TABLE zones(
            id serial PRIMARY KEY,
            name text,
            line integer,
            which integer,
            unit integer,
            wing zone_type,
            range int4range,
            config config_type,
            description text
       )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO zones(name, line, which, unit, wing,range, config, description)
                    VALUES($1, $2, $3, $4, $5,'[10,100)'::int4range, $6, $7)
    ''', 'fq1', 1, 1, 1, 'CABLE A', 'SECURE', 'A10-100')

    # Select a row from the table.
    row = await conn.fetch(
        'SELECT * FROM zones')
    print(row)

    # Close the connection.
    await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
