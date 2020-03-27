import sys, os
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QApplication, QDesktopWidget, QPushButton, QLineEdit, 
                             QInputDialog)
from PyQt5.QtGui     import (QIcon, QPainter, QPen, QColor)
from PyQt5.QtCore    import Qt
from dialogs         import *
from math            import *
from locale          import *
import math

class Example(QMainWindow):    
    def __init__(self):
        super().__init__()
        self.linhas_dda = []
        self.linhas_bsr = []
        self.circulos   = []
        self.comando    = '' 
        self.recorteIni = None
        self.recorteFim = None
        self.nPtsControle = -1
        self.auxControle  = 0
        self.initUI()    
           
            
    def initUI(self):              
        self.resize(960, 540)
        self.center()
        self.setWindowTitle('CG - Algoritmos Unidade I')  
        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)


        ### Criar barra de menu ###
        menubar  = self.menuBar()

        rasteiMenu = menubar.addMenu('&Rasteirização')
        ddaAction = rasteiMenu.addAction('Retas - DDA')
        ddaAction.setShortcut('Ctrl+D')
        ddaAction.triggered.connect(self.btnDDA)

        breAction = rasteiMenu.addAction('Retas - Bresenham')
        breAction.setShortcut('Ctrl+B')
        breAction.triggered.connect(self.btnBSR)

        rasteiMenu.addSeparator()

        circAction = rasteiMenu.addAction('Circunferência – Bresenham')
        circAction.setShortcut('Ctrl+C')
        circAction.triggered.connect(self.btnCirculo)

        transfMenu = menubar.addMenu('&Transformações')
        traAction = transfMenu.addAction('Translação') 
        traAction.setShortcut('Ctrl+T')
        traAction.triggered.connect(self.translacaoDialog)

        rotAction = transfMenu.addAction('Rotação')
        rotAction.setShortcut('Ctrl+R')
        rotAction.triggered.connect(self.rotacaoDialog)

        escAction = transfMenu.addAction('Escala')
        escAction.setShortcut('Ctrl+E')
        escAction.triggered.connect(self.escalaDialog)

        refXAction = transfMenu.addAction('Reflexão em X')
        refXAction.setShortcut('Ctrl+X')
        refXAction.triggered.connect(self.reflexaoemX)

        refYAction = transfMenu.addAction('Reflexão em Y')
        refYAction.setShortcut('Ctrl+Y')
        refYAction.triggered.connect(self.reflexaoemY)

        refCAction = transfMenu.addAction('Reflexão no Centro')
        refCAction.setShortcut('Ctrl+O')
        refCAction.triggered.connect(self.reflexaonoCentro)

        recMenu = menubar.addMenu('&Recorte')
        csAction = recMenu.addAction('Regiões codificadas – Cohen-Sutherland') 
        csAction.setShortcut('Ctrl+S')
        csAction.triggered.connect(self.btnRecorteCS)
        
        lbAction = recMenu.addAction('Equação paramétrica – Liang-Barsky')
        lbAction.setShortcut('Ctrl+L')
        lbAction.triggered.connect(self.btnRecorteLB)



        limparMenu = menubar.addMenu('&Limpar')
        apagarTudo = limparMenu.addAction('Apagar Tudo')
        apagarTudo.setShortcut('Ctrl+A')
        apagarTudo.triggered.connect(self.apagarTudo)



        ###########TOOLBAR ###########
        self.toolbar = self.addToolBar('toolbar')
        self.show()     

    def mousePressEvent(self, event):        
        if event.button() == Qt.LeftButton :
            if self.comando == 'dda':
                p1 = {'x': event.pos().x(), 'y': event.pos().y()}
                self.linhas_dda.append([p1,p1])
                print("Reta - DDA: , Valor de x:{}, valor de y:{}".format(p1['x'],p1['y']))
            elif self.comando == 'bsr':            
                p1 = {'x': event.pos().x(), 'y': event.pos().y()}
                self.linhas_bsr.append([p1,p1])
                print("Reta - Bresenham: , Valor de x:{}, valor de y:{}".format(p1['x'],p1['y']))
            elif self.comando == 'circ':                            
                p1 = {'x': event.pos().x(), 'y': event.pos().y()}
                self.circulos.append([p1,p1])
                print("Circunferência – Bresenham: , Valor de x:{}, valor de y:{}".format(p1['x'],p1['y']))   
            elif self.comando == 'recortecs':
                self.recorteIni = {'x': event.pos().x(), 'y': event.pos().y()}                
                print("Comando: recortecs, Valor de x:{}, valor de y:{}".format(self.recorteIni['x'], self.recorteIni['y']))   
            elif self.comando == 'recortelb':
                self.recorteIni = {'x': event.pos().x(), 'y': event.pos().y()}                
                print("Comando: recortelb, Valor de x:{}, valor de y:{}".format(self.recorteIni['x'], self.recorteIni['y']))   

    def mouseMoveEvent(self, event):
        if self.comando == 'dda':
            p2 = {'x': event.pos().x(), 'y': event.pos().y()}
            self.linhas_dda[len(self.linhas_dda) - 1][1] = p2
            self.update()
        if self.comando == 'bsr':
            p2 = {'x': event.pos().x(), 'y': event.pos().y()}
            self.linhas_bsr[len(self.linhas_bsr) - 1][1] = p2
            self.update()
        if self.comando == 'circ':
            p2 = {'x': event.pos().x(), 'y': event.pos().y()}
            self.circulos[len(self.circulos) - 1][1] = p2
            self.update()
        if self.comando == 'recortecs':
            self.recorteFim = {'x': event.pos().x(), 'y': event.pos().y()}
        if self.comando == 'recortelb':
            self.recorteFim = {'x': event.pos().x(), 'y': event.pos().y()}

    def paintEvent(self, e):
        cor = Qt.black    
        pen = QPen(cor, 3, Qt.SolidLine)                    
        painter = QPainter(self)
        painter.setPen(pen)    

        if self.comando == 'recortecs' and self.recorteIni:
            if self.recorteIni and self.recorteFim:
                pen = QPen(cor, 3, Qt.DashLine)
                painter.setPen(pen)
                painter.drawLine(self.recorteIni['x'], self.recorteIni['y'], self.recorteFim['x'], self.recorteIni['y']) #superior
                painter.drawLine(self.recorteIni['x'], self.recorteIni['y'], self.recorteIni['x'], self.recorteFim['y']) #esquerda
                painter.drawLine(self.recorteIni['x'], self.recorteFim['y'], self.recorteFim['x'], self.recorteFim['y']) #inferior
                painter.drawLine(self.recorteFim['x'], self.recorteFim['y'], self.recorteFim['x'], self.recorteIni['y']) #direita

                for pini, pfim in self.linhas_dda:
                    valores = cohenSutherland(self.recorteIni, self.recorteFim, pini, pfim)
                    if not valores:
                        continue
                    (x1, y1, x2, y2) = valores
                    p1 = {'x': x1, 'y': y1}
                    p2 = {'x': x2, 'y': y2}
                    for ponto in bresenhan(p1, p2, cor):
                        painter.drawPoint(ponto['x'], ponto['y'])

                for pini, pfim in self.linhas_bsr:
                    valores = cohenSutherland(self.recorteIni, self.recorteFim, pini, pfim)
                    if not valores:
                        continue
                    (x1, y1, x2, y2) = valores
                    p1 = {'x': x1, 'y': y1}
                    p2 = {'x': x2, 'y': y2}
                    for ponto in bresenhan(p1, p2, cor):
                        painter.drawPoint(ponto['x'], ponto['y'])
   
            self.update()            
        elif self.comando == 'recortelb' and self.recorteIni:
            if self.recorteIni and self.recorteFim:
                pen = QPen(cor, 3, Qt.DashLine)
                painter.setPen(pen)
                painter.drawLine(self.recorteIni['x'], self.recorteIni['y'], self.recorteFim['x'], self.recorteIni['y']) #superior
                painter.drawLine(self.recorteIni['x'], self.recorteIni['y'], self.recorteIni['x'], self.recorteFim['y']) #esquerda
                painter.drawLine(self.recorteIni['x'], self.recorteFim['y'], self.recorteFim['x'], self.recorteFim['y']) #inferior
                painter.drawLine(self.recorteFim['x'], self.recorteFim['y'], self.recorteFim['x'], self.recorteIni['y']) #direita
                for pini, pfim in self.linhas_dda:
                    valores = liang_Barsky(self.recorteIni, self.recorteFim, pini, pfim)
                    if not valores:
                        continue
                    (x1, y1, x2, y2) = valores
                    p1 = {'x': x1, 'y': y1}
                    p2 = {'x': x2, 'y': y2}
                    for ponto in bresenhan(p1, p2, cor):
                        painter.drawPoint(ponto['x'], ponto['y'])

                for pini, pfim in self.linhas_bsr:
                    valores = liang_Barsky(self.recorteIni, self.recorteFim, pini, pfim)
                    if not valores:
                        continue
                    (x1, y1, x2, y2) = valores
                    p1 = {'x': x1, 'y': y1}
                    p2 = {'x': x2, 'y': y2}
                    for ponto in bresenhan(p1, p2, cor):
                        painter.drawPoint(ponto['x'], ponto['y'])


            self.update()
        else:
            for p1,p2 in self.linhas_dda:
                for ponto in dda(p1,p2,cor):
                    painter.drawPoint(ponto['x'],ponto['y'])
            
            for p1,p2 in self.linhas_bsr:
                for ponto in bresenhan(p1,p2,cor):
                    painter.drawPoint(ponto['x'],ponto['y'])

            for centro, p in self.circulos:
                for ponto in bresenhamCirc(centro, p, cor):
                    painter.drawPoint(ponto['x'],ponto['y'])

            self.update()


    def btnDDA(self):
        self.comando = 'dda'
    
    def btnBSR(self):
        self.comando = 'bsr'
    
    def btnCirculo(self):
        self.comando = 'circ'

    def btnRecorteCS(self):
        self.comando = 'recortecs'

    def btnRecorteLB(self):
        self.comando = 'recortelb'
    
    def apagarTudo(self):
        self.circulos      = []
        self.linhas_bsr    = []
        self.linhas_dda    = []
        self.recorteIni = None
        self.recorteFim = None
        self.update()

    def center(self):
        frame = self.frameGeometry()
        cpoint = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(cpoint)
        self.move(frame.topLeft())


