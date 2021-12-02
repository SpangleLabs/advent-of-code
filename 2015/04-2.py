import hashlib

if __name__ == "__main__":
    num = 0
    while True:
        hash_str = "ckczppom" + str(num)
        result = hashlib.md5(hash_str.encode())
        if result.hexdigest().startswith("000000"):
            print(num)
            break
        num += 1

