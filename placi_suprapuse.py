import copy
import sys
import os
import time

input_path = sys.argv[1]
output_path = sys.argv[2]
nsol = int(sys.argv[3])
timeout = float(sys.argv[4])

t1 = time.time()


class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte
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

    def afisDrum(self, file, nr_maxim):
        l, l_g = self.obtineDrum()
        for i in range(len(l)):
            file.write(str(i+1)+")\n")
            file.write(str(l[i]))
            file.write("Cost ultima mutare: " + str(l_g[i]) + "\n\n")
        file.write("Lungime: " + str(len(l)) + "\n")
        file.write("Cost: " + str(self.g) + "\n")
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        file.write("Timp: " + str(milis) + " milisecunde\n")
        file.write("Numar maxim de noduri existente la un moment dat in memorie: " + str(nr_maxim) + "\n")
        file.write("Numar total de noduri calculate: " + str(gr.nr_succesori) + "\n")
        g.write("\n----------------\n")
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
        line = ""
        for list in self.info:
            sir += (line.join(list) + '\n')
        return sir


class Graph:
    def __init__(self, nume_fisier):
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

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        lengthMatrix = len(nodCurent.info)
        for i in range(0, lengthMatrix):
            length = len(nodCurent.info[i])
            line = nodCurent.info[i]
            j = 0
            while j < length:
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
                            q = i - 2
                            while q >= 0 and nodCurent.info[q][j] == '*':
                                q -= 1
                            # daca nu cade mai mult de un nivel
                            if i < lengthMatrix - 1 and nodCurent.info[i + 1][j] != '.':
                                drop_ball = True
                                newline[j] = '*'
                                # newline_up[j] = '.'
                                infoNodNou[q + 1][j] = '.'
                            # daca suntem pe ultimul nivel
                            elif i == lengthMatrix - 1:
                                drop_ball = True
                                for qq in range(i - 1, q, -1):
                                    infoNodNou[qq][j] = '.'
                            else:
                                valid_move = False
                        infoNodNou[i] = newline[:]
                        if valid_move:
                            valid_move = verify_matrix(infoNodNou, length)
                        if valid_move:
                            if drop_ball:
                                costArc = 1
                            else:
                                costArc = 1 + (j - k + 1)
                            if not nodCurent.contineInDrum(infoNodNou):
                                listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc, self.calculeaza_h(infoNodNou, tip_euristica)))
                                self.nr_succesori += 1

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
                            q = i - 2
                            while q >= 0 and nodCurent.info[q][j] == '*':
                                q -= 1
                            # daca nu cade mai mult de un nivel
                            if i < lengthMatrix - 1 and nodCurent.info[i + 1][j] != '.':
                                drop_ball = True
                                newline[j] = '*'
                                # newline_up[j] = '.'
                                infoNodNou[q + 1][j] = '.'
                            # daca suntem pe ultimul nivel
                            elif i == lengthMatrix - 1:
                                drop_ball = True
                                for qq in range(i - 1, q, -1):
                                    infoNodNou[qq][j] = '.'
                            else:
                                valid_move = False
                        # indicele de start al secventei de bile
                        kk = k - 1
                        while kk > 0 and line[kk] == '*':
                            kk -= 1
                        # daca in stanga secventei de bile avem un spatiu (avem loc sa le impingem la stanga)
                        if line[kk] == '.':
                            if i < lengthMatrix - 1:
                                newline_down = nodCurent.info[i + 1][:]
                            ind_bila = kk
                            newline[ind_bila] = '*'
                            # daca nu cade mai mult de un nivel
                            if i < lengthMatrix - 2 and nodCurent.info[i + 1][ind_bila] == '.' and nodCurent.info[i + 2][ind_bila] != '.':
                                newline_down[ind_bila] = '*'
                                newline[ind_bila] = '.'
                                drop_ball = True
                            # daca nu cade
                            elif i < lengthMatrix - 1 and nodCurent.info[i + 1][ind_bila] != '.':
                                pass
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
                            valid_move = verify_matrix(infoNodNou, length)
                        if valid_move:

                            if drop_ball:
                                costArc = 1
                            else:
                                costArc = 2 * (1 + (j - k + 1))
                            if not nodCurent.contineInDrum(infoNodNou):
                                listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc, self.calculeaza_h(infoNodNou, tip_euristica)))
                                self.nr_succesori += 1

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
                            q = i - 2
                            while q >= 0 and nodCurent.info[q][k] == '*':
                                q -= 1
                            # daca nu cade mai mult de un nivel
                            if i < lengthMatrix - 1 and nodCurent.info[i + 1][k] != '.':
                                newline[k] = '*'
                                infoNodNou[q + 1][k] = '.'
                                drop_ball = True
                            # daca suntem pe ultimul nivel
                            elif i == lengthMatrix - 1:
                                for qq in range(i - 1, q, -1):
                                    infoNodNou[qq][k] = '.'
                                drop_ball = True
                            else:
                                valid_move = False
                        infoNodNou[i] = newline[:]
                        # daca matricea obtinuta e valida
                        if valid_move:
                            valid_move = verify_matrix(infoNodNou, length)
                        if valid_move:
                            if drop_ball:
                                costArc = 1
                            else:
                                costArc = 1 + (j - k + 1)
                            # daca nu am mai ajuns la configuratia asta pana acum
                            if not nodCurent.contineInDrum(infoNodNou):
                                listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc, self.calculeaza_h(infoNodNou, tip_euristica)))
                                self.nr_succesori += 1
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
                            q = i - 2
                            while q >= 0 and nodCurent.info[q][k] == '*':
                                q -= 1
                            # daca nu cade mai mult de un nivel
                            if i < lengthMatrix - 1 and nodCurent.info[i + 1][k] != '.':
                                newline[k] = '*'
                                infoNodNou[q + 1][k] = '.'
                                drop_ball = True
                            # daca suntem pe ultimul nivel
                            elif i == lengthMatrix - 1:
                                for qq in range(i - 1, q, -1):
                                    infoNodNou[qq][k] = '.'
                                drop_ball = True
                            else:
                                valid_move = False
                        # indicele de start al secventei de bile
                        jj = j + 1
                        while jj < length - 1 and line[jj] == '*':
                            jj += 1
                        # daca in dreapta secventei de bile avem un spatiu (avem loc sa le impingem la dreapta)
                        if line[jj] == '.':
                            if i < lengthMatrix - 1:
                                newline_down = nodCurent.info[i + 1][:]
                            ind_bila = jj
                            newline[ind_bila] = '*'
                            # daca nu cade mai mult de un nivel
                            if i < lengthMatrix - 2 and nodCurent.info[i + 1][ind_bila] == '.' and nodCurent.info[i + 2][ind_bila] != '.':
                                newline_down[ind_bila] = '*'
                                newline[ind_bila] = '.'
                                drop_ball = True
                            # daca nu cade
                            elif i < lengthMatrix - 1 and nodCurent.info[i + 1][ind_bila] != '.':
                                pass
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
                            valid_move = verify_matrix(infoNodNou, length)
                        if valid_move:
                            if drop_ball:
                                costArc = 1
                            else:
                                costArc = 2 * (1 + (j - k + 1))
                            if not nodCurent.contineInDrum(infoNodNou):
                                listaSuccesori.append(NodParcurgere(infoNodNou, nodCurent, nodCurent.g + costArc, self.calculeaza_h(infoNodNou, tip_euristica)))
                                self.nr_succesori += 1
                j += 1
        return listaSuccesori

    def calculeaza_h(self, infoNod, tip_euristica):
        if tip_euristica == "euristica banala":
            for line in infoNod:
                if '*' in line:
                    return 1  # minimul dintre costurile tuturor arcelor
            return 0
        elif tip_euristica == "euristica admisibila 1":
            # calculez cate bile mai am in matrice care nu sunt suprapuse
            nr_balls = 0
            for i in range(len(infoNod)):
                for j in range(len(infoNod[i])):
                    if '*' == infoNod[i][j] and not(i < len(infoNod) - 1 and infoNod[i + 1][j] == '*'):
                        nr_balls += 1
            return nr_balls
        elif tip_euristica == "euristica admisibila 2":
            # calculez cate bile mai am in matrice si cate linii mai am pana dispar(ajung pe ultima linie)
            # exista si mutari care pot sa coboare 2 bile in acelasi timp, asa ca de fiecare data cand calculam inaltimea unei bile, scadem 1
            steps = 0
            diff = 0
            lin = len(infoNod)
            col = len(infoNod[0])
            for i in range(lin):
                for j in range(col):
                    # e bila si sub ia nu sunt alte bile suprapuse
                    if '*' == infoNod[i][j] and not(i < len(infoNod) - 1 and infoNod[i + 1][j] == '*'):
                        steps += len(infoNod) - 1 - i
                        diff += 1
                        if diff > 1:
                            st = j - 1
                            dr = j + 1
                            ok = True
                            if i > 0 and st >= 0 and infoNod[i - 1][st] == '*':
                                ok = False
                            if i > 0 and dr < col and infoNod[i - 1][dr] == '*':
                                ok = False
                            if ok:
                                steps -= 1
                        if i < lin - 1:
                            st = j
                            dr = j
                            ok = False
                            # daca exista posibilitatea ca bila sa fie impinsa pe langa una din placile inferioare
                            if (j + 1 < col and infoNod[i + 1][j + 1] == '.') or (j - 1 >= 0 and infoNod[i + 1][j - 1] == '.'):
                                ok = True
                            while st > 0 and infoNod[i + 1][st - 1] == infoNod[i + 1][st]:
                                st -= 1
                            # daca pot sa mut placa din stanga inferioara astfel incat sa fac loc caderii bilei
                            if i > 0 and st > 0 and infoNod[i + 1][st - 1] == '.' and (j + 1 >= col or infoNod[i + 1][j + 1] != infoNod[i + 1][j]):
                                ok = True
                            while dr < col - 1 and infoNod[i + 1][dr + 1] == infoNod[i + 1][dr]:
                                dr += 1
                            # daca pot sa mut placa din dreapta inferioara astfel incat sa fac loc caderii bilei
                            if i > 0 and dr < col - 1 and infoNod[i + 1][dr + 1] == '.' and (j - 1 < 0 or infoNod[i + 1][j - 1] != infoNod[i + 1][j]):
                                ok = True

                            if not ok:
                                cost_min = min(2 + dr - j, 2 + j - st)
                                st = j
                                dr = j
                                # presupunem ca nu exista spatiu sa mutam una din placile invecinate cu bila noastra
                                while st > 0 and infoNod[i][st - 1] == infoNod[i][st]:
                                    st -= 1
                                if i > 0 and st > 0 and infoNod[i][st - 1] == '.':
                                    cost_min = min(cost_min, j - st + 2)
                                while dr < col - 1 and infoNod[i][dr + 1] == infoNod[i][dr]:
                                    dr += 1
                                if i > 0 and dr < col - 1 and infoNod[i][dr + 1] == '.':
                                    cost_min = min(dr - j + 2, cost_min)
                                steps += cost_min - 1

            return steps - diff + 1
        elif tip_euristica == "euristica neadmisibila":
            # pentru fiecare bila din matrice, presupun ca am o piesa cat restul lungimii liniei - 2 (bila si un spatiu liber ca sa se mute) si adun costul mutarii ei presupunand ca o muta pe orizontala
            # si ca sa ajunga in starea scop trebuie sa mut o astfel de piesa pe fiecare linie a matricei de la bila in jos + o mutare de cost 1 ca sa cada un nivel
            cost = 0
            for i in range(len(infoNod)):
                for x in infoNod[i]:
                    if '*' == x:
                        cost += len(infoNod) - 1 - i
            return cost

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


