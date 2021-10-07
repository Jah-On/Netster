def main():
    file = open("log.txt", "rb")
    data = file.read()
    file.close
    lines = data.split(b'\n')

    pings = []
    speedtests = []
    date = b''

    for line in range(len(lines)):
        if not (lines[line][:lines[line].find(b'_')] == date):
            pings.clear()
            date = lines[line][:lines[line].find(b'_')]
        if (lines[line][lines[line].find(b'- ') + 2:lines[line].find(b'- ') + 3] == b'('):
            tup = lines[line][lines[line].find(b'- ')+1:].replace(b' ', b'')
            speedtests.append(tup[1:len(tup) - 1])
        else:            
            if (date != b''):
                file = open(date + b'.csv', "ab")
                file.write(str(list(eval(b'[' + lines[line][lines[line].find(b'- ') + 2:] + b']')[0].values())).encode("utf-8")[1:-1].replace(b' ', b'') + b'\n')
                file.close()

    file = open("speed.csv", "ab")
    try:
        file.write(speedtests[0])
        for i in range(1, len(speedtests)):
            file.write(b'\n' + speedtests[i])
    except:
        pass
    file.close()

if __name__ == "__main__":
    main()