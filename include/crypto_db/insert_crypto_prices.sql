INSERT INTO crypto_prices 
(
    crypto_symbol, 
    capture_date, 
    price_currency, 
    price_open, 
    price_close
)
    VALUES 
        (
            %(crypto_symbol)s, 
            %(capture_date)s, 
            %(price_currency)s, 
            %(price_open)s, 
            %(price_close)s
        );