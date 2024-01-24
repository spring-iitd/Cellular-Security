from pcapng import FileScanner
with open(r'attack-capture.pcapng', 'rb') as fp:
    scanner = FileScanner(fp)
    for block in scanner:
        print(block)
        # print(block._raw) #byte type raw data