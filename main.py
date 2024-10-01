from typing import Annotated
from fastapi import FastAPI, Form, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pymysql
import bcrypt                                       # the library that we are going to use for hashing passwords
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

rds_instance_pswd = os.getenv('RDS_INSTANCE_PSWD')

"""
Steps for storing env variable for RDS_Instance:
1) create .env file in this python file's directory
2) enter RDS_INSTANCE_PSWD = 'your_local_rds_instance_password'
3) Don't forget to include .env file in .gitignore file 
"""


def get_db_connection(db):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=rds_instance_pswd,
        database=db,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

@app.post("/authorize/",
            responses={
                    200: {"description": "Authorization Successful"},
                    401: {"description": "Unauthorized - Incorrect Password"},
                    404: {"description": "User or Organiser not found"},
                }
)
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()], utype: Annotated[str, Form()]):
    con = get_db_connection(utype.lower())
    table = 'org_tab' if utype.lower() == 'organiser' else 'user_tab'
    cur = con.cursor()
    sql = f"select name, hashedpswd from {table} where email = '{email}'"
    cur.execute(sql)
    result = cur.fetchone()
    con.close()
    if result is not None:
        if bcrypt.checkpw(password.encode('utf-8'), result['hashedpswd'].encode('utf-8')):
            return JSONResponse(content={"message": f"Authorization Successful!", "User": result['name']}, status_code=200)
        else: return JSONResponse(content={"message": f"Authorization unsuccessful! Incorrect Password for {email}"}, status_code = 401)
    else: return JSONResponse(content={"message": f"{utype.title()} - {email} Not Found!"}, status_code = 404)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


'''
Below are the actual credentials for users and organisers. The passwords stored in DB are hashed.
To test the login endpoint:
enter email, password and user type i.e user or organiser

User type: 'user'
email, password

johndoe@example.com, aaaaaaaa
janesmith@example.com, bbbbbbbb
robertbrown@example.com, cccccccc
emilydavis@example.com, dddddddd
michaeljohnson@example.com, eeeeeeee


User type: 'organiser'
email, password

alice.johnson@example.com, ffffffff
david.smith@example.com, gggggggg
sophia.garcia@example.com, hhhhhhhh
liam.thompson@example.com, iiiiiiii
emma.brown@example.com, jjjjjjjj

'''

'''
To store hashed password in database:

def hash_pswd(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    bcrypt takes utf-8 encoded password and generaters hashed_password
    but since it is in bytes format, we decode it and store. The hash is still maintained.

'''