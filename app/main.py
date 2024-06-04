import sys
import os
import zlib
import hashlib


#def hash_object(object_type, file_name):
 #   with open(file_name, "rb") as file:
  #      file_content = file.read()

   # header = f"blob {len(file_content)}\x00"
    #store = header.encode("ascii") + file_content

    #ha = hashlib.sha1(store).hexdigest()
    #git_path = os.path.join(os.getcwd(), ".git/objects")
    #os.mkdir(os.path.join(git_path, sha[0:2]))

    #with open(os.path.join(git_path, sha[0:2], sha[2:]), "wb") as file:
     #   file.write(zlib.compress(store))

    #print(sha, end="")

#elif command == "hash-object":
 #       if len(sys.argv) != 4:
  #          print("usage: hash-object -w <file>", file=sys.stderr)
   #         exit()

    #    object_type = sys.argv[2]
     #   file_name = sys.argv[3]

      #  hash_object(object_type, file_name)

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
        if sys.argv[2] == "-w":
            file = sys.argv[3]
            with open(file, "rb") as f:
                data = f.read()
                header = f"blob {len(data)}\0".encode("utf-8")
                store = header + data
                sha = hashlib.sha1(store).hexdigest()
                os.makedirs(f".git/objects/{sha[:2]}", exist_ok=True)
                with open(f".git/objects/{sha[:2]}/{sha[2:]}", "wb") as f:
                    f.write(zlib.compress(store))
                    print(sha)

    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
