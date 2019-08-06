from datetime import datetime

def invalid_author(email, phone):
    aa = 0
    bb = 0
    flag = True
    for c in email:
        if c == '@':
            aa = aa + 1
            flag = False
        if flag == False and c == '.': bb = bb + 1

    if aa != 1 or bb == 0: return True

    aa = 0
    for c in phone: aa = aa + 1
    if aa != 10 or phone[0] != '0': return True
    return False

def invalid_book(isbn, year):
    for c in isbn:
        if not '0' <= c <= '9' and not 'a' <= c <= 'z' and not 'A' <= c <= 'Z': return True

    if year > datetime.now().year: return True
    return False