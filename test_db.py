#!/usr/bin/env python3
"""
Database connection test script for TeslaMate fuel price app.
This script tests the connection to the TeslaMate PostgreSQL database.
"""

import os
import sys
import psycopg2

def test_db_connection():
    """Test database connection with current environment variables."""
    try:
        print("Testing database connection...")
        print(f"Host: {os.environ.get('DATABASE_HOST', 'Not set')}")
        print(f"Database: {os.environ.get('DATABASE_NAME', 'Not set')}")
        print(f"User: {os.environ.get('DATABASE_USER', 'Not set')}")
        print(f"Password: {'Set' if os.environ.get('DATABASE_PASS') else 'Not set'}")
        
        conn = psycopg2.connect(
            host=os.environ.get('DATABASE_HOST', 'database'),
            database=os.environ.get('DATABASE_NAME'),
            user=os.environ.get('DATABASE_USER'),
            password=os.environ.get('DATABASE_PASS')
        )
        
        # Test query
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"✅ Connection successful!")
            print(f"PostgreSQL version: {version[0]}")
            
            # Check if fuel_prices table exists
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'fuel_prices'
                );
            """)
            table_exists = cur.fetchone()[0]
            
            if table_exists:
                print("✅ fuel_prices table exists")
                cur.execute("SELECT COUNT(*) FROM fuel_prices;")
                count = cur.fetchone()[0]
                print(f"📊 Records in fuel_prices table: {count}")
            else:
                print("⚠️  fuel_prices table does not exist. Run init-fuel-prices-table.sql first.")
        
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_db_connection()
    sys.exit(0 if success else 1)