def uniform_cost(gr, nrSolutiiCautate=1):
    '''
    Argumente:
        gr (Graph): obiectul realizat de clasa Graph
        nrSolutiiCautate (int): Numarul de solutii date ca argument in linie-comanda

    Returneaza: -
    '''
    found_solution = False
    if verify_matrix(gr.start, len(gr.start[0])):
        c = [NodParcurgere(gr.start, None, 0)]
    else:
        g.write("Input invalid\n")
        return
    if gr.testeaza_scop(c[0]):
        g.write("Starea initiala este si finala!\n")
        c[0].afisDrum(g, 1)
        return

    nr_maxim_noduri = 1
    while len(c) > 0:
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        if milis > timeout:
            g.write("TIMEOUT REACHED!\n")
            return

        if len(c) > nr_maxim_noduri:
            nr_maxim_noduri = len(c)
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            found_solution = True
            nodCurent.afisDrum(g, nr_maxim_noduri)
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)
    if not found_solution:
        g.write('Nu exista solutie!\n')
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        g.write("Timp: " + str(milis) + " milisecunde\n")
        g.write("Numar maxim de noduri existente la un moment dat in memorie: " + str(nr_maxim_noduri) + "\n")
        g.write("Numar total de noduri calculate: " + str(gr.nr_succesori) + "\n")


def a_star(gr, nrSolutiiCautate, tip_euristica):
    '''
    Argumente:
        gr (Graph): obiectul realizat de clasa Graph
        nrSolutiiCautate (int): Numarul de solutii date ca argument in linie-comanda
        tip_euristica (str): Tipul de euristica ce trebuie folosit in calcularea h-ului

    Returneaza: -
    '''
    found_solution = False

    if verify_matrix(gr.start, len(gr.start[0])):
        c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica=tip_euristica))]
    else:
        g.write("Input invalid\n")
        return

    nr_maxim_noduri = 1
    if gr.testeaza_scop(c[0]):
        g.write("Starea initiala este si finala!\n")
        c[0].afisDrum(g, 1)
        return
    while len(c) > 0:
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        if milis > timeout:
            g.write("TIMEOUT REACHED!\n")
            return

        if len(c) > nr_maxim_noduri:
            nr_maxim_noduri = len(c)
        nodCurent = c.pop(0)

        if gr.testeaza_scop(nodCurent):
            found_solution = True
            nodCurent.afisDrum(g, nr_maxim_noduri)
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)
    if not found_solution:
        g.write('Nu exista solutie!\n')
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        g.write("Timp: " + str(milis) + " milisecunde\n")
        g.write("Numar maxim de noduri existente la un moment dat in memorie: " + str(nr_maxim_noduri) + "\n")
        g.write("Numar total de noduri calculate: " + str(gr.nr_succesori) + "\n")


def a_star_optimizat(gr, tip_euristica):
    '''
    Argumente:
        gr (Graph): obiectul realizat de clasa Graph
        tip_euristica (str): Tipul de euristica ce trebuie folosit in calcularea h-ului

    Returneaza: -
    '''
    found_solution = False
    if verify_matrix(gr.start, len(gr.start[0])):
        l_open = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica=tip_euristica))]
    else:
        g.write("Input invalid\n")
        return

    nr_maxim_noduri = 1

    l_closed = []
    while len(l_open) > 0:
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        if milis > timeout:
            g.write("TIMEOUT REACHED!\n")
            return
        if len(l_open) + len(l_closed) > nr_maxim_noduri:
            nr_maxim_noduri = len(l_open) + len(l_closed)
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent):
            nodCurent.afisDrum(g, nr_maxim_noduri)
            return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                if l_open[i].f > s.f or (l_open[i].f == s.f and l_open[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)
    if not found_solution:
        g.write('Nu exista solutie!\n')
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        g.write("Timp: " + str(milis) + " milisecunde\n")
        g.write("Numar maxim de noduri existente la un moment dat in memorie: " + str(nr_maxim_noduri) + "\n")
        g.write("Numar total de noduri calculate: " + str(gr.nr_succesori) + "\n")


def ida_star(gr, nrSolutiiCautate, tip_euristica):
    '''
    Argumente:
        gr (Graph): obiectul realizat de clasa Graph
        nrSolutiiCautate (int): Numarul de solutii date ca argument in linie-comanda
        tip_euristica (str): Tipul de euristica ce trebuie folosit in calcularea h-ului

    Returneaza: -
    '''
    if verify_matrix(gr.start, len(gr.start[0])):
        nodStart = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica=tip_euristica))
        if gr.testeaza_scop(nodStart):
            g.write("Starea initiala este si finala!\n")
            nodStart.afisDrum(g, 1)
            return
    else:
        g.write("Input invalid\n")
        return
    limita = nodStart.f
    while True:
        nr_maxim_noduri = 1
        nrSolutiiCautate, rez, nr_maxim_noduri = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, nr_maxim_noduri, tip_euristica)
        if rez == "gata":
            break
        if rez == float('inf'):
            g.write('Nu exista solutie!\n')
            t2 = time.time()
            milis = round(1000 * (t2 - t1))
            g.write("Timp: " + str(milis) + " milisecunde\n")
            g.write("Numar maxim de noduri existente la un moment dat in memorie: " + str(nr_maxim_noduri) + "\n")
            g.write("Numar total de noduri calculate: " + str(gr.nr_succesori) + "\n")
            break
        limita = rez


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, nr_maxim_noduri, tip_euristica):
    '''
    Argumente:
        gr (Graph): obiectul realizat de clasa Graph
        nodCurent (NodParcurgere): nodul curent (din graf) pe care il evaluam
        limita (int): limita in functie de care stabilim daca continuam expandarea nodului
        nrSolutiiCautate (int): Numarul de solutii date ca argument in linie-comanda
        nr_maxim_noduri (int): Numarul maxim de noduri in memorie la un moment dat ce trebuie pasat spre afisare
        tip_euristica (str): Tipul de euristica ce trebuie folosit in calcularea h-ului

    Returneaza: -
    '''
    t2 = time.time()
    milis = round(1000 * (t2 - t1))
    if milis > timeout:
        g.write("TIMEOUT REACHED!\n")
        return 0, "gata", 0
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f, nr_maxim_noduri
    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
        nodCurent.afisDrum(g, nr_maxim_noduri)
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return 0, "gata", nr_maxim_noduri
    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
    nr_maxim_noduri += len(lSuccesori)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez, nr_maxim_noduri = construieste_drum(gr, s, limita, nrSolutiiCautate, nr_maxim_noduri, tip_euristica)
        if rez == "gata":
            return 0, "gata", nr_maxim_noduri
        if rez < minim:
            minim = rez
    return nrSolutiiCautate, minim, nr_maxim_noduri


def verify_matrix(matrix, length):
    '''
    Argumente:
        matrix (liste de liste de char-uri): Starea sub forma de matrice pe care trebuie sa o afiseze
        length (int): Lungimea primei linii citite din fisierul de input pentru a verifica daca toate liniile din matrice au aceeasi lungime

    Returneaza: True daca matricea respecta constrangerile de validare, altfel False
    '''
    if length == 0:
        return False
    for (poz, line) in enumerate(matrix):
        if length != len(line):
            return False
        # daca nu suntem pe ultima linie
        if poz != len(matrix) - 1:
            i = 0
            while i < length:
                # presupunem ca placa e in aer
                floating = True
                # cat timp nu am ajuns la capat, avem o secventa si nu suntem siguri ca nu e in aer
                while i < length - 1 and line[i] == line[i + 1]:
                    # daca sub ea nu e un gol continuu sau ea insasi e un gol
                    if matrix[poz + 1][i] != '.' or line[i] == '.':
                        floating = False
                    i += 1
                if matrix[poz + 1][i] != '.' or line[i] == '.':
                    floating = False
                if floating:
                    return False
                i += 1
    return True


def print_matrix(matrix, file):
    '''
    Argumente:
        matrix (liste de liste de char-uri): Starea sub forma de matrice pe care trebuie sa o afiseze
        file (str): Fisierul de output unde trebuie facuta afisarea

    Returneaza: -
    '''
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
    # daca avem deja bila pe ultima linie, o stergem automat
    for i in range(len(gr.start[len(gr.start) - 1])):
        if gr.start[len(gr.start) - 1][i] == '*':
            line_ind = len(gr.start) - 1
            while line_ind >= 0 and gr.start[line_ind][i] == '*':
                gr.start[line_ind][i] = '.'
                line_ind -= 1
            print(gr.start)

    # uniform_cost(gr, nrSolutiiCautate=nsol)

    # a_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica banala")
    # a_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica admisibila 1")
    # a_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica admisibila 2")
    # a_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica neadmisibila")

    # a_star_optimizat(gr, tip_euristica="euristica banala")
    # a_star_optimizat(gr, tip_euristica="euristica admisibila 1")
    # a_star_optimizat(gr, tip_euristica="euristica admisibila 2")
    # a_star_optimizat(gr, tip_euristica="euristica neadmisibila")

    # ida_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica banala")
    # ida_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica admisibila 1")
    # ida_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica admisibila 2")
    ida_star(gr, nrSolutiiCautate=nsol, tip_euristica="euristica neadmisibila")
    g.close()


