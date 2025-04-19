import math
from dataclasses import dataclass, field

from LogicalDevices.LogicalNodes.CommonDataClasses.CMV import CMV
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.BasicTypes.BOOLEAN import BOOLEAN
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.Enum.dirEnum import DirEnum
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.Quality import Quality
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.TimeStamp import TimeStamp
from LogicalDevices.LogicalNodes.CommonDataClasses.SAV import SAV
from LogicalDevices.LogicalNodes.CommonDataClasses.WYE import WYE
from LogicalDevices.LogicalNodes.LogicalNodeClass import LogicalNodeClass


@dataclass
class RMXU(LogicalNodeClass):
    """
        Входные данные узла:
    """
    A1: WYE = field(init=False)
    A2: WYE = field(init=False)
    A3: WYE = field(init=False)

    """
        Выходные данные узла:
    """
    pARem: WYE = field(init=False)
    ARes: WYE = field(init=False)
    Amp1: SAV = field(init=False)
    Amp2: SAV = field(init=False)
    Amp3: SAV = field(init=False)

    def __post_init__(self):
        self.A1 = WYE()
        self.A2 = WYE()
        self.A3 = WYE()

    def polar_to_decart(r, angle):
        """
            Преобразование полярных координат (значений длины вектора r и его угла angle) в декартовы (x, y)
        """
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        return x, y

    def decart_to_polar(x, y):
        """
            Преобразование декартовых координат (x, y) в полярные (r, angle)
        """
        r = math.sqrt(x ** 2 + y ** 2)
        angle = math.atan2(y, x)  # atan2 обрабатывает все квадранты
        return r, angle

    def process(self):
        """
            Преобразование полярных координат (значений длины вектора и его угла) в декартовы (x, y)
        """
        "Сторона ВН"
        A1_phA_x, A1_phA_y = self.polar_to_decart(self.A1.phsA.cVal.mag.f.value, self.A1.phsA.cVal.ang.f.value)
        A1_phB_x, A1_phB_y = self.polar_to_decart(self.A1.phsB.cVal.mag.f.value, self.A1.phsB.cVal.ang.f.value)
        A1_phC_x, A1_phC_y = self.polar_to_decart(self.A1.phsC.cVal.mag.f.value, self.A1.phsC.cVal.ang.f.value)

        "Сторона СН"
        A2_phA_x, A2_phA_y = self.polar_to_decart(self.A2.phsA.cVal.mag.f.value, self.A2.phsA.cVal.ang.f.value)
        A2_phB_x, A2_phB_y = self.polar_to_decart(self.A2.phsB.cVal.mag.f.value, self.A2.phsB.cVal.ang.f.value)
        A2_phC_x, A2_phC_y = self.polar_to_decart(self.A2.phsC.cVal.mag.f.value, self.A2.phsC.cVal.ang.f.value)

        "Сторона НН"
        A3_phA_x, A3_phA_y = self.polar_to_decart(self.A3.phsA.cVal.mag.f.value, self.A3.phsA.cVal.ang.f.value)
        A3_phB_x, A3_phB_y = self.polar_to_decart(self.A3.phsB.cVal.mag.f.value, self.A3.phsB.cVal.ang.f.value)
        A3_phC_x, A3_phC_y = self.polar_to_decart(self.A3.phsC.cVal.mag.f.value, self.A3.phsC.cVal.ang.f.value)

        """
        Нахождение дифференциального тока 
        """
        "Фаза A"
        A1_phA_diff_Mag, A1_phA_diff_ang = self.decart_to_polar(A1_phA_x + A2_phA_x + A3_phA_x,
                                                                A1_phA_y + A2_phA_y + A3_phA_y)
        "Фаза B"
        A1_phB_diff_Mag, A1_phB_diff_ang = self.decart_to_polar(A1_phB_x + A2_phB_x + A3_phB_x,
                                                                A1_phB_y + A2_phB_y + A3_phB_y)
        "Фаза C"
        A1_phC_diff_Mag, A1_phC_diff_ang = self.decart_to_polar(A1_phC_x + A2_phC_x + A3_phC_x,
                                                                A1_phC_y + A2_phC_y + A3_phC_y)

        """
        Нахождение тормозного тока 
        """
        "Фаза A"
        ResAPhsA = self.A1.phsA.cVal.mag.f.value + self.A2.phsA.cVal.mag.f.value + self.A3.phsA.cVal.mag.f.value
        "Фаза B"
        ResAPhsB = self.A1.phsB.cVal.mag.f.value + self.A2.phsB.cVal.mag.f.value + self.A3.phsB.cVal.mag.f.value
        "Фаза C"
        ResAPhsC = self.A1.phsC.cVal.mag.f.value + self.A2.phsC.cVal.mag.f.value + self.A3.phsC.cVal.mag.f.value

        """
            Формирование выходного сигнала pARem: WYE
        """
        "Фаза A"
        self.pARem.phsA = CMV()  # Создаем экземпляр CMV для phsA
        self.pARem.phsA.cVal.mag.f.value = A1_phA_diff_Mag # Устанавливаем значения
        self.pARem.phsA.cVal.ang.f.value = A1_phA_diff_ang

        "Фаза B"
        self.pARem.phsB = CMV()  # Создаем экземпляр CMV для phsA
        self.pARem.phsB.cVal.mag.f.value = A1_phB_diff_Mag  # Устанавливаем значения
        self.pARem.phsB.cVal.ang.f.value = A1_phB_diff_ang

        "Фаза C"
        self.pARem.phsC = CMV()  # Создаем экземпляр CMV для phsA
        self.pARem.phsC.cVal.mag.f.value = A1_phC_diff_Mag  # Устанавливаем значения
        self.pARem.phsC.cVal.ang.f.value = A1_phC_diff_ang

        self.ARes = WYE()
        self.ARes.general = BOOLEAN(ResAPhsA or ResAPhsB or ResAPhsC)
        self.ARes.phsA = BOOLEAN(ResAPhsA)
        self.ARes.phsB = BOOLEAN(ResAPhsB)
        self.ARes.phsC = BOOLEAN(ResAPhsC)
        self.ARes.neut = BOOLEAN(False)
        self.ARes.dirGeneral = DirEnum.UNKNOWN
        self.ARes.dirPhsA = DirEnum.UNKNOWN
        self.ARes.dirPhsB = DirEnum.UNKNOWN
        self.ARes.dirPhsC = DirEnum.UNKNOWN
        self.ARes.dirNeut = DirEnum.UNKNOWN
        self.ARes.q = Quality()
        self.ARes.t = TimeStamp()