#_______________________________________________________________________________________________________________________________#


#_______________________________________________________________________________________________________________________________#
                                                    #### Transformações ####
    #Transformações - Deslocamento de objetos segundo um vetor
    def translacaoDialog(self):
        x, y, ok = TranslacaoDialog.getResults()
        if ok:                
            for dda in self.linhas_dda:
                for ponto in dda:
                    ponto['x'] += int(x)
                    ponto['y'] += int(y)
            for bsr in self.linhas_bsr:
                for ponto in bsr:
                    ponto['x'] += int(x)
                    ponto['y'] += int(y)
            for bsrCirculo in self.circulos:
                for ponto in bsrCirculo:
                    ponto['x'] += int(x)
                    ponto['y'] += int(y)
                    
    def rotacaoDialog(self):
        angulo, ok = RotacaoDialog.getResults()
        if ok:
            seno = float(math.sin(angulo))
            cosseno = float((math.cos(angulo)))

            for dda in self.linhas_dda:
                pi = dda[0] #ponto inicial
                for p in dda:
                    x1 = ((p['x'] - pi['x']) * cosseno)
                    y1 = ((p['y'] - pi['y']) * seno)
                    x2 = ((p['x'] - pi['x']) * seno)
                    y2 = ((p['y'] - pi['y']) * cosseno)

                    p['x'] = x1 - y1 + pi['x']
                    p['y'] = x2 + y2 + pi['y']

            for bsr in self.linhas_bsr:
                pi = bsr[0]
                for p in bsr:
                    x1 = ((p['x'] - pi['x']) * cosseno)
                    y1 = ((p['y'] - pi['y']) * seno)
                    x2 = ((p['x'] - pi['x']) * seno)
                    y2 = ((p['y'] - pi['y']) * cosseno)
                    
                    p['x'] = x1 - y1 + pi['x']
                    p['y'] = x2 + y2 + pi['y']

    def escalaDialog(self):
        escalaA, ok = EscalaDialog.getResults()

        if ok:            
            escalaA = float(escalaA.replace(',','.'))
            for dda in self.linhas_dda:
                pi = dda[0]
                for p in dda:
                    p['x'] = ((p['x'] - pi['x'])*escalaA) + pi['x']
                    p['y'] = ((p['y'] - pi['y'])*escalaA) + pi['y']

            for bsr in self.linhas_bsr:        
                pi = bsr[0]
                for p in bsr:
                    p['x'] = ((p['x'] - pi['x'])*escalaA) + pi['x']
                    p['y'] = ((p['y'] - pi['y'])*escalaA) + pi['y']
            for bsrCirculo in self.circulos:
                pi = bsrCirculo[0]
                for p in bsrCirculo:
                    p['x'] = ((p['x'] - pi['x'])*escalaA) + pi['x']
                    p['y'] = ((p['y'] - pi['y'])*escalaA) + pi['y']

    def reflexao(self,rx,ry):
        for dda in self.linhas_dda:
            pi = dda[0]
            for p in dda:
                p['x'] = ((p['x'] - pi['x']) * (rx)) + pi['x']
                p['y'] = ((p['y'] - pi['y']) * (ry)) + pi['y']
        for bsr in self.linhas_bsr:
            pi = bsr[0]
            for p in bsr:
                p['x'] = ((p['x'] - pi['x']) * (rx)) + pi['x']
                p['y'] = ((p['y'] - pi['y']) * (ry)) + pi['y']
        for bsrCirculo in self.circulos:
            pi = bsrCirculo[0]
            for p in bsrCirculo:
                p['x'] = ((p['x'] - pi['x']) * (rx)) + pi['x']
                p['y'] = ((p['y'] - pi['y']) * (ry)) + pi['y']
        self.update()

    def reflexaoemX(self):
        self.reflexao(1,-1)
    def reflexaoemY(self):
        self.reflexao(-1,1)
    def reflexaonoCentro(self):
        self.reflexao(-1,-1)
