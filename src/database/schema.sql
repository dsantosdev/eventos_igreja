CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_name TEXT NOT NULL,
    purchase_date TEXT NOT NULL,
    event_id INTEGER NOT NULL,
    ticket_quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    payment_method TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id)
);