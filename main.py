import sys
from networking import Player, Host, TEST_HOST, TEST_PORT

def client():
    p = Player()
    p.join(TEST_HOST, TEST_PORT)
    while True:
        print(f"Got Back: {p.send_and_recieve_test()!r}")

def host():
    print("Launching as host...")
    h = Host()
    h.listen()
    while True:
        h.manage_player_connections()

def main():
    pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        main()
    elif sys.argv[1] == "client":
        client()
    elif sys.argv[1] == 'host':
        host()
    else:
        main()