import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from math 			 import *
from locale 		 import *

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