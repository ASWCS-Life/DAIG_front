header = {'key':'dummy'}

def get_auth_header():
    print(header)
    return header['key']

# res["auth"] -> e
def set_auth_header(e):
    header['key'] = e['key']
    print('set header')
    print(header)

