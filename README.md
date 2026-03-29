# mystery_guessing_game
A real-time multiplayer guessing game built in python with Tkinter. 
Players connect to a shared room, recieve a puzzle in an emoji or shape and then compete to guess before a timer runs out. Points are awarded based on speed.
Key features include: multiplayer: client-server model, puzzels, a leaderboard and Tkinter GUI.
Project structure: client.py #connects to server and launches GUI, server.py #handles rooms, gui.py #Tkinter interface for puzzels, game_engine.py , utils.py , database.py , game.db #local database file, pycache .
How to run? Start the server. python server.py  . In a new terminal click, python client.py  . This will open multiple clients to test the game and submit guesses. 
Tools include: python, Tkinter and SQLite.
