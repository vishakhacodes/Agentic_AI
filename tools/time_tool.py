from datetime import datetime

def execute(argument: dict):
    now = datetime.now()
    return now.strftime("%d-%m-%Y %I:%M:%S %p")

if __name__ == "__main__":
    print("Time tool \n")
    print(execute({}))