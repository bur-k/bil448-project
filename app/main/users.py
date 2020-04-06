import hashlib
import bcrypt

users = {} # global users dict to store users
rooms = {} # global rooms dict to store room specific keys


def createUser(username, passwordHash, salt): # if username does not exist creates user
    if username not in users:
        users[username] = {
            "username": username, "passwordHash": passwordHash, "salt": salt
        }
    else:
        print("username exists")
        raise Exception(username)


def getUser(username): # returns user with given username
    if username in users:
        print(users[username])
        return True, users[username]
    else:
        return False, ""


def generateUsers(): # generates user in given range 
    print("generating users...")
    for i in range(1, 4):
        salt = bcrypt.gensalt()
        createUser("user" + str(i), bcrypt.hashpw(("pass" + str(i)).encode(), salt).decode(), salt.decode())


def getRoom(room): # if room_key exists returns given room otherwise creates and returns
    if room in rooms:
        return rooms[room]
    else:
        rooms[room] = {"room": room, "room_key": hashlib.sha256(bcrypt.gensalt()).hexdigest()[:64]}
        return rooms[room]
