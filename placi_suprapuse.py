import copy
import sys
import os

input_path = sys.argv[1]
output_path = sys.argv[2]
nsol = int(sys.argv[3])
timeout = float(sys.argv[4])
'''
print(input_path)
print(output_path)
print(nsol)
print(timeout)
'''



# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, info, parinte, cost=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            print(str(nod))
        if afisCost:
            print("Cost: ", self.g)
        if afisLung:
            print("Lungime: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:

            if infoNodNou == nodDrum.info:
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return sir

    def __str__(self):
        sir = ""
        maxInalt = max([len(stiva) for stiva in self.info])
        for inalt in range(maxInalt, 0, -1):
            for stiva in self.info:
                if len(stiva) < inalt:
                    sir += "  "
                else:
                    sir += stiva[inalt - 1] + " "
            sir += "\n"
        sir += "-" * (2 * len(self.info) - 1)
        return sir

    """
    def __str__(self):
        sir=""
        for stiva in self.info:
            sir+=(str(stiva))+"\n"
        sir+="--------------\n"
        return sir
    """


class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        '''
        def obtineStive(sir):
            stiveSiruri = sir.strip().split("\n")
            listaStive = [sirStiva.strip().split() if sirStiva != "#" else [] for sirStiva in stiveSiruri]
            return listaStive

        f = open(nume_fisier, 'r')

        continutFisier = f.read()
        siruriStari = continutFisier.split("stari_finale")
        self.start = obtineStive(siruriStari[0])  # stare initiala
        self.scopuri = []
        siruriStariFinale = siruriStari[1].strip().split("---")
        for scop in siruriStariFinale:
            self.scopuri.append(obtineStive(scop))
        print("Stare Initiala:", self.start)
        print("Stari finale posibile:", self.scopuri)
        input()
        '''
        f = open(nume_fisier)
        line = f.readline()
        n = int(len(line)) - 1
        m = [list(line)[:n]]
        for line in f.readlines():
            m.append(list(line)[:n])
        f.close()
        self.start = m

    def testeaza_scop(self, nodCurent):
        for line in nodCurent.info:
            if '*' in line:
                return False
        return True

    # va genera succesorii sub forma de noduri in arborele de parcurgere

    def genereazaSuccesori(self, nodCurent):
        listaSuccesori = []
        lengthMatrix = len(nodCurent.info)
        for i in range(0, lengthMatrix):
            if '*' not in nodCurent.info[i] and not(i > 1 and '*' not in nodCurent.info[i-1]):
                continue
            length = len(nodCurent.info[i])
            line = nodCurent.info[i]
            j = 0
            while j < length-1:
                k = j
                # cat timp nu am ajuns la capat si avem o placa
                while j < length-1 and line[j] == line[j+1] and (line[j] != '.' or line[j] != '*'):
                    j += 1
                # daca la stanga avem spatiu
                if k > 0 and line[k-1] == '.':
                    newline = line[:]
                    for ind in range(k-1, j):
                        newline[ind] = newline[ind + 1]
                    newline[j] = '.'
                    valid_move = True
                    if i > 0 and nodCurent.info[i-1][j] == '*':
                        if i < lengthMatrix - 1 and nodCurent.info[i+1][j] != '.':
                            newline[j] = '*'
                        else:
                            valid_move = False
                    infoNodNou = copy.deepcopy(nodCurent.info)
                    infoNodNou[i] = newline[:]
                    if valid_move:
                        # print(infoNodNou)
                        valid_move = verify_matrix(infoNodNou, length)
                        # print(line)
                        # print(newline, valid_move)
                    if valid_move:
                        if not nodCurent.contineInDrum(infoNodNou):
                            costArc = 1
                            listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc))
                            # print(infoNodNou)
                            # print_matrix(infoNodNou, g)
                # TODO: Mai multe bile in sir
                # daca la stanga avem bila
                if k > 1 and line[k - 1] == '*':
                    newline = line[:]
                    for ind in range(k - 1, j):
                        newline[ind] = newline[ind + 1]
                    newline[j] = '.'
                    valid_move = True
                    if i > 0 and nodCurent.info[i - 1][j] == '*':
                        if i < lengthMatrix - 1 and nodCurent.info[i + 1][j] != '.':
                            newline[j] = '*'
                        else:
                            valid_move = False
                    infoNodNou = copy.deepcopy(nodCurent.info)
                    infoNodNou[i] = newline[:]
                    if valid_move:
                        # print(infoNodNou)
                        valid_move = verify_matrix(infoNodNou, length)
                        # print(line)
                        # print(newline, valid_move)
                    if valid_move:
                        if not nodCurent.contineInDrum(infoNodNou):
                            costArc = 1
                            listaSuccesori.append(
                                NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc))
                            # print(infoNodNou)
                            # print_matrix(infoNodNou, g)
                j += 1

        '''
        rangeStive = range(len(nodCurent.info))
        # nodCurent.info
        for i in rangeStive:
            if len(nodCurent.info[i]) == 0:
                continue
            copieStive = copy.deepcopy(nodCurent.info)
            bloc = copieStive[i].pop()  # sterge si returneaza ultimul element din lista
            for j in rangeStive:
                if i == j:
                    continue
                infoNodNou = copy.deepcopy(copieStive)
                infoNodNou[j].append(bloc)
                if not nodCurent.contineInDrum(infoNodNou):
                    costArc = 1
                    listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc))
        '''
        return listaSuccesori

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, 0)]
    print("Coada: " + str(c))
    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            print("Solutie: ")
            nodCurent.afisDrum(True, True)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)






