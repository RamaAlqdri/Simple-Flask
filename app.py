from flask import Flask, request, jsonify
import os
# import psycopg2
from supabase import create_client, Client
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_PROJECT_URL: str = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_API_KEY: str = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)

@app.route('/makeroom', methods=['POST'])
def makeroom():
    data = request.get_json()  # Mendapatkan data JSON dari request
    room_name = data.get("name")  # Mengambil nama room dari data JSON
    
    if room_name:  # Pastikan nama room ada di dalam JSON
        result = supabase.table("Room").insert({"name": room_name}).execute()
        print(result.data)
        return result.data
    else:
        return {"error": "Room name is missing"}, 400  # Kembalikan error jika nama room tidak ada


@app.route('/create_message', methods=['POST'])
def create_message():
    data = request.get_json()
    room_id = data.get("room_id")
    content = data.get("content")
    sender = data.get("sender")
    
    if room_id and content and sender:
        result = supabase.table("Message").insert({"room_id": room_id, "content": content, "sender": sender}).execute()
        print(result.data)
        return result.data
    else:
        return {"error": "Room ID, content, or sender is missing"}, 400
    
@app.route('/get_room_messages', methods=['GET'])
def get_room_messages():
    room_id = request.args.get("room_id")
    
    if room_id:
        result = supabase.table("Message").select("*").eq("room_id", room_id).execute()
        print(result.data)
        return result.data
    else:
        return {"error": "Room ID is missing"}, 400
    
@app.route('/get_rooms', methods=['GET'])
def get_rooms():
    result = supabase.table("Room").select("*").execute()
    print(result.data)
    return result.data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)  # Jalankan aplikasi Flask