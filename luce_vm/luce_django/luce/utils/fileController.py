import ipfshttpclient
from cryptography.fernet import Fernet

client = ipfshttpclient.connect()

def uploadFile(file):
    original_file_content = file.read()
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_file_content = fernet.encrypt(original_file_content)
    #print(encrypted_file_content)
    path = str(file)
    with open(path, 'wb') as f:
        f.write(encrypted_file_content)
    response = __uploadIPFS(path)
    return response, key

def getFile(_hash, key):
    file = __retrieveIPFS(_hash)
    print("file")
    print(file)
    fernet = Fernet(key)
    uncrypted = fernet.decrypt(file)
    print("uncrypted")
    path = str(file)
    with open("tempfile.csv", 'wb') as f:
        f.write(uncrypted)
        return f


def __uploadIPFS(encrypted_file):
    try:
        res = client.add(encrypted_file)
        print(res)
        return res
    except Exception as e:
        print(e)

def __retrieveIPFS(_hash):
    file = client.cat(_hash)
    return file


    
    

    



