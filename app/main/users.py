import hashlib
import bcrypt

users = {}
rooms = {}


def createUser(username, passwordHash, salt):
    if username not in users:
        users[username] = {
            "username": username, "passwordHash": passwordHash, "salt": salt
        }
    else:
        print("username exists")
        raise Exception(username)


def getUser(username):
    if username in users:
        print(users[username])
        return True, users[username]
    else:
        return False, ""


def generateUsers():
    print("generating users...")
    for i in range(1, 4):
        salt = bcrypt.gensalt()
        createUser("user" + str(i), bcrypt.hashpw(("pass" + str(i)).encode(), salt).decode(), salt.decode())


def getRoom(room):
    if room in rooms:
        return rooms[room]
    else:
        rooms[room] = {"room": room, "room_key": hashlib.sha256(bcrypt.gensalt()).hexdigest()[:64]}
        return rooms[room]
