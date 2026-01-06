from database import get_database
from bson.objectid import ObjectId

db = get_database()
musics = db["music"]

def create_music(music, artist):
    musics.insert_one({
        "your favorite music": music,
        "artist": artist,
        
    })



