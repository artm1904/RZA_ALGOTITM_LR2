import csv
from abc import abstractmethod, ABC
from dataclasses import dataclass, field

import comtrade
from matplotlib import pyplot as plt

from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.AnalogueValue import AnalogueValue
from LogicalDevices.LogicalNodes.CommonDataClasses.SAV import SAV


@dataclass
class Parser(ABC):
    cfgFilePath: str
    datFilePath: str
    csvFilePath: str

    @abstractmethod
    def setPaths(self, cfgFilePath: str, datFilePath: str, csvFilePath: str):
        pass

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def parsing(self):
        pass

    @abstractmethod
    def getTime(self):
        pass


@dataclass
class Pasring_Comtrade():
    time_stamp: int = 0
    CurrentA_vn: SAV = field(init=False)  # Тип должен быть SAV
    CurrentB_vn: SAV = field(init=False)
    CurrentC_vn: SAV = field(init=False)

    CurrentA_sn: SAV = field(init=False)  # Тип должен быть SAV
    CurrentB_sn: SAV = field(init=False)
    CurrentC_sn: SAV = field(init=False)

    CurrentA_nn: SAV = field(init=False)  # Тип должен быть SAV
    CurrentB_nn: SAV = field(init=False)
    CurrentC_nn: SAV = field(init=False)

    ia_vn_chanel = []
    ib_vn_chanel = []
    ic_vn_chanel = []

    ia_sn_chanel = []
    ib_sn_chanel = []
    ic_sn_chanel = []

    ia_nn_chanel = []
    ib_nn_chanel = []
    ic_nn_chanel = []

    lg_flt = []

    time = []

    def __post_init__(self):
        self.CurrentA_vn = SAV()
        self.CurrentB_vn = SAV()
        self.CurrentC_vn = SAV()

        self.CurrentA_sn = SAV()
        self.CurrentB_sn = SAV()
        self.CurrentC_sn = SAV()

        self.CurrentA_nn = SAV()
        self.CurrentB_nn = SAV()
        self.CurrentC_nn = SAV()

    def parsing(self):
        rec = comtrade.load(self.cfgFilePath, self.datFilePath)

        if len(rec.analog) <= 8:
            self.ia_vn_chanel = rec.analog[0]
            self.ib_vn_chanel = rec.analog[1]
            self.ic_vn_chanel = rec.analog[2]

            self.ia_sn_chanel = [0.0] * len(rec.time)
            self.ib_sn_chanel = [0.0] * len(rec.time)
            self.ic_sn_chanel = [0.0] * len(rec.time)

            self.ia_nn_chanel = rec.analog[3]
            self.ib_nn_chanel = rec.analog[4]
            self.ic_nn_chanel = rec.analog[5]

            self.lg_flt = [0.0] * len(rec.time)

        else:
            self.ia_vn_chanel = rec.analog[0]
            self.ib_vn_chanel = rec.analog[1]
            self.ic_vn_chanel = rec.analog[2]

            self.ia_sn_chanel = rec.analog[3]
            self.ib_sn_chanel = rec.analog[4]
            self.ic_sn_chanel = rec.analog[5]

            self.ia_nn_chanel = rec.analog[6]
            self.ib_nn_chanel = rec.analog[7]
            self.ic_nn_chanel = rec.analog[8]

            self.lg_flt = [0.0] * len(rec.time)

        self.time = rec.time

        if len(rec.analog) <= 8:
            # Plotting
            plt.figure()
            plt.plot(self.time, self.ia_vn_chanel, label="ia_vn")
            plt.plot(self.time, self.ib_vn_chanel, label="ib_vn")
            plt.plot(self.time, self.ic_vn_chanel, label="ic_vn")

            plt.plot(self.time, self.ia_nn_chanel, label="ia_nn")
            plt.plot(self.time, self.ib_nn_chanel, label="ib_nn")
            plt.plot(self.time, self.ic_nn_chanel, label="ic_nn")

            # Labels and title
            plt.xlabel("Time")
            plt.ylabel("Current")  # Or whatever the units are
            plt.title("Current vs. Time")
            plt.legend()
            plt.savefig("INPUT_REACTOR.png")
        else:
            # Plotting
            plt.figure()
            plt.plot(self.time, self.ia_vn_chanel, label="ia_vn")
            plt.plot(self.time, self.ib_vn_chanel, label="ib_vn")
            plt.plot(self.time, self.ic_vn_chanel, label="ic_vn")

            plt.plot(self.time, self.ia_sn_chanel, label="ia_sn")
            plt.plot(self.time, self.ib_sn_chanel, label="ib_sn")
            plt.plot(self.time, self.ic_sn_chanel, label="ic_sn")

            plt.plot(self.time, self.ia_nn_chanel, label="ia_nn")
            plt.plot(self.time, self.ib_nn_chanel, label="ib_nn")
            plt.plot(self.time, self.ic_nn_chanel, label="ic_nn")

            # Labels and title
            plt.xlabel("Time")
            plt.ylabel("Current")  # Or whatever the units are
            plt.title("Current vs. Time")
            plt.legend()
            plt.savefig("INPUT_3xTrans.png")

    def process(self):
        try:
            # Создаем AnalogueValue для каждого канала, используя FLOAT32 для правильной инициализации
            analogue_a_vn = AnalogueValue()
            analogue_a_vn.f.value = self.ia_vn_chanel[self.time_stamp] * 1000  #Умножаем на 1000
            analogue_b_vn = AnalogueValue()
            analogue_b_vn.f.value = self.ib_vn_chanel[self.time_stamp] * 1000  #Умножаем на 1000
            analogue_c_vn = AnalogueValue()
            analogue_c_vn.f.value = self.ic_vn_chanel[self.time_stamp] * 1000  #Умножаем на 1000

            analogue_a_sn = AnalogueValue()
            analogue_a_sn.f.value = self.ia_sn_chanel[self.time_stamp] * 1000  #Умножаем на 1000
            analogue_b_sn = AnalogueValue()
            analogue_b_sn.f.value = self.ib_sn_chanel[self.time_stamp] * 1000  #Умножаем на 1000
            analogue_c_sn = AnalogueValue()
            analogue_c_sn.f.value = self.ib_sn_chanel[self.time_stamp] * 1000  #Умножаем на 1000



            analogue_a_nn = AnalogueValue()
            analogue_a_nn.f.value = self.ia_nn_chanel[self.time_stamp] * 1000  #Умножаем на 1000
            analogue_b_nn = AnalogueValue()
            analogue_b_nn.f.value = self.ib_nn_chanel[self.time_stamp] * 1000  #Умножаем на 1000
            analogue_c_nn = AnalogueValue()
            analogue_c_nn.f.value = self.ib_nn_chanel[self.time_stamp] * 1000  #Умножаем на 1000


        # Создаем SAV объекты, используя AnalogueValue
            self.CurrentA_vn.instMag = analogue_a_vn
            self.CurrentB_vn.instMag = analogue_b_vn
            self.CurrentC_vn.instMag = analogue_c_vn


            self.CurrentA_sn.instMag = analogue_a_sn
            self.CurrentB_sn.instMag = analogue_b_sn
            self.CurrentC_sn.instMag = analogue_c_sn


            self.CurrentA_nn.instMag = analogue_a_nn
            self.CurrentB_nn.instMag = analogue_b_nn
            self.CurrentC_nn.instMag = analogue_c_nn

            self.time_stamp += 1
            return self.CurrentA_vn, self.CurrentB_vn, self.CurrentB_vn, self.CurrentA_sn, self.CurrentB_sn, self.CurrentC_sn, self.CurrentA_nn, self.CurrentB_nn, self.CurrentC_nn

        except IndexError:
            print(f"IndexError: time_stamp {self.time_stamp} is out of range.")
            return None, None, None
        except TypeError as e:
            print(f"TypeError: {e}")
            return None, None, None
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return None, None, None

    def getTime(self):
        return self.time

    def setPaths(self, cfgFilePath: str, datFilePath: str, csvFilePath: str):
        self.cfgFilePath = cfgFilePath
        self.datFilePath = datFilePath
        self.csvFilePath = csvFilePath


