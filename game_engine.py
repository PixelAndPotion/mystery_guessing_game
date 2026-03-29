import random
from utils import generate_shape, generate_emoji_puzzle

class GameEngine:
    def __init__(self): self.rooms={}
    def start_round(self,room_id,round_number):
        puzzle_type=random.choice(['shape','emoji'])
        puzzle_data=generate_shape() if puzzle_type=='shape' else generate_emoji_puzzle()
        self.rooms[room_id]={"round_number":round_number,"puzzle_data":puzzle_data}
        return puzzle_type,puzzle_data
    def check_guess(self,room_id,guess):
        current=self.rooms.get(room_id); return current and guess.lower()==current['puzzle_data'].lower()
    def get_hint(self,room_id):
        current=self.rooms.get(room_id); return "Starts with: "+current['puzzle_data'][0] if current else "No round"
