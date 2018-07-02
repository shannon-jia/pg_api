#!/usr/bin/env python3
import asyncio
import asyncpg
# import datetime


async def main(dsn='postgresql://postgres:passwd+123@localhost/test'):
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect(dsn)

    await conn.execute('''
        DROP TABLE IF EXISTS logs;
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS tag_type;
        CREATE TYPE tag_type AS ENUM (
            '入侵者',
            '垃圾',
            '测试',
            '动物',
            '工作人员',
            '天气',
            '植被'
       )
    ''')

    await conn.execute('''
        DROP TYPE IF EXISTS handler_type;
        CREATE TYPE handler_type AS ENUM (
            'USER',
            'SCM'
       )
    ''')    

    # Execute a statement to create a new table.
    await conn.execute('''
        DROP TABLE IF EXISTS logs;
        CREATE TABLE logs(
            id serial PRIMARY KEY,
            name text,
            time text default now(),
            type alarm_type,
            status alarm_status,
            tag tag_type,
            handleTime text default now(),
            handler handler_type default 'SCM',
            discription text default 'SystemLog',
            note text
       )
    ''')

    # Insert a record into the created table.
    await conn.execute('''
        INSERT INTO logs(name, type, status, tag, note)
                    VALUES($1, $2, $3, $4, $5)
    ''', 'SBC_0_1', 'CABLE FAULT', 'OCCURRED', '测试', 'DON NOT HAVE' )

    # Select a row from the table.
    row = await conn.fetch(
        'SELECT * FROM logs')
    print(row)

    # Close the connection.
    await conn.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
