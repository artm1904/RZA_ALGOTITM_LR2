import csv
from abc import abstractmethod, ABC
from dataclasses import dataclass, field

import comtrade
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
class Pasring_Comtrade(Parser):
    time_stamp: int = 0
    CurrentA_vn: SAV = field(init=False)
    CurrentB_vn: SAV = field(init=False)
    CurrentC_vn: SAV = field(init=False)

    CurrentA_sn: SAV = field(init=False)
    CurrentB_sn: SAV = field(init=False)
    CurrentC_sn: SAV = field(init=False)

    CurrentA_nn: SAV = field(init=False)
    CurrentB_nn: SAV = field(init=False)
    CurrentC_nn: SAV = field(init=False)

    ia_vn_chanel: list[float] = field(default_factory=list)
    ib_vn_chanel: list[float] = field(default_factory=list)
    ic_vn_chanel: list[float] = field(default_factory=list)

    ia_sn_chanel: list[float] = field(default_factory=list)
    ib_sn_chanel: list[float] = field(default_factory=list)
    ic_sn_chanel: list[float] = field(default_factory=list)

    ia_nn_chanel: list[float] = field(default_factory=list)
    ib_nn_chanel: list[float] = field(default_factory=list)
    ic_nn_chanel: list[float] = field(default_factory=list)

    lg_flt: list[float] = field(default_factory=list)

    time: list[float] = field(default_factory=list)

    cfgFilePath: str = ""
    datFilePath: str = ""
    csvFilePath: str = ""

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

        self.ia_vn_chanel = rec.analog[0]
        self.ib_vn_chanel = rec.analog[1]
        self.ic_vn_chanel = rec.analog[2]
        ia_vn_chanel_plot = list(rec.analog[0])
        ib_vn_chanel_plot = list(rec.analog[1])
        ic_vn_chanel_plot = list(rec.analog[2])
        time_plot = list(rec.time)

        if len(rec.analog) <= 8:
            self.ia_sn_chanel = [0.0] * len(rec.time)
            self.ib_sn_chanel = [0.0] * len(rec.time)
            self.ic_sn_chanel = [0.0] * len(rec.time)
            ia_sn_chanel_plot = [0.0] * len(rec.time)
            ib_sn_chanel_plot = [0.0] * len(rec.time)
            ic_sn_chanel_plot = [0.0] * len(rec.time)


            self.ia_nn_chanel = rec.analog[3]
            self.ib_nn_chanel = rec.analog[4]
            self.ic_nn_chanel = rec.analog[5]

            ia_nn_chanel_plot = list(rec.analog[3])
            ib_nn_chanel_plot = list(rec.analog[4])
            ic_nn_chanel_plot = list(rec.analog[5])
        else:
            self.ia_sn_chanel = rec.analog[3]
            self.ib_sn_chanel = rec.analog[4]
            self.ic_sn_chanel = rec.analog[5]

            ia_sn_chanel_plot = list(rec.analog[3])
            ib_sn_chanel_plot = list(rec.analog[4])
            ic_sn_chanel_plot = list(rec.analog[5])

            self.ia_nn_chanel = rec.analog[6]
            self.ib_nn_chanel = rec.analog[7]
            self.ic_nn_chanel = rec.analog[8]

            ia_nn_chanel_plot = list(rec.analog[6])
            ib_nn_chanel_plot = list(rec.analog[7])
            ic_nn_chanel_plot = list(rec.analog[8])

        self.lg_flt = [0.0] * len(rec.time)

        # Create plot
        fig = go.Figure()

        # Add traces
        fig.add_trace(go.Scatter(x=time_plot, y=ia_vn_chanel_plot, mode='lines', name='ia_vn'))
        fig.add_trace(go.Scatter(x=time_plot, y=ib_vn_chanel_plot, mode='lines', name='ib_vn'))
        fig.add_trace(go.Scatter(x=time_plot, y=ic_vn_chanel_plot, mode='lines', name='ic_vn'))

        if len(rec.analog) <= 8:
            fig.add_trace(go.Scatter(x=time_plot, y=ia_nn_chanel_plot, mode='lines', name='ia_nn'))
            fig.add_trace(go.Scatter(x=time_plot, y=ib_nn_chanel_plot, mode='lines', name='ib_nn'))
            fig.add_trace(go.Scatter(x=time_plot, y=ic_nn_chanel_plot, mode='lines', name='ic_nn'))
        else:
            fig.add_trace(go.Scatter(x=time_plot, y=ia_sn_chanel_plot, mode='lines', name='ia_sn'))
            fig.add_trace(go.Scatter(x=time_plot, y=ib_sn_chanel_plot, mode='lines', name='ib_sn'))
            fig.add_trace(go.Scatter(x=time_plot, y=ic_sn_chanel_plot, mode='lines', name='ic_sn'))
            fig.add_trace(go.Scatter(x=time_plot, y=ia_nn_chanel_plot, mode='lines', name='ia_nn'))
            fig.add_trace(go.Scatter(x=time_plot, y=ib_nn_chanel_plot, mode='lines', name='ib_nn'))
            fig.add_trace(go.Scatter(x=time_plot, y=ic_nn_chanel_plot, mode='lines', name='ic_nn'))

        # Update layout
        fig.update_layout(
            title="Current vs. Time",
            xaxis_title="Time",
            yaxis_title="Current"
        )

        fig.write_html("INPUT_COMTRADE.html")

    def process(self):
        try:
            analogue_a_vn = AnalogueValue()
            analogue_a_vn.f.value = self.ia_vn_chanel[self.time_stamp] * 1000
            analogue_b_vn = AnalogueValue()
            analogue_b_vn.f.value = self.ib_vn_chanel[self.time_stamp] * 1000
            analogue_c_vn = AnalogueValue()
            analogue_c_vn.f.value = self.ic_vn_chanel[self.time_stamp] * 1000

            analogue_a_sn = AnalogueValue()
            analogue_a_sn.f.value = self.ia_sn_chanel[self.time_stamp] * 1000
            analogue_b_sn = AnalogueValue()
            analogue_b_sn.f.value = self.ib_sn_chanel[self.time_stamp] * 1000
            analogue_c_sn = AnalogueValue()
            analogue_c_sn.f.value = self.ic_sn_chanel[self.time_stamp] * 1000

            analogue_a_nn = AnalogueValue()
            analogue_a_nn.f.value = self.ia_nn_chanel[self.time_stamp] * 1000
            analogue_b_nn = AnalogueValue()
            analogue_b_nn.f.value = self.ib_nn_chanel[self.time_stamp] * 1000
            analogue_c_nn = AnalogueValue()
            analogue_c_nn.f.value = self.ic_nn_chanel[self.time_stamp] * 1000

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
            return None, None, None, None, None, None, None, None, None
        except TypeError as e:
            print(f"TypeError: {e}")
            return None, None, None, None, None, None, None, None, None
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return None, None, None, None, None, None, None, None, None

    def getTime(self):
        return self.time

    def setPaths(self, cfgFilePath: str, datFilePath: str, csvFilePath: str):
        self.cfgFilePath = cfgFilePath
        self.datFilePath = datFilePath
        self.csvFilePath = csvFilePath


