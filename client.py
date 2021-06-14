import xmlrpc.client
import time


server_ip = input("server ip\t: ")
server_port = input("server port\t: ")

server = xmlrpc.client.Server(f'http://{server_ip}:{server_port}')


class Game:
    def __init__(self, server):
        self.server = server
        self.login(self.server.unavailablePawn())
        print("=======================")
        self.waitingForEnemy()
        print("=======================")
        print(f"your pawn is {self.my_pawn}")
        print(f"enemy's pawn is {self.enemy_pawn}")
        print("=======================")

    def login(self, unavailablePawn):
        while True:
            if unavailablePawn is None:
                pawn = input("type pawn : ")
                if len(pawn) == 1:
                    break
            else:
                pawn = input(
                    f"type pawn ({unavailablePawn} is not available) : ")
                if len(pawn) == 1 and pawn != unavailablePawn:
                    break

        self.my_pawn = pawn
        self.my_index = self.server.login(pawn)

    def waitingForEnemy(self):
        while True:
            print("waiting for enemy...")
            if self.server.isFull():
                break
            time.sleep(1)

        self.enemy_pawn = self.server.getEnemyPawn(self.my_index)
        print(f"enemy is founded")

    def board(self):
        self.datas = self.server.getDatas()
        def bracket(x): return f"[{x}]"

        print("    0  1  2")
        for idx, data in enumerate(self.datas):
            d = "".join([bracket(x) for x in data])
            print("{}: {}".format(idx, d))

    def play(self):
        while not self.server.dataIsFull() and not self.server.isThereWinner() and not server.isThereAfk():
            if self.server.isMyTurn(self.my_index):
                print("\n"*10)
                self.board()
                print("=======================")

                while True:
                    try:
                        row, col = input("fill (row col) : ").split()
                        row, col = int(row), int(col)

                        if self.datas[row][col] == " ":
                            break
                    except:
                        continue

                self.server.fill(self.my_index, row, col)
                print("=======================")
            else:
                print("enemy turn...")
                time.sleep(1)

        if self.server.isMyTurn(self.my_index):
            print("=======================")

        if server.isThereAfk():
            print("Enemy is AFK")
            print("=======================")

    def printWinner(self):
        if self.server.isThereWinner():
            if self.server.isWin(self.my_index):
                print("!!!...VICTORY...!!!")
            else:
                print("!!!...DEFEAT...!!!")
        else:
            print("!!!...DRAW...!!!")


if not server.isFull():
    print("\n"*10)
    game = Game(server)

    try:
        game.play()
        game.printWinner()

        time.sleep(3)
        game.quit()
    except:
        server.quit()
else:
    print("game is full")
    print("please wait for a minute")
