import sqlite3

def get_users():
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    db.close()
    return users

def create_new_user(username, password, email):
    try:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username, ))
        d = c.fetchone()
        if d != None:
            db.close()
            return False
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        db.commit()
        db.close()
        return True
    except:
        db.close()
        return False

def fetch_user(username):
    try:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT password, id, username FROM users WHERE username = ?", (username, ))
        data = c.fetchone()
        if data:
            db.close()
            return data
        else:
            db.close()
            return False
    except:
        db.close()
        return False

def create_new_album(name, description, owner):
    try:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("INSERT INTO albums (ownerid, about, name) VALUES (?,?,?)", (owner, description, name))
        db.commit()
        c.execute("SELECT * FROM albums WHERE id = (SELECT MAX(id) FROM albums)")
        data = c.fetchone()
        print(data)
        return data
    except:
        db.close()
        return False