#_______________________________________________________________________________________________________________________________#


#_______________________________________________________________________________________________________________________________#
                                            ### Algoritmos implementados ###

def dda(p1, p2, cor): 
    x, y = p1['x'], p1['y']
    dx = p2['x'] - x
    dy = p2['y'] - y
    linha = [p1]

    if abs(dx) > abs(dy) :   # > ou >= TESTAR
        passos = int(abs(dx))
    else:
        passos = int(abs(dy))
    if passos == 0:
        return linha

    xincr = dx/passos
    yincr = dy/passos
    
    for _ in range(passos):
        x += xincr
        y += yincr
        linha.append({'x': round(x), 'y': round(y)})

    return linha

def bresenhan(p1, p2, cor):
    x, y = p1['x'], p1['y']
    #USO DE VARIÁVEIS INTEIRS APENAS
    dx = int(p2['x'] - x)
    dy = int(p2['y'] - y)
    linha = [p1]

    if dx < 0 :
        dx = -dx; xincr = -1
    else: 
        xincr = 1

    if dy < 0 : 
        dy = -dy
        yincr = -1
    else: 
        yincr = 1
        
    if dx > dy : #1º caso
        p = 2*dy-dx
        c1 = 2*dy; c2 = 2*(dy-dx)
        for i in range(dx):
            #vai sempre atualizando o valor de x
            x += xincr  
            if p < 0 :
                p+= c1
            else:
                y += yincr
                p+= c2
            linha.append({'x': x, 'y': y})
    else: #2º caso
        p = 2*dx-dy; c1 = 2*dx; c2 = 2*(dx-dy)
        for i in range(dy):
            #vai sempre atualizando o valor de y
            y += yincr
            if p < 0 :
                p += c1
            else:
                p += c2
                x += xincr            
            linha.append({'x': x, 'y': y})
    return linha


