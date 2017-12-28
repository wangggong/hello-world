import sys

def classifyLetter(letter):
    if 'A' <= letter <= 'Z':
        return 0
    if 'a' <= letter <= 'z':
        return 1
    if '0' <= letter <= '9':
        return 2
    return 3


def checkPasswd(passwd):
    if len(passwd) <= 8:
        return False
    status, S = [0]*4, set()
    for i, j in enumerate(passwd):
        status[classifyLetter(j)] = 1
        if i < len(passwd) - 2:
            if passwd[i:i + 3] in S:
                return False
            else:
                S.add(passwd[i:i + 3])
    return sum(status) >= 3


if __name__ == '__main__':
    passwd_lines = sys.stdin.readlines()
    for passwd_line in passwd_lines:
        # print passwd_line.strip()
        print 'OK' if checkPasswd(passwd_line.strip()) else 'NG', '\n'
