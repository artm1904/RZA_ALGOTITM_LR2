from dataclasses import dataclass, field

from LogicalDevices.LogicalNodes.CommonDataClasses.ACD import ACD
from LogicalDevices.LogicalNodes.CommonDataClasses.ASG import ASG
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.BasicTypes.BOOLEAN import BOOLEAN
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.Enum.dirEnum import DirEnum
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.Quality import Quality
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.TimeStamp import TimeStamp
from LogicalDevices.LogicalNodes.CommonDataClasses.WYE import WYE
from LogicalDevices.LogicalNodes.LogicalNodeClass import LogicalNodeClass


@dataclass
class PHAR(LogicalNodeClass):
    """
        Входные данные узла:
         """
    A: WYE = field(init=False)
    HA: WYE = field(init=False)
    PhStr: ASG = field(init=False)

    """
        Выходные данные узла:
         """
    Str: ACD = field(init=False)

    def __post_init__(self):
        self.A = WYE()
        self.HA = WYE()
        self.PhStr = ASG()

    def process(self):

        """
            Проверка превышает ли отношение тока определённой гармоники Iд к первичной гармонике I1 заданную уставку PhStr
        """
        StrPhsA = (self.HA.phsA.cVal.mag.f.value / self.A.phsA.cVal.mag.f.value) >= (self.PhStr.setMag.f.value / 100)
        StrPhsB = (self.HA.phsB.cVal.mag.f.value / self.A.phsB.cVal.mag.f.value) >= (self.PhStr.setMag.f.value / 100)
        StrPhsC = (self.HA.phsC.cVal.mag.f.value / self.A.phsC.cVal.mag.f.value) >= (self.PhStr.setMag.f.value / 100)
        StrLoc = (StrPhsA) or (StrPhsB) or (StrPhsC)

        """
            Формирование выходного сигнала Str: ACD
        """
        self.Str = ACD()
        self.Str.general = BOOLEAN(StrLoc)
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