import socket
import csv
import time

# Change IP and Port. MAKE EXCEPTIONS FOR BINDING

# filepath = input('Insert name of the file with sequence: ')
# splitter = input('Insert splitter: ')

filepath = "output.csv"
splitter = ';'

with open(filepath, 'r') as file:
    raw_data = csv.reader(file)
    sequence = []

    for row in raw_data:
        if len(row[0].split(splitter)) != 5:
            print('Wrong format of sequence file')
            exit(1)
        sequence.append(row[0].split(splitter))

seq_dict = []

for i in range(1, len(sequence)):
    _, raw_freq, power, N, dur = sequence[i]
    freq, prr = raw_freq.split(' ')
    prr = prr.strip('()')
    seq_dict.append({'FREQUENCY': freq,
                     'PRR': prr,
                     'POWER': power,
                     'N': N,
                     'DURATION': dur})

try:
    sock = socket.create_connection(("192.168.10.3", 50001))
except:
    print('Can\'t connect to remote server')
    exit(5)


def talk(req):
    try:
        sock.send(req.encode("ascii"))
    except socket.timeout:
        print('Connection timeout, can\'t send request')
        exit(2)

    try:
        ans = sock.recv(1024)
    except socket.timeout:
        print('Connection timeout, don\'t get answer')
        exit(3)

    return ans.decode('ascii')


def check_answer(ans, correct_str):
    ans = ans.strip(':\r\n').split(' ')[1]
    if ans == str(correct_str):
        return True
    else:
        return False


def make_request(ty, req):
    if ty == 'F':
        return 'SPRR ' + req + '\r\n'
    if ty == 'P':
        return 'SSP ' + req + '\r\n'
    if ty == 'N':
        return 'SNB ' + req + '\r\n'


def switch_off():
    # switching off laser
    return 0


def switch_on():
    # switching on laser
    return 0


def retry(ty, req):
    tmp = make_request(ty, req)
    while True:
        ans = talk(tmp)
        if check_answer(ans, req):
            print(tmp + 'OK')
            return 0
        else:
            decision = input('Wrong response, try again? (Y/N) ')
            if decision == 'N':
                switch_off()
                sock.close()
                exit(0)


for task in seq_dict:
    print('Begin task')
    # set frequency
    retry('F', task['FREQUENCY'])

    # set power
    power_lvl = int(round(2.55 * float(task['POWER'])))
    retry('P', str(power_lvl))

    # set number of pulses
    retry('N', str(task['N']))

    # sleep duting duration
    time.sleep(float(task['DURATION']) / 100)

    print('\n\nTask complete')
    print('_' * 100)

sock.close()

input()

