import ast
import os
from enigma import Reflectors, Rotors, Plugboards

dir = os.path.dirname(os.path.abspath(__file__))

def randsetup(filename):
    global dir
    os.makedirs(f"{dir}/data", exist_ok=True)
    setup = []
    for i in range(3):
        setup.append(Rotors.randrotor(26))
    setup.append(Reflectors.randreflector(26))
    setup.append(Plugboards.randplugboard(26, 6))
    path = f'{dir}/data/{filename}.txt'
    setupfile = open(path, "w")
    setupfile.write(str(setup))
    setupfile.close()
    print("success")


def readsetup(filename):
    global dir
    os.makedirs(f"{dir}/data", exist_ok=True)
    path = f'{dir}/data/{filename}.txt'
    setupfile = open(path, 'r')
    data = ast.literal_eval(setupfile.read())
    setupfile.close()
    return data


def originalengima():
    global dir
    os.makedirs(f"{dir}/data", exist_ok=True)
    filename = input('Please enter your setup file name:')
    path = f'{dir}/data/{filename}.txt'
    print(f'Please check the path:{path}')
    if not os.path.exists(path):
        print("File does not exist")
    else:
        setup = readsetup(filename)
        rotor1, rotor2, rotor3, reflector, plugboard = setup
        offset3, offset2, offset1 = [ord(i.lower()) - 97 for i in input("Please enter 3 offset,case doesn't matter(such as ABC,MEI,QAQ):")]
        rotor1 = Rotors(rotor1, offset1)
        rotor2 = Rotors(rotor2, offset2)
        rotor3 = Rotors(rotor3, offset3)
        reflector = Reflectors(reflector)
        plugboard = Plugboards(plugboard)
        print('Setup done!')
        print('Please enter your text below,only lower-case english character will be encrypted,Multiline input allowed,empty row finished input:')
        lines = []
        while True:
            line = input()
            if line == '':
                break
            lines.append(line)
        text = '\n'.join(lines)
        encrypttext = ''
        count = 0
        len_rotor = len(rotor1.rotor)
        for i in text:
            alphalist = [chr(j) for j in range(97, 97 + len_rotor)]
            if i not in alphalist:
                encrypttext += i
            else:
                step1 = plugboard.pluged(i)
                step2 = rotor1.right(rotor2.right(rotor3.right(reflector.reflect(rotor3.left(rotor2.left(rotor1.left(ord(step1) - 97)))))))
                while step2 < 0:
                    step2 += len_rotor
                step3 = chr(97 + step2)
                step4 = plugboard.pluged(step3)
                encrypttext += step4
                count += 1
                rotor1.shift()
                if count % len_rotor == 0:
                    rotor2.shift()
                if count % (len_rotor * len_rotor) == 0:
                    rotor3.shift()
        print('Here is encrypted text:')
        print(encrypttext)


def main():
    try:
        originalengima()
    except Exception as e:
        print('ERROR:', e)
    finally:
        input('----------Press enter to exit----------')


if __name__ == '__main__':
    main()
