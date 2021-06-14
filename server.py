import numpy as np
from requests import get
from xmlrpc.server import SimpleXMLRPCServer

port = int(input("port : "))
print("\n"*10)

with SimpleXMLRPCServer(("0.0.0.0", port), logRequests=False, allow_none=True) as server:
    server.register_introspection_functions()

    class TicTacToe:
        def __init__(self, port):
            self.public_ip = get('https://api.ipify.org').text
            self.port = port

            self.reset()

            print(f"PUBLIC IP\t: {self.public_ip}")
            print(f"PORT\t\t: {self.port}")

        def reset(self):
            self.pawns = []
            self.datas = np.full((3, 3), -1)
            self.turn = 0

        def isFull(self):
            return len(self.pawns) >= 2

        def unavailablePawn(self):
            try:
                return self.pawns[0]
            except:
                return None

        def login(self, pawn):
            index = len(self.pawns)
            self.pawns.append(pawn)
            print(f"INDEX {index} LOGIN WITH PAWN {pawn}")
            return index

        def isMyTurn(self, my_index):
            return self.turn == my_index

        def getEnemyIndex(self, my_index):
            if my_index == 0:
                return 1
            return 0

        def getEnemyPawn(self, my_index):
            return self.pawns[self.getEnemyIndex(my_index)]

        def getDatas(self):
            def value(x): return " " if x == -1 else self.pawns[x]
            return [[value(x) for x in data] for data in self.datas]

        def dataIsFull(self):
            for data in self.datas:
                for x in data:
                    if x == -1:
                        return False
            return True

        def fill(self, my_index, row, col):
            self.turn = self.getEnemyIndex(my_index)
            self.datas[row][col] = my_index

        def isWin(self, my_index):
            for i in range(3):
                if np.all(self.datas[i] == my_index):
                    return True

            for i in range(3):
                if np.all(self.datas[:, i] == my_index):
                    return True

            if np.all(np.diag(self.datas) == my_index):
                return True

            if np.all(np.diag(self.datas[:, ::-1]) == my_index):
                return True

            return False

        def isThereWinner(self):
            for i in range(2):
                if self.isWin(i):
                    return True
            return False

        def isThereAfk(self):
            return len(self.pawns) < 2

        def quit(self):
            print("RESETING...")

            self.reset()

            print(f"PUBLIC IP\t: {self.public_ip}")
            print(f"PORT\t\t: {self.port}")

    server.register_instance(TicTacToe(port))
    server.serve_forever()
