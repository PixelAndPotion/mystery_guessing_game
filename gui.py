import tkinter as tk
from threading import Thread
import json

class GameGUI:
    def __init__(self, socket):
        self.socket = socket
        self.root = tk.Tk()
        self.root.title("Mystery Shape / Emoji Pictionary")

        self.timer_label = tk.Label(self.root, text="Time: 0", font=("Arial", 16))
        self.timer_label.pack()

        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack()
        self.guess_button = tk.Button(self.root, text="Submit Guess", command=self.submit_guess)
        self.guess_button.pack()

        self.leaderboard = tk.Label(self.root, text="Leaderboard", justify=tk.LEFT)
        self.leaderboard.pack()

    def submit_guess(self):
        guess = self.guess_entry.get()
        msg = {"action":"guess","value":guess,"room":"room1"}
        self.socket.send(json.dumps(msg).encode())
        self.guess_entry.delete(0, tk.END)

    def start(self):
        Thread(target=self.listen_server, daemon=True).start()
        self.root.mainloop()

    def listen_server(self):
        while True:
            try:
                msg = self.socket.recv(1024).decode()
                if msg:
                    data = json.loads(msg)
                    event = data.get("event")

                    if event == "new_round":
                        self.canvas.delete("all")
                        self.canvas.create_text(200,200,text=f"Puzzle: {data['data']}",font=("Arial",20))

                    elif event == "result":
                        self.leaderboard.config(text=f"Guess: {data['guess']} | Correct: {data['correct']}")

                    elif event == "hint":
                        print("Hint:", data["hint"])
            except:
                break
