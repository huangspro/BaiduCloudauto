def get(path):
    with open(path, "r", encoding="utf-8") as f:
        value = f.read().strip()
        if value == "":
            print(f"{path} is empty")
            sys.exit(1)
        return value
