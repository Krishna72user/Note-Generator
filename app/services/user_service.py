from app.schemas.user import RegisterRequest,LoginRequest
from fastapi import HTTPException

import bcrypt


def register(regis: RegisterRequest,conn):
    email = regis.email
    name= regis.name
    passwrd = regis.password
    with conn.cursor() as cursor:
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query,(email,))

        if cursor.fetchone() :
            status = 0
        else:
            hashed = bcrypt.hashpw(
                passwrd.encode(),
                bcrypt.gensalt()
            ).decode()

            cursor.execute(
                """
                INSERT INTO users(name, email, password_hash)
                VALUES(%s, %s, %s)
                RETURNING id
                """,
                (name, email, hashed)
            )
            status = 1

    conn.commit()
    conn.close()
    if status ==1:
        return {
        "message": "User created successfully",
        "user":{"name": name,'email':email},
        'status':201
        }
    else: raise HTTPException(
                status_code=409,
                detail="User already exists"
            )

    

def login(login: LoginRequest,conn):
    password = login.password
    email = login.email
    with conn.cursor() as cursor:
        query = "SELECT email,name,password_hash FROM users WHERE email = %s"
        cursor.execute(query,(email,))
        user = cursor.fetchone()
        conn.close()
        if user:
            if bcrypt.checkpw(password.encode(),user[2].encode()): 
                return {"message":"Login Successful","user":{"name":user[1],"email":user[0]},"status":200}
            else:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid Credentials"
                )
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid Credentials"
            )
