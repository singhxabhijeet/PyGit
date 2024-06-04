import sys
import os
import zlib
import hashlib


def hash_object(object_type, file_name):
    with open(file_name, "rb") as file:
        file_content = file.read()

    header = f"blob {len(file_content)}\x00"
    store = header.encode("ascii") + file_content

    sha = hashlib.sha1(store).hexdigest()
    git_path = os.path.join(os.getcwd(), ".git/objects")
    os.mkdir(os.path.join(git_path, sha[0:2]))

    with open(os.path.join(git_path, sha[0:2], sha[2:]), "wb") as file:
        file.write(zlib.compress(store))

    print(sha, end="")

def main():
    
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file":
        if sys.argv[2] == "-p":
            blob_sha = sys.argv[3]
            with open(f".git/objects/{blob_sha[:2]}/{blob_sha[2:]}", "rb") as f:
                raw = zlib.decompress(f.read())
                header, content = raw.split(b"\0", maxsplit=1)
                print(content.decode("utf-8"), end="")
    elif command == "hash-object":
        if len(sys.argv) != 4:
            print("usage: hash-object -w <file>", file=sys.stderr)
            exit()

        object_type = sys.argv[2]
        file_name = sys.argv[3]

        hash_object(object_type, file_name)

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
