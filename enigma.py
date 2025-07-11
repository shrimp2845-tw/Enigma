import random as rd


class Rotors:
    def __init__(self, rotor, offset):
        self.offset = offset % len(rotor)
        for i in range(offset):
            rotor.insert(0, rotor.pop())
        self.rotor = rotor

    def left(self, node):
        while node <= -len(self.rotor):
            node -= -len(self.rotor)
        node += self.rotor[node][1]
        return node

    def right(self, node):
        while node <= -len(self.rotor):
            node -= -len(self.rotor)
        node += self.rotor[node][0]
        return node

    def shift(self):
        self.offset = (self.offset + 1) % len(self.rotor)
        self.rotor.insert(0, self.rotor.pop())

    def get_offset(self):
        alphalist = [chr(i) for i in range(97, 97 + len(self.rotor))]
        return alphalist[self.offset]

    @staticmethod
    def randrotor(n):
        nodes = list(range(n))
        spinwheel = [[1, 1] for i in range(n)]
        for i in range(n):
            node = rd.choice(nodes)
            nodes.remove(node)
            move1 = node - i
            if move1 > 0:
                move1 = move1 - n
            spinwheel[i][1] = move1
            spinwheel[i + move1][0] = -n - move1
        return spinwheel


class Plugboards:
    def __init__(self, l):
        self.plugboard = {}
        for i in l:
            self.plugboard[i[0]] = i[1]
            self.plugboard[i[1]] = i[0]

    @staticmethod
    def randplugboard(n, m):
        lines = []
        nodes = [chr(j) for j in range(97, 97 + n)]
        for i in range(m):
            line = rd.sample(nodes, k=2)
            lines.append(line)
            for j in line:
                nodes.remove(j)
        return lines

    def pluged(self, alpha):
        changedalpha = self.plugboard.get(alpha)
        if changedalpha:
            return changedalpha
        return alpha


class Reflectors:
    def __init__(self, l):
        self.reflector = l

    @staticmethod
    def randreflector(n):
        lines = []
        nodes = [j for j in range(0, n)]
        for i in range(n // 2):
            line = rd.sample(nodes, k=2)
            lines.append(line)
            for j in line:
                nodes.remove(j)
        return lines

    def reflect(self, node):
        while node < 0:
            node = len(self.reflector * 2) - abs(node)
        for i in self.reflector:
            if node in i:
                return i[i.index(node) - 1]
