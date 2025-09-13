-- SQL script to create the fuel_prices table in your TeslaMate database
-- Run this script against your TeslaMate PostgreSQL database

CREATE TABLE IF NOT EXISTS fuel_prices (
    date DATE PRIMARY KEY,
    price_diesel DECIMAL(5,3) NOT NULL,
    price_gasoline DECIMAL(5,3) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index for better query performance
CREATE INDEX IF NOT EXISTS idx_fuel_prices_date ON fuel_prices(date DESC);

-- Create a trigger to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_fuel_prices_updated_at 
    BEFORE UPDATE ON fuel_prices 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
