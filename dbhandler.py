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

def create_new_album(name, description, owner, thumbnail):
    try:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("INSERT INTO albums (ownerid, about, name, thumb) VALUES (?,?,?,?)", (owner, description, name, thumbnail))
        db.commit()
        c.execute("SELECT * FROM albums WHERE id = (SELECT MAX(id) FROM albums)")
        data = c.fetchone()
        return data
    except:
        db.close()
        return False

def create_new_post(name, description, link, owner, tags, albumid):
    try:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("INSERT INTO posts (ownerid, about, name, tags, link, albumid) VALUES (?,?,?,?,?,?)", (owner, description, name, tags, link, albumid))
        db.commit()
        db.close()
        return True
    except:
        db.close()
        return False

def fetch_album_posts(albumid):
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("SELECT * FROM posts WHERE albumid = ?", (albumid, ))
    posts = c.fetchall()
    db.close()
    return posts

def fetch_album(albumid):
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("SELECT * FROM albums WHERE id = ?", (albumid, ))
    album = c.fetchone()

    if album != None:
        db.close()
        return album
    else:
        db.close()
        return False

def fetch_album_owner(albumid):
    try:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT ownerid FROM albums WHERE id = ?", (albumid, ))
        ownerid = c.fetchone()[0]
        c.execute("SELECT id, username FROM users WHERE id = ?", (ownerid, ))
        data = c.fetchone()
        db.close()
        return data
    except:
        db.close()
        return False

def fetch_user_albums(userid):
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("SELECT * FROM albums WHERE ownerid = ?", (userid, ))
    albums = c.fetchall()
    db.close()
    return albums