def verify_matrix(matrix, length):
    for (poz, line) in enumerate(matrix):
        if length != len(line):
            # print(length, len(line))
            return False
        # daca nu suntem pe ultima linie
        if poz != len(matrix) - 1:
            i = 0
            while i < length-1:
                # presupunem ca placa e in aer
                floating = True
                # cat timp nu am ajuns la capat, avem o secventa si nu suntem siguri ca nu e in aer
                while i < length-1 and line[i] == line[i+1] and floating:
                    # print(line[i])
                    # daca sub ea nu e un gol continuu sau ea insasi e un gol
                    if matrix[poz+1][i] != '.' or line[i] == '.':
                        floating = False
                    i += 1
                # print(line[i])
                if matrix[poz + 1][i] != '.' or line[i] == '.':
                    floating = False
                if floating:
                    # print(line)
                    return False
                i += 1
    return True


# def verify_line(line1, line2, length): in caz ca am nevoie


def print_matrix(matrix, file):
    line = ""
    for list in matrix:
        file.write(line.join(list) + '\n')
    file.write('\n')

# creez fisiere de output pentru fiecare fisier de input din folder_input_2

# verific daca nu există folderul folder_output, caz în care îl creez
if not os.path.exists(output_path):
    os.mkdir(output_path)
for numeFisier in os.listdir(input_path):
    # pentru fiecare fisier de input cu numele fisier.txt (unde fisier e un nume generic, ca o variabila nu textul "fisier" in sine) fac un fisier de output, denumit output_fisier.txt
    numeFisierOutput = "output_" + numeFisier


    '''
    f=open(input_path + "/" + numeFisier)
    line = f.readline()
    n = int(len(line))-1
    m = [list(line)[:n]]
    for line in f.readlines():
        m.append(list(line)[:n])
    f.close()



    print(verify_matrix(m, n))
    '''
    print(numeFisier, "--->", numeFisierOutput)
    # ca sa îmi creeze fișierul în folder_output, îl concatenez la numele fișierului având astfel o cale relativă la folderul în care se află programul main.py
    g = open(output_path + "/" + numeFisierOutput, "w")
    # print_matrix(m, g)
    gr = Graph(input_path + "/" + numeFisier)
    uniform_cost(gr, nrSolutiiCautate=nsol)
    g.close()


