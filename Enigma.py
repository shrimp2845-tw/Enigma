import random as rd
import ast
import os
dir=os.getcwd()
class rotors():
    def __init__(self,rotor,offset):
        self.offset=offset
        for i in range(offset):
            rotor.insert(0,rotor.pop())
        self.rotor=rotor
    def left(self,node):
        while node<=-len(self.rotor):
            node-=-len(self.rotor)
        node+=self.rotor[node][1]
        return node
    def right(self,node):
        while node<=-len(self.rotor):
            node-=-len(self.rotor)
        node+=self.rotor[node][0]
        return node
    def shift(self):
        self.offset=(self.offset + 1) % len(self.rotor)
        self.rotor.insert(0, self.rotor.pop())
    def get_offset(self):
        alphalist=[chr(i) for i in range(97,97+len(self.rotor))]
        return (alphalist[self.offset])
    @staticmethod
    def randrotor(n):
        nodes=list(range(n))
        spinwheel=[[1, 1] for i in range(n)]
        for i in range(n):
            node=rd.choice(nodes)
            nodes.remove(node)
            move1=node-i
            if move1>0:
                move1=move1-n
            spinwheel[i][1]=move1
            spinwheel[i+move1][0]=-n-move1
        return spinwheel


class plugboards():
    def __init__(self,l):
        self.plugboard={}
        for i in l:
            self.plugboard[i[0]]=i[1]
            self.plugboard[i[1]]=i[0]
    @staticmethod
    def randplugboard(n,m):
        if n//2>13:
            return None
        lines=[]
        nodes = [chr(j) for j in range(97, 97+n)]
        for i in range(m):
            line=rd.sample(nodes,k=2)
            lines.append(line)
            for j in line:
                nodes.remove(j)
        return lines
    def pluged(self,alpha):
        changedalpha=self.plugboard.get(alpha)
        if changedalpha:
            return changedalpha
        return alpha


class reflectors():
    def __init__(self,l):
        self.reflector=l
    @staticmethod
    def randreflector(n):
        if n//2>13:
            return None
        lines=[]
        nodes=[j for j in range(0,n)]
        for i in range(n//2):
            line=rd.sample(nodes,k=2)
            lines.append(line)
            for j in line:
                nodes.remove(j)
        return lines
    def reflect(self,node):
        while node<0:
            node=len(self.reflector*2)-abs(node)
        for i in self.reflector:
            if node in i:
                return i[i.index(node)-1]


def randsetup(filename):
    global dir
    setup=[]
    for i in range(3):
        setup.append(rotors.randrotor(26))
    setup.append(reflectors.randreflector(26))
    setup.append(plugboards.randplugboard(26,6))
    path=fr'{dir}\data\{filename}.txt'
    setupfile=open(path,"w")
    setupfile.write(str(setup))
    setupfile.close()
    print("success")


def readsetup(filename):
    global dir
    path=fr'{dir}\data\{filename}.txt'
    setupfile=open(path,'r')
    data=ast.literal_eval(setupfile.read())
    setupfile.close()
    return data


def originalengima():
    global dir
    filename=input('Please enter your setup file name:')
    path=fr'{dir}\data\{filename}.txt'
    print(f'Please check the path:{path}')
    if not os.path.exists(path):
        print("File does not exist")
    else:
        setup=readsetup(filename)
        rotor1,rotor2,rotor3,reflector,plugboard=setup
        offset3,offset2,offset1=[ord(i)-97 for i in input("Please enter 3 offset for rotor(such as abc,mei,qaq):")]
        rotor1=rotors(rotor1,offset1)
        rotor2=rotors(rotor2,offset2)
        rotor3=rotors(rotor3,offset3)
        reflector=reflectors(reflector)
        plugboard=plugboards(plugboard)
        print('Setup done!')
        text=input('Please enter your text,only lower-case english character will be encrypted:')
        encrypttext=''
        count=0
        len_rotor=len(rotor1.rotor)
        for i in text:
            alphalist = [chr(j) for j in range(97, 97+len_rotor)]
            if i not in alphalist:
                encrypttext+=i
            else:
                step1=plugboard.pluged(i)
                step2=rotor1.right(rotor2.right(rotor3.right(reflector.reflect(rotor3.left(rotor2.left(rotor1.left(ord(step1)-97)))))))
                while step2<0:
                    step2+=len_rotor
                step3=chr(97+step2)
                step4=plugboard.pluged(step3)
                encrypttext+=step4
            count+=1
            rotor1.shift()
            if count%len_rotor==0:
                rotor2.shift()
            if count%(len_rotor*len_rotor)==0:
                rotor3.shift()
        print('Here is encrypted text:')
        print(encrypttext)


def main():
    originalengima()
    input("----------press enter to exit----------")


if __name__ == '__main__':
    main()
