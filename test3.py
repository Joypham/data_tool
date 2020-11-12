if __name__ == "__main__":
    import os
    from core import BASE_DIR,CORE_DIR

    print(BASE_DIR)
    print(CORE_DIR)
    query_path = os.path.join(BASE_DIR, "sources", "query.txt")
    print(query_path)
