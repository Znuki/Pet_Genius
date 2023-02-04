from pymongo import MongoClient
client = MongoClient('mongodb+srv://dbUser:<sparta>@cluster0.7qlimrh.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta