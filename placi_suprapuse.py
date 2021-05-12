import copy
import sys
import os

input_path = sys.argv[1]
output_path = sys.argv[2]
nsol = int(sys.argv[3])
timeout = float(sys.argv[4])

# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        l_g = []
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            l_g.insert(0, nod.g - nod.parinte.g)
            nod = nod.parinte
        l_g.insert(0, 0)
        return l, l_g

    def afisDrum(self, file, nr_maxim):  # returneaza si lungimea drumului
        l, l_g = self.obtineDrum()
        for i in range(len(l)):
            file.write(str(i+1)+")\n")
            file.write(str(l[i]))
            file.write("Cost ultima mutare: " + str(l_g[i]) + "\n\n")
        file.write("Lungime: " + str(len(l)) + "\n")
        file.write("Cost: " + str(self.g) + "\n")
        # TODO: timp gasire solutie
        file.write("Numar maxim de noduri existente la un moment dat in memorie: " + str(nr_maxim) + "\n")
        file.write("Numar total de noduri calculate: " + str(gr.nr_succesori) + "\n")
        return len(l)

    def contineInDrum(self, infoNodNou, costNodNou):
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
        line = ""
        for list in self.info:
            sir += (line.join(list) + '\n')
        return sir


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
        self.nr_succesori = 0

    def testeaza_scop(self, nodCurent):
        for line in nodCurent.info:
            if '*' in line:
                return False
        return True

    # va genera succesorii sub forma de noduri in arborele de parcurgere

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        lengthMatrix = len(nodCurent.info)
        for i in range(0, lengthMatrix):
            # Cred ca poti sa o stergi ca pare ca strica lucruri
            if '*' not in nodCurent.info[i] and not(i > 0 and '*' in nodCurent.info[i - 1]) and not(i < lengthMatrix - 1 and '*' in nodCurent.info[i + 1]):
                continue
            length = len(nodCurent.info[i])
            line = nodCurent.info[i]
            j = 0
            while j < length - 1:
                if line[j] != '.' and line[j] != '*':
                    # k - capatul stang al placii
                    # j - capatul drept al placii
                    k = j
                    # cat timp nu am ajuns la capat si avem o placa
                    while j < length - 1 and line[j] == line[j + 1]:
                        j += 1

                    # daca la stanga avem spatiu
                    if k > 0 and line[k - 1] == '.':
                        infoNodNou = copy.deepcopy(nodCurent.info)
                        newline = line[:]
                        for ind in range(k - 1, j):
                            newline[ind] = newline[ind + 1]
                        newline[j] = '.'
                        valid_move = True
                        drop_ball = False
                        # daca am eliberat spatiu sa cada o bila
                        if i > 0 and nodCurent.info[i - 1][j] == '*':
                            newline_up = nodCurent.info[i - 1][:]
                            # daca nu cade mai mult de un nivel
                            if i < lengthMatrix - 1 and nodCurent.info[i + 1][j] != '.':
                                drop_ball = True
                                newline[j] = '*'
                                newline_up[j] = '.'
                            # daca suntem pe ultimul nivel
                            elif i == lengthMatrix - 1:
                                drop_ball = True
                                newline_up[j] = '.'
                            else:
                                valid_move = False
                            infoNodNou[i - 1] = newline_up[:]
                        infoNodNou[i] = newline[:]
                        # daca matricea obtinuta e valida
                        if valid_move:
                            # print(infoNodNou)
                            valid_move = verify_matrix(infoNodNou, length)
                            # print(line)
                            # print(newline, valid_move)
                        if valid_move:
                            # daca nu am mai ajuns la configuratia asta pana acum
                            if drop_ball:
                                costArc = 1
                            else:
                                costArc = 1 + (j - k + 1)
                            if not nodCurent.contineInDrum(infoNodNou, nodCurent.g + costArc):
                                listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc, self.calculeaza_h(infoNodNou, tip_euristica)))
                                self.nr_succesori += 1
                                # print(infoNodNou)
                                # print_matrix(infoNodNou, g)

                    # daca la stanga avem cel putin o bila
                    if k > 1 and line[k - 1] == '*':
                        infoNodNou = copy.deepcopy(nodCurent.info)
                        newline = line[:]
                        for ind in range(k - 1, j):
                            newline[ind] = newline[ind + 1]
                        newline[j] = '.'
                        valid_move = True
                        drop_ball = False
                        # daca am eliberat spatiu sa cada o bila
                        if i > 0 and nodCurent.info[i - 1][j] == '*':
                            newline_up = nodCurent.info[i - 1][:]
                            # daca nu cade mai mult de un nivel
                            if i < lengthMatrix - 1 and nodCurent.info[i + 1][j] != '.':
                                newline[j] = '*'
                                newline_up[j] = '.'
                                drop_ball = True
                            # daca suntem pe ultimul nivel
                            elif i == lengthMatrix - 1:
                                newline_up[j] = '.'
                                drop_ball = True
                            else:
                                valid_move = False
                            infoNodNou[i - 1] = newline_up[:]
                        # indicele de start al secventei de bile
                        kk = k - 1
                        while kk > 0 and line[kk] == '*':
                            kk -= 1
                        # daca in stanga secventei de bile avem un spatiu (avem loc sa le impingem la stanga)
                        if line[kk] == '.':
                            if i < lengthMatrix - 1:
                                newline_down = nodCurent.info[i + 1][:]
                            for ind_bila in range(kk, k - 1):
                                newline[ind_bila] = '*'
                                # daca nu cade mai mult de un nivel
                                if i < lengthMatrix - 2 and nodCurent.info[i + 1][ind_bila] == '.' and nodCurent.info[i + 2][ind_bila] != '.':
                                    newline_down[ind_bila] = '*'
                                    newline[ind_bila] = '.'
                                    drop_ball = True
                                # daca sunt pe penultimul nivel si poate sa cada pe ultimul nivel
                                elif i == lengthMatrix - 2 and nodCurent.info[i + 1][ind_bila] == '.':
                                    newline[ind_bila] = '.'
                                    drop_ball = True
                                else:
                                    valid_move = False
                            if i < lengthMatrix - 1:
                                infoNodNou[i + 1] = newline_down[:]
                        else:
                            valid_move = False
                        infoNodNou[i] = newline[:]
                        if valid_move:
                            # print(infoNodNou)
                            valid_move = verify_matrix(infoNodNou, length)
                            # print(line)
                            # print(newline, valid_move)
                        if valid_move:

                            if drop_ball:
                                costArc = 1
                            else:
                                costArc = 2 * (1 + (j - k + 1))
                            if not nodCurent.contineInDrum(infoNodNou, nodCurent.g + costArc):
                                listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc, self.calculeaza_h(infoNodNou, tip_euristica)))
                                self.nr_succesori += 1
                                # print(infoNodNou)
                                # print_matrix(infoNodNou, g)

                    # daca la dreapta avem spatiu
                    if j < length - 1 and line[j + 1] == '.':
                        infoNodNou = copy.deepcopy(nodCurent.info)
                        newline = line[:]
                        for ind in range(j + 1, k, -1):
                            newline[ind] = newline[ind - 1]
                        newline[k] = '.'
                        valid_move = True
                        drop_ball = False
                        # daca am eliberat spatiu sa cada o bila
                        if i > 0 and nodCurent.info[i - 1][k] == '*':
                            newline_up = nodCurent.info[i - 1][:]
                            # daca nu cade mai mult de un nivel
                            if i < lengthMatrix - 1 and nodCurent.info[i + 1][k] != '.':
                                newline[k] = '*'
                                newline_up[k] = '.'
                                drop_ball = True
                            # daca suntem pe ultimul nivel
                            elif i == lengthMatrix - 1:
                                newline_up[k] = '.'
                                drop_ball = True
                            else:
                                valid_move = False
                            infoNodNou[i - 1] = newline_up[:]
                        infoNodNou[i] = newline[:]
                        # daca matricea obtinuta e valida
                        if valid_move:
                            # print(infoNodNou)
                            valid_move = verify_matrix(infoNodNou, length)
                            # print(line)
                            # print(newline, valid_move)
                        if valid_move:
                            if drop_ball:
                                costArc = 1
                            else:
                                costArc = 1 + (j - k + 1)
                            # daca nu am mai ajuns la configuratia asta pana acum
                            if not nodCurent.contineInDrum(infoNodNou, nodCurent.g + costArc):
                                listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc, self.calculeaza_h(infoNodNou, tip_euristica)))
                                self.nr_succesori += 1
                                # print(infoNodNou)
                                # print_matrix(infoNodNou, g)
                    # daca la dreapta avem cel putin o bila
                    if j < length - 2 and line[j + 1] == '*':
                        infoNodNou = copy.deepcopy(nodCurent.info)
                        newline = line[:]
                        for ind in range(j + 1, k, -1):
                            newline[ind] = newline[ind - 1]
                        newline[k] = '.'
                        valid_move = True
                        drop_ball = False
                        # daca am eliberat spatiu sa cada o bila
                        if i > 0 and nodCurent.info[i - 1][k] == '*':
                            newline_up = nodCurent.info[i - 1][:]
                            # daca nu cade mai mult de un nivel
                            if i < lengthMatrix - 1 and nodCurent.info[i + 1][k] != '.':
                                newline[k] = '*'
                                newline_up[k] = '.'
                                drop_ball = True
                            # daca suntem pe ultimul nivel
                            elif i == lengthMatrix - 1:
                                newline_up[k] = '.'
                                drop_ball = True
                            else:
                                valid_move = False
                            infoNodNou[i - 1] = newline_up[:]
                        # indicele de start al secventei de bile
                        jj = j + 1
                        while jj < length - 1 and line[jj] == '*':
                            jj += 1
                        # daca in dreapta secventei de bile avem un spatiu (avem loc sa le impingem la dreapta)
                        if line[jj] == '.':
                            if i < lengthMatrix - 1:
                                newline_down = nodCurent.info[i + 1][:]
                            for ind_bila in range(j + 2, jj + 1):
                                newline[ind_bila] = '*'
                                # daca nu cade mai mult de un nivel
                                if i < lengthMatrix - 2 and nodCurent.info[i + 1][ind_bila] == '.' and \
                                        nodCurent.info[i + 2][ind_bila] != '.':
                                    newline_down[ind_bila] = '*'
                                    newline[ind_bila] = '.'
                                    drop_ball = True
                                # daca sunt pe penultimul nivel si poate sa cada pe ultimul nivel
                                elif i == lengthMatrix - 2 and nodCurent.info[i + 1][ind_bila] == '.':
                                    newline[ind_bila] = '.'
                                    drop_ball = True
                                else:
                                    #print(newline)
                                    #print(newline_down)
                                    #print("\n")
                                    valid_move = False
                            if i < lengthMatrix - 1:
                                infoNodNou[i + 1] = newline_down[:]
                        else:
                            valid_move = False
                        infoNodNou[i] = newline[:]
                        if valid_move:
                            # print(infoNodNou)
                            valid_move = verify_matrix(infoNodNou, length)
                            # print(line)
                            # print(newline, valid_move)
                        if valid_move:
                            if drop_ball:
                                costArc = 1
                            else:
                                costArc = 2 * (1 + (j - k + 1))
                            if not nodCurent.contineInDrum(infoNodNou, nodCurent.g + costArc):
                                listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc, self.calculeaza_h(infoNodNou, tip_euristica)))
                                self.nr_succesori += 1
                                # print(infoNodNou)
                                # print_matrix(infoNodNou, g)
                j += 1
        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica == "euristica banala":
            for line in infoNod:
                if '*' in line:
                    return 1  # minimul dintre costurile tuturor arcelor
            return 0
        elif tip_euristica == "euristica admisibila 1":
            # calculez cate bile mai am in matrice
            nr_balls = 0
            for line in infoNod:
                for x in line:
                    if '*' == x:
                        nr_balls += 1
            return nr_balls
        elif tip_euristica == "euristica admisibila 2":
            # calculez cate bile mai am in matrice si cate linii mai am pana dispar(ajung pe ultima linie)
            # exista si mutari care pot sa coboare 2 bile in acelasi timp, asa ca de fiecare data cand calculam inaltimea unei bile, scadem 1
            steps = 0
            diff = 0
            for i in range(len(infoNod)):
                for x in infoNod[i]:
                    if '*' == x:
                        steps += len(infoNod) - i
                        diff += 1
            return steps - diff if diff > 1 else steps
        '''
        elif tip_euristica == "euristica neadmisibila":
            # calculez cate blocuri nu sunt la locul fata de fiecare dintre starile scop, si apoi iau minimul dintre aceste valori
            euristici = []
            for (iScop, scop) in enumerate(self.scopuri):  # scop e o stare scop
                h = 0
                for iStiva, stiva in enumerate(infoNod):
                    for iElem, elem in enumerate(stiva):
                        try:
                            # exista în stiva scop indicele iElem dar pe acea pozitie nu se afla blocul din infoNod
                            if elem != scop[iStiva][iElem]:
                                h += 1
                        except IndexError:
                            # nici macar nu exista pozitia iElem in stiva cu indicele iStiva din scop
                            h += 2
                euristici.append(h)
            return min(euristici)
        '''
    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    if verify_matrix(gr.start, len(gr.start[0])):
        c = [NodParcurgere(gr.start, None, 0)]
    else:
        g.write("Input invalid\n")
        return
    # print("Coada: " + str(c))
    nr_maxim_noduri = 1
    nr_succesori = 0
    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        if len(c) > nr_maxim_noduri:
            nr_maxim_noduri = len(c)
        nodCurent = c.pop(0)
        # print_matrix(nodCurent.info, g)
        # print(verify_matrix(nodCurent.info, len(nodCurent.info)))
        if gr.testeaza_scop(nodCurent):
            nodCurent.afisDrum(g, nr_maxim_noduri)
            g.write("\n----------------\n")
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


def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    if verify_matrix(gr.start, len(gr.start[0])):
        c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    else:
        g.write("Input invalid\n")
        return
    # print("Coada: " + str(c))
    nr_maxim_noduri = 1
    nr_succesori = 0
    while len(c) > 0:
        # print("Coada actuala: " + str(c))
        # input()
        if len(c) > nr_maxim_noduri:
            nr_maxim_noduri = len(c)
        nodCurent = c.pop(0)
        # print_matrix(nodCurent.info, g)
        # print(verify_matrix(nodCurent.info, len(nodCurent.info)))
        if gr.testeaza_scop(nodCurent):
            nodCurent.afisDrum(g, nr_maxim_noduri)
            g.write("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def verify_matrix(matrix, length):
    if length == 0:
        return False
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


def print_matrix(matrix, file):
    line = ""
    for list in matrix:
        file.write(line.join(list) + '\n')
    file.write('\n')


if not os.path.exists(output_path):
    os.mkdir(output_path)
for numeFisier in os.listdir(input_path):
    numeFisierOutput = "output_" + numeFisier
    print(numeFisier, "--->", numeFisierOutput)
    g = open(output_path + "/" + numeFisierOutput, "w")
    gr = Graph(input_path + "/" + numeFisier)
    #uniform_cost(gr, nrSolutiiCautate=nsol)
    #a_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica banala")
    #a_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica admisibila 1")
    a_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica admisibila 2")
    g.close()


