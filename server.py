import socket, threading, json, time
from game_engine import GameEngine
from database import init_db

HOST, PORT = '127.0.0.1', 5556
init_db()
engine = GameEngine()
rooms, scores = {}, {}  # room_id -> clients, user -> score

def broadcast(room, message):
    for client in rooms.get(room, []):
        try: client.send(message.encode())
        except: rooms[room].remove(client)

def handle_client(client_socket):
    username = f"user{len(scores)+1}"  # temp usernames
    scores[username] = {"points":0,"streak":0}
    room = "room1"
    rooms.setdefault(room, []).append(client_socket)

    # auto-start round
    puzzle_type, puzzle_data = engine.start_round(room, 1)
    broadcast(room, json.dumps({"event":"new_round","type":puzzle_type,"data":puzzle_data,"timer":20}))
    threading.Thread(target=round_timer,args=(room,20)).start()

    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                data = json.loads(msg)
                if data["action"]=="guess":
                    guess = data["value"]
                    correct = engine.check_guess(room, guess)
                    if correct:
                        pts = 10 + 5 + scores[username]["streak"]*2
                        scores[username]["points"] += pts
                        scores[username]["streak"] += 1
                        broadcast(room,json.dumps({"event":"result","user":username,"guess":guess,"correct":True,"points":pts}))
                        broadcast(room,json.dumps({"event":"leaderboard_update","scores":scores}))
                    else:
                        scores[username]["streak"]=0
                        client_socket.send(json.dumps({"event":"result","user":username,"guess":guess,"correct":False}).encode())
                elif data["action"]=="hint":
                    hint = engine.get_hint(room)
                    scores[username]["points"] -= 3
                    client_socket.send(json.dumps({"event":"hint_update","hint":hint}).encode())
        except: break

def round_timer(room,seconds):
    time.sleep(seconds)
    broadcast(room,json.dumps({"event":"round_end"}))

def start_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,PORT)); server.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT}")
    while True:
        client_socket,_=server.accept()
        threading.Thread(target=handle_client,args=(client_socket,)).start()

if __name__=="__main__": start_server()
