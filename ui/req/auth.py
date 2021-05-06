global header
header = {}

def get_auth_header():
    print(header)
    return header

# res["auth"]["key"] -> e
def set_auth_header(e):
    global header
    header = {
        "AUTH" : e
    }