def bresenhamCirc(centro, p1, cor):
        raio = round(sqrt((centro['x'] - p1['x'])**2 + (centro['y'] - p1['y'])**2))
        x = 0
        y = raio
        p = 3-2*raio

        circ = desenhaSimetricos(centro, x, y)

        while x < y:   #2°octante
            if p < 0:
                p += 4*x + 6
            else:
                p += 4*(x - y) + 10
                y -= 1 # atualizacao
            x += 1
            circ += desenhaSimetricos(centro, x, y)
        return circ

def desenhaSimetricos(centro,x,y):#plota todos pontos simetricos
        pontos = []
        pontos.append({'x': centro['x'] + x, 'y': centro['y'] + y})
        pontos.append({'x': centro['x'] + x, 'y': centro['y'] - y})
        pontos.append({'x': centro['x'] - x, 'y': centro['y'] + y})
        pontos.append({'x': centro['x'] - x, 'y': centro['y'] - y})
        pontos.append({'x': centro['x'] + y, 'y': centro['y'] + x})
        pontos.append({'x': centro['x'] + y, 'y': centro['y'] - x})
        pontos.append({'x': centro['x'] - y, 'y': centro['y'] + x})
        pontos.append({'x': centro['x'] - y, 'y': centro['y'] - x})
        return pontos

    
    #calcula os limites da regiao
