from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()

pasw = os.getenv("password")


async def connection_db():
    try:
        conn = await asyncpg.connect(
            host = "localhost",
            port = 5432,
            user = "postgres",
            database = "home_work",
            password = pasw 
        )
        print("Connected successfuly")
        return conn
    except Exception as error:
        print(f"Error in connectiong database: {error}")



async def create_table_db():
        try:
            conn = await connection_db()
            await conn.execute("""
    Create table if not exists users(
    telegram_id bigint primary key,
    user_name varchar(50),
    full_name varchar(50),
    is_active boolean  default true,
    created_at timestamp default now()
    );


    Create table if not exists assignments(
    assignment_id bigint primary key,
    title varchar(50),
    due_date timestamp,
    is_active boolean default true,
    created_at timestamp default now()
    );

    Create table if not exists submissions(
    submission_id bigint primary key,
    telegram_id bigint,
    assignment_id int references assignments(assignment_id),
    submitted_at timestamp default now(),
    grade int check(grade between 1 and 100) 
    )
                        """)
            print("Table created successfuly")
            print("Bot started")
            return conn
        except Exception as error:
            print(f"Error in creating table: {error}")
        finally:
            await conn.close()