@dataclass
class Pasring_CSV():
    time_stamp: int = 0
    CurrentA: SAV = field(init=False)  # Тип должен быть SAV
    CurrentB: SAV = field(init=False)
    CurrentC: SAV = field(init=False)
    time = []
    ia_chanel = []
    ib_chanel = []
    ic_chanel = []
    ifake_chanel = []

    def __post_init__(self):
        self.CurrentA = SAV()  # Инициализируем как экземпляры SAV
        self.CurrentB = SAV()
        self.CurrentC = SAV()

    def parsing(self):
        with open(self.csvFilePath, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header row

            for row in reader:
                try:
                    # Convert data to numeric types (float)
                    self.time.append(float(row[0]))
                    self.ia_chanel.append(float(row[1]) * 1000)
                    self.ib_chanel.append(float(row[2]) * 1000)
                    self.ic_chanel.append(float(row[3]) * 1000)
                    self.ifake_chanel.append(float(row[4]) * 1000)

                except ValueError:
                    print(f"Skipping row due to invalid {row}")  # Handle potential errors

        # Plotting
        plt.figure()
        plt.plot(self.time, self.ia_chanel, label="ia")
        plt.plot(self.time, self.ib_chanel, label="ib")
        plt.plot(self.time, self.ic_chanel, label="ic")
        plt.plot(self.time, self.ifake_chanel, label="ifake_chanel")
        # Labels and title
        plt.xlabel("Time")
        plt.ylabel("Current")  # Or whatever the units are
        plt.title("Current vs. Time")
        plt.legend()
        plt.savefig("INPUT.png")

    def process(self):
        try:
            # Создаем AnalogueValue для каждого канала, используя FLOAT32 для правильной инициализации
            analogue_a = AnalogueValue()
            analogue_a.f.value = self.ia_chanel[self.time_stamp]
            analogue_b = AnalogueValue()
            analogue_b.f.value = self.ib_chanel[self.time_stamp]
            analogue_c = AnalogueValue()
            analogue_c.f.value = self.ic_chanel[self.time_stamp]

            # Создаем SAV объекты, используя AnalogueValue
            self.CurrentA.instMag = analogue_a
            self.CurrentB.instMag = analogue_b
            self.CurrentC.instMag = analogue_c

            self.time_stamp += 1
            return self.CurrentA, self.CurrentB, self.CurrentC

        except IndexError:
            print(f"IndexError: time_stamp {self.time_stamp} is out of range.")
            return None, None, None
        except TypeError as e:
            print(f"TypeError: {e}")
            return None, None, None
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return None, None, None

    def getTime(self):
        return self.time

    def setPaths(self, cfgFilePath: str, datFilePath: str, csvFilePath: str):
        self.cfgFilePath = cfgFilePath
        self.datFilePath = datFilePath
        self.csvFilePath = csvFilePath
