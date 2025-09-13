import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a-very-secure-secret')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get('DATABASE_HOST'),
            database=os.environ.get('DATABASE_NAME'),
            user=os.environ.get('DATABASE_USER'),
            password=os.environ.get('DATABASE_PASS')
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    prices = []
    if conn:
        try:
            with conn.cursor() as cur:
                # Modified to select both price columns
                cur.execute("SELECT date, price_diesel, price_gasoline FROM fuel_prices ORDER BY date DESC;")
                prices = cur.fetchall()
            conn.close()
        except psycopg2.Error as e:
            flash(f'Error querying prices: {e}', 'error')
    else:
        flash('Could not connect to the database.', 'error')
    
    return render_template('index.html', prices=prices)

@app.route('/add', methods=['POST'])
def add_price():
    date = request.form['date']
    price_diesel = request.form['price_diesel']
    price_gasoline = request.form['price_gasoline']
    
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                # Modified to insert/update both price columns
                sql = """
                    INSERT INTO fuel_prices (date, price_diesel, price_gasoline) 
                    VALUES (%s, %s, %s) 
                    ON CONFLICT (date) DO UPDATE SET 
                        price_diesel = EXCLUDED.price_diesel, 
                        price_gasoline = EXCLUDED.price_gasoline;
                """
                cur.execute(sql, (date, price_diesel, price_gasoline))
            conn.commit()
            conn.close()
            flash('Prices added/updated successfully.', 'success')
        except psycopg2.Error as e:
            flash(f'Error saving prices: {e}', 'error')
    else:
        flash('Could not connect to the database to save prices.', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
