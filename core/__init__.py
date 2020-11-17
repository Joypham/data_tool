import os

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CORE_DIR)
query_path = os.path.join(BASE_DIR, "sources", "query.txt")
credentials_path = os.path.join(BASE_DIR, "sources", "credentials.json")
token_path = os.path.join(BASE_DIR, "sources", "token.pickle")
youtube_com_cookies_path = os.path.join(BASE_DIR, "sources", "youtube_com_cookies.txt")




# if __name__ == "__main__":
#     print(query_path)
#     print(credentials_path)
#     print(token_path)
