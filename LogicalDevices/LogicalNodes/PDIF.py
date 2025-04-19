import math
from dataclasses import dataclass, field

from LogicalDevices.LogicalNodes.CommonDataClasses.ACD import ACD
from LogicalDevices.LogicalNodes.CommonDataClasses.ACT import ACT
from LogicalDevices.LogicalNodes.CommonDataClasses.ASG import ASG
from LogicalDevices.LogicalNodes.CommonDataClasses.CMV import CMV
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.BasicTypes.BOOLEAN import BOOLEAN
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.Enum.dirEnum import DirEnum
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.Quality import Quality
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.TimeStamp import TimeStamp
from LogicalDevices.LogicalNodes.CommonDataClasses.SAV import SAV
from LogicalDevices.LogicalNodes.CommonDataClasses.WYE import WYE
from LogicalDevices.LogicalNodes.LogicalNodeClass import LogicalNodeClass


@dataclass
class PDIF(LogicalNodeClass):
    pARem: WYE = field(init=False)
    ARes: WYE = field(init=False)
    Amp1: SAV = field(init=False)
    Amp2: SAV = field(init=False)
    Amp3: SAV = field(init=False)

    Blk2Q1: ACD = field(init=False)
    Blk2Q2: ACD = field(init=False)
    Blk2Q3: ACD = field(init=False)
    Blk5Q1: ACD = field(init=False)
    Blk5Q2: ACD = field(init=False)
    Blk5Q3: ACD = field(init=False)

    StrVal: ASG = field(init=False) # начальный дифференциальный ток
    KVal: ASG = field(init=False)   # коэффициент торможения

    Str: ACD = field(init=False)
    Op: ACT = field(init=False)
    counter = 0


    def process(self):

        DifAPhsA = self.pARem.phsA.cVal.mag.f.value * math.cos(self.pARem.phsA.cVal.ang.f.value) # Диф ток фазы А
        DifAPhsB = self.pARem.phsB.cVal.mag.f.value * math.cos(self.pARem.phsB.cVal.ang.f.value) # Диф ток фазы В
        DifAPhsC = self.pARem.phsC.cVal.mag.f.value * math.cos(self.pARem.phsC.cVal.ang.f.value) # Диф ток фазы С

        ResAPhsA = self.ARes.phsA.cVal.mag.f.value  # Торм ток фазы А
        ResAPhsB = self.ARes.phsB.cVal.mag.f.value  # Торм ток фазы В
        ResAPhsC = self.ARes.phsC.cVal.mag.f.value  # Торм ток фазы С

        ResAStrVal = self.StrVal.setMag.f.value / self.KVal.setMag.f.value  # Ток начала торможения

        Str1PhsA = DifAPhsA > self.StrVal.setMag.f.value # Срабатывание на 1 участке фаза А
        Str1PhsB = DifAPhsB > self.StrVal.setMag.f.value # Срабатывание на 1 участке фаза В
        Str1PhsC = DifAPhsB > self.StrVal.setMag.f.value # Срабатывание на 1 участке фаза С

        Str2PhsA = DifAPhsA > self.StrVal.setMag.f.value * self.KVal.setMag.f.value  # Срабатывание на 2 участке фаза А
        Str2PhsB = DifAPhsB > self.StrVal.setMag.f.value * self.KVal.setMag.f.value  # Срабатывание на 2 участке фаза В
        Str2PhsC = DifAPhsC > self.StrVal.setMag.f.value * self.KVal.setMag.f.value  # Срабатывание на 2 участке фаза C

        isSlopingSecPhsA = ResAPhsA > ResAStrVal
        isSlopingSecPhsB = ResAPhsB > ResAStrVal
        isSlopingSecPhsC = ResAPhsC > ResAStrVal

        Blk2PhsA = self.Blk2Q1.phsA.value or self.Blk2Q2.phsA.value or self.Blk2Q3.phsA.value
        Blk2PhsB = self.Blk2Q1.phsB.value or self.Blk2Q2.phsB.value or self.Blk2Q3.phsB.value
        Blk2PhsC = self.Blk2Q1.phsC.value or self.Blk2Q2.phsC.value or self.Blk2Q3.phsC.value

        Blk5PhsA = self.Blk5Q1.phsA.value or self.Blk5Q2.phsA.value or self.Blk5Q3.phsA.value
        Blk5PhsB = self.Blk5Q1.phsB.value or self.Blk5Q2.phsB.value or self.Blk5Q3.phsB.value
        Blk5PhsC = self.Blk5Q1.phsC.value or self.Blk5Q2.phsC.value or self.Blk5Q3.phsC.value

        StrPhsA = ((isSlopingSecPhsA & Str2PhsA) or Str1PhsA) and not (Blk2PhsA) and not (Blk5PhsA)
        StrPhsB = ((isSlopingSecPhsB & Str2PhsB) or Str1PhsB) and not (Blk2PhsB) and not (Blk5PhsB)
        StrPhsC = ((isSlopingSecPhsC & Str2PhsC) or Str1PhsC) and not (Blk2PhsC) and not (Blk5PhsC)

        self.Str = ACD()

        self.Str.general = BOOLEAN(StrPhsA or StrPhsB or StrPhsC)
        self.Str.phsA = BOOLEAN(StrPhsA)
        self.Str.phsB = BOOLEAN(StrPhsB)
        self.Str.phsC = BOOLEAN(StrPhsC)
        self.Str.neut = BOOLEAN(False)
        self.Str.dirGeneral = DirEnum.UNKNOWN
        self.Str.dirPhsA = DirEnum.UNKNOWN
        self.Str.dirPhsB = DirEnum.UNKNOWN
        self.Str.dirPhsC = DirEnum.UNKNOWN
        self.Str.dirNeut = DirEnum.UNKNOWN
        self.Str.q = Quality()
        self.Str.t = TimeStamp()

        self.Op = ACT()

        self.Op.general = BOOLEAN(StrPhsA or StrPhsB or StrPhsC)
        self.Op.phsA = BOOLEAN(StrPhsA)
        self.Op.phsB = BOOLEAN(StrPhsB)
        self.Op.phsC = BOOLEAN(StrPhsC)
        self.Op.neut = BOOLEAN(False)
        self.Op.q = Quality()
        self.Op.t = TimeStamp()


