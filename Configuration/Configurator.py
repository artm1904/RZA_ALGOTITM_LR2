from dataclasses import dataclass

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from LogicalDevices.LD_Ctrl import LDCtrl
from LogicalDevices.LD_PROT import LDProt_MTZ
from LogicalDevices.LogicalNodes.CommonDataClasses.ASG import ASG

from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.AnalogueValue import AnalogueValue

from LogicalDevices.LogicalNodes.CommonDataClasses.CommonDATypes.BasicTypes.INT32 import INT32
from LogicalDevices.LogicalNodes.CommonDataClasses.ING import ING
from LogicalDevices.Parser import Parser
from LogicalDevices.LD_Meas import LDMeasurement_TCTR_Fur, LD_Meas

@dataclass
class LB1:
    cfgFilePath : str
    datFilePath : str
    csvFilePath : str
    stg1Value : float
    stg2Value : float
    stg3Value : float
    stg1Time : int
    stg2Time : int
    stg3Time : int
    ldMeas : LD_Meas
    parser : Parser

    def process(self):
        parser = self.parser
        parser.setPaths(self.cfgFilePath, self.datFilePath, self.csvFilePath)
        parser.parsing()

        ld_meas = self.ldMeas
        ld_ctrl = LDCtrl()
        ld_prot = LDProt_MTZ()

        # Задаем уставки по току и времени для ступеней МТЗ для LDProt_MTZ
        mtz1_I = AnalogueValue()
        mtz1_I.f.value = self.stg1Value  # Или FLOAT(3000), в зависимости от типа
        ags1 = ASG()
        ags1.setMag = mtz1_I
        ld_prot.StrVal_stg1 = ags1

        mtz2_I = AnalogueValue()
        mtz2_I.f.value = self.stg2Value
        ags2 = ASG()
        ags2.setMag = mtz2_I
        ld_prot.StrVal_stg2 = ags2

        mtz3_I = AnalogueValue()
        mtz3_I.f.value = self.stg3Value
        ags3 = ASG()
        ags3.setMag = mtz3_I
        ld_prot.StrVal_stg3 = ags3

        mtz1_t = ING()
        mtz1_t.setVal = INT32(self.stg1Time)
        ld_prot.OPDlTmms_stg1 = mtz1_t

        mtz2_t = ING()
        mtz2_t.setVal = INT32(self.stg2Time)
        ld_prot.OPDlTmms_stg2 = mtz2_t

        mtz3_t = ING()
        mtz3_t.setVal = INT32(self.stg3Time)
        ld_prot.OPDlTmms_stg3 = mtz3_t

        # Инициализация отображаемых массивов
        ia_chanel = []
        ib_chanel = []
        ic_chanel = []
        mtz_1 = [0.0] * 2000  # Инициализируем список mtz_1
        mtz_2 = [0.0] * 2000  # Инициализируем список mtz_2
        mtz_3 = [0.0] * 2000  # Инициализируем список mtz_3
        op_chanel = []
        str_chanel = []

        for i in range(2000):
            parser.process()

            mtz_1[i] = mtz1_I.f.value
            mtz_2[i] = mtz2_I.f.value
            mtz_3[i] = mtz3_I.f.value

            # Получаем значения из parser и присваиваем их ld_meas
            ld_meas.CurrentA.instMag.f.value = parser.CurrentA.instMag.f.value
            ld_meas.CurrentB.instMag.f.value = parser.CurrentB.instMag.f.value
            ld_meas.CurrentC.instMag.f.value = parser.CurrentC.instMag.f.value

            ld_meas.process()

            ia_chanel.append(ld_meas.A.phsA.cVal.mag.f.value)
            ib_chanel.append(ld_meas.A.phsB.cVal.mag.f.value)
            ic_chanel.append(ld_meas.A.phsC.cVal.mag.f.value)

            # Задаем связи между LD (выход LDMeasurement - вход LDProt_MTZ)
            ld_prot.A = ld_meas.A

            ld_prot.process()

            if ld_prot.Op.general.value == True:
                op_chanel.append(1)
            else:
                op_chanel.append(0)

            if ld_prot.Str.general.value == True:
                str_chanel.append(1)
            else:
                str_chanel.append(0)

            # Задаем связи между LD (выход LDProt_MTZ - вход LDCtrl)
            ld_ctrl.Op = ld_prot.Op

            ld_ctrl.process()

        time = parser.getTime()

        # Create subplots
        fig = make_subplots(rows=2, cols=1, subplot_titles=("Current vs. Time", "Logical Signal vs. Time"))

        # Add traces for I_filtered plot
        fig.add_trace(go.Scatter(x=time, y=ia_chanel, mode='lines', name='Ia', marker=dict(color='orange')), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=ib_chanel, mode='lines', name='Ib', marker=dict(color='green')), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=ic_chanel, mode='lines', name='Ic', marker=dict(color='red')), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=mtz_1, mode='lines', name='mtz1', marker=dict(color='black', dash='dash')), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=mtz_2, mode='lines', name='mtz2', marker=dict(color='black', dash='dash')), row=1, col=1)
        fig.add_trace(go.Scatter(x=time, y=mtz_3, mode='lines', name='mtz3', marker=dict(color='black', dash='dash')), row=1, col=1)

        # Add traces for Str + Op plot
        fig.add_trace(go.Scatter(x=time, y=op_chanel, mode='lines', name='Op'), row=2, col=1)
        fig.add_trace(go.Scatter(x=time, y=str_chanel, mode='lines', name='Str'), row=2, col=1)

        # Update layout
        fig.update_layout(
            title_text="RZA Algorithm",
            height=800,
            width=1200,
            showlegend=True
        )

        # Update x and y axes titles
        fig.update_xaxes(title_text="Time", row=1, col=1)
        fig.update_yaxes(title_text="Current", row=1, col=1)
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Logical Signal LD_Prot", row=2, col=1)

        # Save the plot to HTML file
        fig.write_html("RZA_Algorithm_Plot.html")