from connection import *

async def create_user(username, fullname, telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        INSERT INTO users(user_name, full_name, telegram_id) Values
        ($1, $2, $3)
                """, username, fullname, telegram_id)
        print("User created successfuly")
        return conn
    except Exception as error:
        print(f"Error in creating user: {error}")
    finally:
        await conn.close()


async def get_users(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
    SELECT * FROM users where telegram_id = $1
                    """, telegram_id)
        print(f"Users selected successfuly")
        return user
    except Exception as error:
        print(f"Error in selecting users: {error}")
    finally:
        await conn.close()


async def add_asignment(title, due_date):
    try:
        conn = await connection_db()
        await conn.execute("""
    INSERT INTO assignments(title, due_date) Values
    ($1, $2)
                        """, title, due_date)
        return True
    except Exception as error:
        print(error)
    finally:
        await conn.close()



async def submit(telegram_id, assignment_id):
    try:
        conn = await connection_db()
        await conn.execute("""
    INSERT INTO submissions(telegram_id, assignment_id) Values
    ($1, $2)

                    """, telegram_id, assignment_id)
        return True
    except Exception as error:
        print(error)
    finally:
        await conn.close()








