with open("./temp.txt") as rf:
    with open("./temp_copy.txt") as wf:
        for line in rf:
            wf.write(line)
