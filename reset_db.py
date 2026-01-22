# reset_db.py
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys

def reset_database():
    try:
        print("Connecting to PostgreSQL...")
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host="127.0.0.1",
            port="5432",
            user="postgres",
            password="DKmm28262507"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cur = conn.cursor()
        
        # Check if database exists
        print("Checking for existing database...")
        cur.execute("SELECT 1 FROM pg_database WHERE datname='bakery_db'")
        exists = cur.fetchone()
        
        if exists:
            print("Dropping existing database 'bakery_db'...")
            # Terminate existing connections first
            cur.execute("""
                SELECT pg_terminate_backend(pid) 
                FROM pg_stat_activity 
                WHERE datname='bakery_db' AND pid <> pg_backend_pid()
            """)
            cur.execute("DROP DATABASE bakery_db")
            print("Database dropped successfully!")
        
        print("Creating new database 'bakery_db'...")
        cur.execute("CREATE DATABASE bakery_db")
        print("Database 'bakery_db' created successfully!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your password")
        print("3. Try starting PostgreSQL service:")
        print("   - Open Services (services.msc)")
        print("   - Find 'PostgreSQL' service")
        print("   - Start it if stopped")
        sys.exit(1)

if __name__ == "__main__":
    reset_database()