def limites(p1, p2):
    if p1['x'] > p2['x']:
        xmax = p1['x']
        xmin = p2['x']
    else:
        xmax = p2['x']
        xmin = p1['x']

    if p1['x'] > p2['y']:
        ymax = p1['y']
        ymin = p2['y']
    else:
        ymax = p2['y']
        ymin = p1['y']

    return(xmax, ymax, xmin, ymin)

    
'''
     obtem o codigo associados a sua posicao inicial e final, dependendo da sua posicao
     em relacao a janela.    
'''
def obtemCodigo(p1,p2,x,y): 
        codigo = 0
        (xmax, ymax, xmin, ymin) = limites(p1, p2)

        if x < xmin:
            codigo = codigo + 1
        elif x > xmax:
            codigo = codigo + 2
        if y < ymin:
            codigo = codigo + 4
        elif y > ymax:
            codigo = codigo + 8
        
        return codigo


def cohenSutherland(p1, p2, pi, pf):
        aceite = False
        feito = False
        (xmax, ymax, xmin, ymin) = limites(p1, p2)
        (x1, y1, x2, y2) = (pi['x'], pi['y'], pf['x'], pf['y'])

        while not feito:
            codigo1 = obtemCodigo(p1,p2,x1,y1)
            codigo2 = obtemCodigo(p1,p2,x2,y2)

            if codigo1 == 0 and codigo2 == 0: #segmento completamente dentro
                aceite = True
                feito = True
            elif codigo1 & codigo2 != 0: #segmento completamente fora
                feito = True
            else:
                if codigo1 != 0: #determina ponto exterior
                    cfora = codigo1
                else:
                    cfora = codigo2

                if cfora & 1 == 1: #limite esquerdo, bit 0
                    xint = xmin
                    yint = y1+(y2-y1)*(xmin-x1)/(x2-x1)
                elif cfora & 2 == 2: #limite direito, bit 1
                    xint = xmax
                    yint = y1+(y2-y1)*(xmax-x1)/(x2-x1)
                elif cfora & 4 == 4: #limite abaixo, bit 2
                    yint = ymin
                    xint = x1+(x2-x1)*(ymin-y1)/(y2-y1)
                elif cfora & 8 == 8: #limite superior, bit 3
                    yint = ymax
                    xint = x1+(x2-x1)*(ymax-y1)/(y2-y1)

                if codigo1 == cfora: #att p.inicial da reta
                    x1 = xint
                    y1 = yint
                else:                #att p.final da reta
                    x2 = xint
                    y2 = yint
        if(aceite):
            return (round(x1), round(y1), round(x2), round(y2))
        else:
            return ()



def cliptest(p,q,u1,u2):
    result = True

    if p < 0:
        r = q/p
        if r > u2:
            result = False
        elif r > u1:
            u1 = r
    elif p > 0:
        r = q/p
        if r < u1:
            result = False
        elif r < u2:
            u2 = r
    elif q < 0:
        result = False

    #F => fora da janela
    #V => pode passar p/ proxima fronteira
    return(u1,u2,result) 

