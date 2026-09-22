import sqlite3

conn = sqlite3.connect('customers.db')
c = conn.cursor()
cols = [r[1] for r in c.execute('PRAGMA table_info(customers)').fetchall()]

if 'status' not in cols:
    c.execute("ALTER TABLE customers ADD COLUMN status TEXT DEFAULT 'Pending'")
    # Explicitly ensure any nulls become 'Pending'
    c.execute("UPDATE customers SET status = 'Pending' WHERE status IS NULL OR status = ''")
    conn.commit()
    print("Added status column to customers table with default 'Pending'!")
else:
    print("'status' column already exists in customers table.")

dist = c.execute('SELECT status, COUNT(*) FROM customers GROUP BY status').fetchall()
print("Current Status distribution in DB:", dist)

conn.close()
