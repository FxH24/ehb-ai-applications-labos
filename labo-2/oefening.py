def naar_llm(antwoord):
    if antwoord ["confidence"] < 0.8:
        return True
    else:
        return False