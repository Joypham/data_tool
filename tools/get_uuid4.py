import uuid


def get_uuid4():
    for _ in range(0, 1):
        return uuid.uuid4().hex.upper()

if __name__ == "__main__":
    print(get_uuid4())
