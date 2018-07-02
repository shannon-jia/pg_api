#!/Usr/bin/env python3
import asyncio
import asyncpg
# import datetime


async def main(dsn='postgresql://postgres:passwd+123@localhost/test'):
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect(dsn)

    await conn.execute('''
        DROP TABLE IF EXISTS links;
    ''')
    
    # Execute a statement to create a new table.
    await conn.execute('''
        DROP TABLE IF EXISTS links;
        CREATE TABLE links(
            id serial PRIMARY KEY,
            name text,
            zone text,
            lsc text,
            action text,
            comment text
       )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO links(name, zone, lsc, action, comment)
                    VALUES($1, $2, $3, $4, $5)
    ''', 'ld1', 'fq1', 'SPEAKER_1', 'secure', 'SPEAKER_1')    

    # Select a row from the table.
    row = await conn.fetch(
        'SELECT * FROM links')
    print(row)

    # Close the connection.
    await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
