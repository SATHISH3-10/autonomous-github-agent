API_CALL_LIMIT = 50
api_calls = 0

def track_api_call():
    global api_calls
    api_calls += 1

    if api_calls > API_CALL_LIMIT:
        raise Exception("Compute budget exceeded")