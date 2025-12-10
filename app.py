from flask import Flask
import redis
import psycopg2
from psycopg2 import OperationalError
import os

app = Flask(__name__)

r = redis.Redis(host="redis", port=6379)
    
def check_db():
     """Try connecting to PostgreSQL to see if it's running"""
     try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=int(os.getenv("DB_PORT",5432))
        )
        conn.close()
        return True
     except OperationalError:
         return False
            

@app.route("/")
def health():
    try:
        r.ping()
        redis_stats = "UP"
    except redis.exceptions.ConnectionError:
        redis_stats = "DOWN"

    db_stats = "Up" if check_db() else "DOWN!"
    return f"Redis: {redis_stats}, Database: {db_stats}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
