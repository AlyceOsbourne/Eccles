if __name__ == "__main__":
    from main import docs, __todo__

    print("Attempting to create wiki")

    path = "C:\\Users\\Alyce\\PycharmProjects\\Eccles.wiki\\"

    with open(path + "ECS.md", 'w') as f:
        f.write(docs())

    with open(path + "TODO.md", 'w') as f:
        f.write(__todo__)

    print("Wiki created")
