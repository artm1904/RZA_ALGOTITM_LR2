from dataclasses import dataclass, field
from typing import List

from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.BasicTypes.FLOAT32 import FLOAT32
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.BasicTypes.INT16U import INT16U
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.Quality import Quality
from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.TimeStamp import TimeStamp
from LogicalDevices.LogicalNodes.CommonDataClasses.Vector import Vector


@dataclass
class HWYE:
    q: Quality = field(default_factory=Quality)  # q: Качество
    t: TimeStamp = field(default_factory=TimeStamp)  # t: Временная меткаefault_factory=TimeStam
    phsAHar: List[Vector] = field(init=False)  # Список Vector
    numHar: INT16U = field(init=False)
    numCyc: INT16U = field(init=False)
    evalTm: INT16U = field(init=False)
    frequency: FLOAT32 = field(init=False)


    def __post_init__(self):
        self.phsAHar = [Vector() for _ in range(self.numHar.value)]


# # from ваш_модуль import HWYE, Vector, INT16U  # Укажите правильный путь к вашим классам
#
# # Создаем экземпляр HWYE
# hwye_instance = HWYE(numHar=INT16U(10))  # Например, 10 гармоник
#
# # Теперь phsAHar - это список из 10 объектов Vector
# # Вы можете получить доступ к каждой гармонике:
# first_harmonic = hwye_instance.phsAHar[0]  # Первый вектор гармоники