def get_riddle_features(attempts, solved):
    return {
        "attempts": attempts,
        "solved": int(solved)
    }
