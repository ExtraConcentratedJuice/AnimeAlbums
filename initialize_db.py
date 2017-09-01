#Run this file to initialize AA's database
import sqlite3

db = sqlite3.connect('database.db')

db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)')

db.execute('CREATE TABLE IF NOT EXISTS userdata (id INTEGER PRIMARY KEY, username TEXT, about TEXT)')

db.execute('CREATE TABLE IF NOT EXISTS albums (id INTEGER PRIMARY KEY, ownerid INTEGER, about TEXT, name TEXT)')

db.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, ownerid INTEGER, about TEXT, tags TEXT, link TEXT, name TEXT)')

db.close()
