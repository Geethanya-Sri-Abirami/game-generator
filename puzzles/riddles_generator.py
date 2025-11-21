import random

RIDDLES = [
    {
        "question": "I speak without a mouth and hear without ears. What am I?",
        "answer": "echo"
    },
    {
        "question": "What gets wetter the more it dries?",
        "answer": "towel"
    },
    {
        "question": "I have keys but no locks. What am I?",
        "answer": "piano"
    },
    {
        "question": "What has to be broken before you can use it?",
        "answer": "egg"
    },
    {
        "question": "What has many teeth but cannot bite?",
        "answer": "comb"
    }
]

def generate_riddle():
    return random.choice(RIDDLES)