@dataclass
class Pasring_CSV(Parser):
    time_stamp: int = 0
    CurrentA: SAV = field(init=False)
    CurrentB: SAV = field(init=False)
    CurrentC: SAV = field(init=False)
    time: list[float] = field(default_factory=list)
    ia_chanel: list[float] = field(default_factory=list)
    ib_chanel: list[float] = field(default_factory=list)
    ic_chanel: list[float] = field(default_factory=list)
    ifake_chanel: list[float] = field(default_factory=list)

    cfgFilePath: str = ""
    datFilePath: str = ""
    csvFilePath: str = ""

    def __post_init__(self):
        self.CurrentA = SAV()
        self.CurrentB = SAV()
        self.CurrentC = SAV()

    def parsing(self):
        with open(self.csvFilePath, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header row

            for row in reader:
                try:
                    self.time.append(float(row[0]))
                    self.ia_chanel.append(float(row[1]) * 1000)
                    self.ib_chanel.append(float(row[2]) * 1000)
                    self.ic_chanel.append(float(row[3]) * 1000)
                    self.ifake_chanel.append(float(row[4]) * 1000)
                except ValueError:
                    print(f"Skipping row due to invalid {row}")

        # Create plot
        fig = go.Figure()

        # Add traces
        fig.add_trace(go.Scatter(x=self.time, y=self.ia_chanel, mode='lines', name='ia'))
        fig.add_trace(go.Scatter(x=self.time, y=self.ib_chanel, mode='lines', name='ib'))
        fig.add_trace(go.Scatter(x=self.time, y=self.ic_chanel, mode='lines', name='ic'))
        fig.add_trace(go.Scatter(x=self.time, y=self.ifake_chanel, mode='lines', name='ifake_chanel'))

        # Update layout
        fig.update_layout(
            title="Current vs. Time",
            xaxis_title="Time",
            yaxis_title="Current"
        )

        fig.write_html("INPUT_CSV.html")

    def process(self):
        try:
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