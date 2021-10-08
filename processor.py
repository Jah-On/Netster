def main():
    file = open("log.txt", "rb")
    data = file.read()
    file.close
    lines = data.split(b'\n')

    speedtests = []
    iphs = []
    date = b''

    for line in range(len(lines)):
        if not (lines[line][:lines[line].find(b'_')] == date):
            if (date != b''):
                f = open(date + b'.csv', "rb")
                data = f.read()
                f.close()
                f = open(date + b'.csv', "wb")
                f.write(b'Time,' + str(iphs)[1:-1].encode("utf-8").replace(b'b\"', b'').replace(b'\"', b'').replace(b' ', b'').replace(b'\'', b'') + b'\n' + data)
                f.close()
                iphs.clear()
            date = lines[line][:lines[line].find(b'_')]
        if (lines[line][lines[line].find(b'- ') + 2:lines[line].find(b'- ') + 3] == b'('):
            tup = lines[line][lines[line].find(b'- ')+1:].replace(b' ', b'')
            speedtests.append(tup[1:len(tup) - 1])
        else:            
            if (date != b''):
                out = lines[line][lines[line].index(b'_') + 1:lines[line].index(b' ')] + b','
                pairs = lines[line][lines[line].index(b'- ') + 3:-1].replace(b' ', b'').split(b',')
                for pair in range(len(pairs)):
                    if (pairs[pair] != b''):
                        keyWithValue = pairs[pair].split(b':')
                        if (keyWithValue[0] not in iphs):
                            iphs.append(keyWithValue[0])
                        out += keyWithValue[1] + b','
                file = open(date + b'.csv', "ab")
                file.write(out[:-1] + b'\n')
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