def liang_Barsky(p1,p2,pi,pf):
    u1 = 0
    u2 = 1 

    (x1,y1,x2,y2) = (pi['x'],pi['y'],pf['x'],pf['y'])

    (xmax,ymax,xmin,ymin) = limites(p1,p2)

    dx = x2-x1
    dy = y2-y1

    u1, u2, result = cliptest(-dx, x1 - xmin, u1, u2)
    if result: #fronteira esquerda
        u1, u2, result = cliptest(dx, xmax - x1, u1, u2)
        if result: #fronteira direita
            u1, u2, result = cliptest(-dy, y1 - ymin, u1, u2)
            if result: #fronteira inferior
                u1, u2, result = cliptest(dy, ymax - y1, u1, u2)
                if result: #fronteira superior
                    if u2 < 1:
                        x2 = x1 + (dx * u2)
                        y2 = y1 + (dy * u2)
                    if u1 > 0:
                        x1 = x1 + (dx * u1)
                        y1 = y1 + (dy * u1)
                    return (round(x1), round(y1), round(x2), round(y2))

    return ()
#_______________________________________________________________________________________________________________________________#



#_______________________________________________________________________________________________________________________________#
                                            ### Dialogs ###

class TranslacaoDialog(QDialog):
    def __init__(self, parent = None):
        super(TranslacaoDialog, self).__init__(parent)

        layout = QFormLayout(self)
        self.setWindowTitle("Translação")
        
        #Entrada para transalação no eixo X
        self.trans_x = QLineEdit()
        self.trans_x.setValidator(QIntValidator())
        self.trans_x.setMaxLength(4)
        layout.addRow("Translação no eixo X: ", self.trans_x)

        #Entrada para transalação no eixo X
        self.trans_y = QLineEdit()
        self.trans_y.setValidator(QIntValidator())
        self.trans_y.setMaxLength(4)
        layout.addRow("Translação no eixo Y: ", self.trans_y)

        # Butões de OK e Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def getX(self):
        return self.trans_x.text()

    def getY(self):
        return self.trans_y.text()

    @staticmethod
    def getResults(parent = None):
        dialog = TranslacaoDialog(parent)
        result = dialog.exec_()
        trans_x = dialog.getX()
        trans_y = dialog.getY()
        return (trans_x, trans_y, result == QDialog.Accepted)


class RotacaoDialog(QDialog):
    def __init__(self, parent = None):
        super(RotacaoDialog, self).__init__(parent)

        layout = QFormLayout(self)
        self.setWindowTitle("Rotação")

        #entrada para angulo de rotação
        self.ang = QDoubleSpinBox()
        self.ang.setRange(-360,360)
        layout.addRow("Ângulo: ", self.ang)

        #Ok and cancel
        buttons = QDialogButtonBox(
        QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
        Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def getAngulo(self):
        return self.ang.text()

    @staticmethod
    def getResults(parent = None):
        dialog = RotacaoDialog(parent)
        result = dialog.exec_()
        ang = dialog.getAngulo()
        return (radians(float(ang.replace(',','.'))), result == QDialog.Accepted)

class EscalaDialog(QDialog):
    def __init__(self, parent = None):
        super(EscalaDialog, self).__init__(parent)

        layout = QFormLayout(self)
        self.setWindowTitle("Escala")

        #entrar com escala
        self.escalaEscA = QDoubleSpinBox()
        ##self.escalaEscA = setMinimum(0)
        layout.addRow("Valor da escalaEscA: ",self.escalaEscA)

        #Ok and cancel
        buttons = QDialogButtonBox(
        QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
        Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)  
    
    def getEscalaEscA(self):
        return self.escalaEscA.text()

    @staticmethod
    def getResults(parent = None):
        dialog = EscalaDialog(parent)
        result = dialog.exec_()
        escalaEscA = dialog.getEscalaEscA()
        return (escalaEscA, result == QDialog.Accepted)

#_______________________________________________________________________________________________________________________________#






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
