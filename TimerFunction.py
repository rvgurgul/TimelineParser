from datetime import datetime

def time_a_function(func):
    a = datetime.now()
    func()
    b = datetime.now()
    d = b - a
    print(f"Function took {d}")
    return d
