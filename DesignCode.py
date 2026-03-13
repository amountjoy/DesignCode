# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 15:06:02 2025

@author: MOUNTJA
"""

import pandas as pd
import math
from IPython.display import display, Math, Latex
from IPython.display import Image as IPImage
from PIL import Image
import pint

# Create a global unit registry
ureg = pint.UnitRegistry()
ureg.load_definitions('Units.txt')

class Utilities:
    
    def __init__(self):
        self.ureg=ureg
        return    

    def DispImage(self, File_Path, width=None, height=None):
        display(IPImage(filename=File_Path, width=width, height=height))
        return
    
    def strain(self, E, sigma):
        if not hasattr(E, 'dimensionality'):
            E=E*self.ureg.MPa
        if not hasattr(sigma, 'dimensionality'):
            sigma=sigma*self.ureg.MPa
        
        equation = sigma / E
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{\sigma}{E}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2e} \\]"))
        return equation
    
    def highlight_cells(self, x, highlight_coords):
        df = pd.DataFrame("", index=x.index, columns=x.columns)
        
        for row, col in highlight_coords:
            df.loc[row, col] = "background-color: yellow"
            
        return df


class BlueBook:
    
    def __init__(self, file_path="UC-secpropsdimsprops-EC3UKNA-UK.csv", index_col=0):
        self.df = self.import_data(file_path, index_col)
        
    def import_data(self, file_path=None, index_col=0):
        """
        Imports data from a CSV file into a DataFrame.
    
        Parameters:
        file_path (str): The path to the CSV file.
        index_col (str): The column to set as the index. Default is column 0.
    
        Returns:
        DataFrame: The imported data as a pandas DataFrame.
        """
        df = pd.read_csv(file_path, header=0, index_col=index_col)
        return df
    
class BS_EN_1993_1_1:
    
    def __init__(self):
        # self.ureg = pint.UnitRegistry()
        # self.ureg.load_definitions('Units.txt') 
        self.ureg=ureg
        self.Table_5_1_data=self.import_data(file_path="Table 5.1.csv", index_col=0)
        self.Table_8_4_data=self.import_data(file_path="Table 8.4.csv", index_col=0)
        return
    
    def import_data(self, file_path=None, index_col=0):
        """
        Imports data from a CSV file into a DataFrame.
    
        Parameters:
        file_path (str): The path to the CSV file.
        index_col (str): The column to set as the index. Default is column 0.
    
        Returns:
        DataFrame: The imported data as a pandas DataFrame.
        """
        df = pd.read_csv(file_path, header=0, index_col=index_col)
        return df
             
    def fy(self, tf, tw, Grade):
        if not hasattr(tf, 'dimensionality'):
            tf=tf*self.ureg.meter
        if not hasattr(tw, 'dimensionality'):
            tw=tw*self.ureg.meter 
        # tf = Section["tf (mm)"]
        # tw = Section["tw (mm)"]
        max_t=max(tf, tw)

        if max_t.magnitude<=0.040:
            result = self.Table_5_1_data.loc[Grade,"fy (≤40mm) (N/mm²)"]
        elif max_t.magnitude>0.040 and max_t.magnitude<=0.080:
            result = self.Table_5_1_data.loc[Grade,"fy (40<t≤80mm) (N/mm²)"]
        result = result*self.ureg.MPa
        return result
    
    def fu(self, tf, tw, Grade):
        if not hasattr(tf, 'dimensionality'):
            tf=tf*self.ureg.meter
        if not hasattr(tw, 'dimensionality'):
            tw=tw*self.ureg.meter      
        
        # tf = Section["tf (mm)"]
        # tw = Section["tw (mm)"]
        max_t=max(tf, tw)
    
        if max_t.magnitude<=0.040:
            result = self.Table_5_1_data.loc[Grade,"fu (≤40mm) (N/mm²)"]
        elif max_t.magnitude>0.040 and max_t.magnitude<=0.080:
            result = self.Table_5_1_data.loc[Grade,"fu (40<t≤80mm) (N/mm²)"]
        result = result*self.ureg.MPa
        return result
            
    def eqn_5_1(self, fy):
        if not hasattr(fy, 'dimensionality'):
            fy = fy * self.ureg.MPa
        numerator = 235
        numerator = numerator*self.ureg.MPa
        equation = (numerator / fy) ** 0.5
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\left( \frac{235}{f_y} \right)^{0.5}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\]"))
        return equation
    
    def Table_7_3(self, c_t, epsilon):
        if c_t<=72*epsilon:
            return 1
        elif c_t<=83*epsilon:
            return 2
        elif c_t<=121*epsilon:
            return 3
        else:
            return 4
        
    def Table_7_4(self, c_t, epsilon):
        if c_t<=9*epsilon:
            return 1
        elif c_t<=10*epsilon:
            return 2
        elif c_t<=14*epsilon:
            return 3
        else:
            return 4
        
    def Eqn_8_11(self, Wy, fy):
        
        if not hasattr(Wy, 'dimensionality'):
            Wy = Wy*self.ureg.meter**3
        if not hasattr(fy, 'dimensionality'):
            fy = fy * self.ureg.MPa
            
        equation = Wy*fy
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"W_y \cdot f_y"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.to(self.ureg.kNm):.2f} \\]"))
        return equation.to(self.ureg.kNm)
    
    def Eqn_8_12(self, Wz, fy):
        if not hasattr(Wz, 'dimensionality'):
            Wz = Wz*self.ureg.meter**3
        # Check if fy has a unit, if not assign MPa
        if not hasattr(fy, 'dimensionality'):
            fy = fy * self.ureg.MPa
        equation = Wz*fy
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"W_z \cdot f_y"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.to(self.ureg.kNm):.2f} \\]"))
        return equation.to(self.ureg.kNm)
    
    def Eqn_8_20(self, M_Rk,g_M_0=1):
        if not hasattr(M_Rk, 'dimensionality'):
            M_Rk = M_Rk*self.ureg.kNm
        equation = M_Rk/g_M_0
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{M_{Rk}}{\gamma_{M0}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def Eqn_8_19 (self, M_Ed, M_c_Rd):
        if not hasattr(M_Ed, 'dimensionality'):
            M_Ed = M_Ed*self.ureg.kNm
        if not hasattr(M_c_Rd, 'dimensionality'):
            M_c_Rd = M_c_Rd*self.ureg.kNm
        equation=M_Ed/M_c_Rd
        if equation>1:
            Verification="Fail"
        else:
            Verification="Pass"
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{M_{Ed}}{M_{c,Rd}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\] {Verification}"))
        return equation, Verification
    
    def M_cr(self, L_cr, E, I_z, I_w, G, I_t):
        
        if not hasattr(L_cr, 'dimensionality'):
            L_cr = L_cr * self.ureg.meter
        if not hasattr(E, 'dimensionality'):
            E = E * self.ureg.megapascal
        if not hasattr(I_z, 'dimensionality'):
            I_z = I_z * self.ureg.m**4
        if not hasattr(I_w, 'dimensionality'):
            I_w = I_w * self.ureg.m**6
        if not hasattr(G, 'dimensionality'):
            G = G * self.ureg.megapascal
        if not hasattr(I_t, 'dimensionality'):
            I_t = I_t * self.ureg.m**4
        
        equation = math.pi**2*E*I_z/(L_cr**2)*((I_w/I_z)+(L_cr**2*G*I_t)/(math.pi**2*E*I_z))**0.5
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{\pi^2 \cdot E \cdot I_z}{L_{cr}^2} \cdot \left(\frac{I_w}{I_z}+\frac{L_{cr}^2 \cdot G \cdot I_t}{\pi^2 \cdot E \cdot I_z}\right)^{0.5}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.to(self.ureg.kNm):.2f} \\]"))
        return equation.to(self.ureg.kNm)
    
    def Eqn_8_80(self, M_Rk, M_cr):
        
        if not hasattr(M_Rk, 'dimensionality'):
            M_Rk = M_Rk*self.ureg.kNm
        if not hasattr(M_cr, 'dimensionality'):
            M_cr = M_cr*self.ureg.kNm
            
        equation = (M_Rk/M_cr)**0.5
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\sqrt{\left(\frac{M_{Rk}}{M_{cr}}\right)}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\]"))
        
        return equation
    
    def Table_8_4(self, h, b_min, type="Rolled I or H sections"):
        display(IPImage(filename="Table 8.4.png"))
        if type=="Rolled I or H sections":
            if h/b_min<=2:
                return "LTB curve a"
            else:
                return "LTB curve b"
        elif type=="Welded I-setions":
            if h/b_min<=2:
                return "LTB curve c"
            else:
                return "LTB curve d"
        else:
            return "LTB curve d"
        
    def Table_8_5(self, h, b, t_f, W_el_y, W_el_z, type="Rolled I or H sections"):
        display(IPImage(filename="Table 8.5.png"))
        if not hasattr(t_f, 'dimensionality'):
            t_f = t_f*self.ureg.m
        if not hasattr(W_el_y, 'dimensionality'):
            W_el_y = W_el_y*self.ureg.m**3
        if not hasattr(W_el_z, 'dimensionality'):
            W_el_z = W_el_z*self.ureg.m**3
        if type=="Rolled I or H sections":
            if h/b>1.2:
                if t_f<=0.04:
                    return min(0.34, 0.12*(W_el_y/W_el_z)**0.5)
                else:
                    return min(0.49, 0.16*(W_el_y/W_el_z)**0.5)
            else:
                return min(0.49, 0.16*(W_el_y/W_el_z)**0.5)
        elif type=="Welded I sections":
            if t_f<=0.040:
                return min(0.64, 0.21*(W_el_y/W_el_z)**0.5)
            else:
                return min(0.76, 0.25*(W_el_y/W_el_z)**0.5)
            
    def Eqn_8_72(self, epsilon):
        if not hasattr(epsilon, 'dimensionality'):
            epsilon = epsilon * self.ureg.dimensionless
        equation = 93.9*epsilon
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"93.9 \cdot \epsilon"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\]"))
        return equation
    
    def Eqn_8_70(self, L_cr, i, lambda_1):
        if not hasattr(L_cr, 'dimensionality'):
            L_cr = L_cr * self.ureg.meter
        if not hasattr(i, 'dimensionality'):
            i = i * self.ureg.meter
        if not hasattr(lambda_1, 'dimensionality'):
            lambda_1 = lambda_1 * self.ureg.dimensionless
        equation = (L_cr/i)*(1/lambda_1)
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{L_{cr}}{i} \cdot \frac{1}{\lambda_1}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\]"))
        return equation
    
    def Eqn_8_82(self, fM, lambda_bar_LT, lambda_bar_z, alpha_LT):
        if not hasattr(fM, 'dimensionality'):
            fM = fM * self.ureg.dimensionless
        if not hasattr(lambda_bar_LT, 'dimensionality'):
            lambda_bar_LT = lambda_bar_LT * self.ureg.dimensionless
        if not hasattr(lambda_bar_z, 'dimensionality'):
            lambda_bar_z = lambda_bar_z * self.ureg.dimensionless
        if not hasattr(alpha_LT,'dimensionality'):
            alpha_LT = alpha_LT * self.ureg.dimensionless
            
        equation = 0.5*(1+fM*(((lambda_bar_LT/lambda_bar_z)**2)*alpha_LT*(lambda_bar_z-0.2)+lambda_bar_LT**2))
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"0.5 \cdot \left(1+f_M\left(\left(\frac{\bar{\lambda}_{LT}}{\bar{\lambda}_z}\right)^2 \cdot \alpha_{LT} \cdot \left(\bar{\lambda}_z-0.2\right)+\bar{\lambda}_{LT}^2\right)\right)"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\]"))
        return equation
    
    def Eqn_8_81(self, fM, phi_LT, lambda_bar_LT):
        if not hasattr(fM, 'dimensionality'):
            fM = fM * self.ureg.dimensionless
        if not hasattr(phi_LT, 'dimensionality'):
            phi_LT = phi_LT * self.ureg.dimensionless
        if not hasattr(lambda_bar_LT, 'dimensionality'):
            lambda_bar_LT = lambda_bar_LT * self.ureg.dimensionless
            
        equation = min(1, fM/(phi_LT+(phi_LT**2-fM*lambda_bar_LT**2)**0.5))
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{f_M}{\phi_{LT}+\sqrt{\phi_{LT}^2-f_M \cdot \bar{\lambda}_{LT}^2}} \qquad but \qquad \chi_{LT} \leq 1"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\]"))
        return equation
    
    def Eqn_8_79(self, chi_LT, M_Rk, gamma_M1=1):
        if not hasattr(chi_LT, 'dimensionality'):
            chi_LT = chi_LT * self.ureg.dimensionless
        if not hasattr(M_Rk, 'dimensionality'):
            M_Rk = M_Rk * self.ureg.kNm
        if not hasattr(gamma_M1, 'dimensionality'):
            gamma_M1 = gamma_M1 * self.ureg.dimensionless
            
        equation = chi_LT*(M_Rk/gamma_M1)
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\chi_{LT} \cdot \frac{M_{Rk}}{\gamma_{M1}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def Eqn_8_78(self, M_Ed, M_b_Rd):
        if not hasattr(M_Ed, 'dimensionality'):
            M_Ed = M_Ed*self.ureg.kNm
        if not hasattr(M_b_Rd, 'dimensionality'):
            M_b_Rd = M_b_Rd*self.ureg.kNm
        equation=M_Ed/M_b_Rd
        if equation>1:
            Verification="Fail"
        else:
            Verification="Pass"
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{M_{Ed}}{M_{b,Rd}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\] {Verification}"))
        return equation, Verification
    
    def Eqn_8_14(self, A, fy, gamma_M0=1):
        if not hasattr(A, 'dimensionality'):
            A = A * self.ureg.meter**2
        if not hasattr(fy, 'dimensionality'):
            fy = fy * self.ureg.megapascal
        if not hasattr(gamma_M0, 'dimensionality'):
            gamma_M0 = gamma_M0 * self.ureg.dimensionless
        equation = A*fy/gamma_M0
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{A \cdot f_y}{\gamma_{M0}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.to(self.ureg.kN):.2f} \\]"))
        return equation.to(self.ureg.kN)
    
    def Eqn_8_13(self, N_Ed, N_t_Rd):
        if not hasattr(N_Ed, 'dimensionality'):
            N_Ed = N_Ed * self.ureg.kN
        if not hasattr(N_t_Rd, 'dimensionality'):
            N_t_Rd = N_t_Rd * self.ureg.kN
        equation=N_Ed/N_t_Rd
        if equation>1:
            Verification="Fail"
        else:
            Verification="Pass"
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{N_{Ed}}{N_{t,Rd}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\] {Verification}"))
        return equation, Verification
    
    def Eqn_8_18(self, A, fy, gamma_M0=1):
        if not hasattr(A, 'dimensionality'):
            A = A * self.ureg.meter**2
        if not hasattr(fy, 'dimensionality'):
            fy = fy * self.ureg.megapascal
        if not hasattr(gamma_M0, 'dimensionality'):
            gamma_M0 = gamma_M0 * self.ureg.dimensionless
        equation = A*fy/gamma_M0
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{A \cdot f_y}{\gamma_{M0}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.to(self.ureg.kN):.2f} \\]"))
        return equation.to(self.ureg.kN)
    
    def Eqn_8_17(self, N_Ed, N_c_Rd):
        if not hasattr(N_Ed, 'dimensionality'):
            N_Ed = N_Ed * self.ureg.kN
        if not hasattr(N_c_Rd, 'dimensionality'):
            N_c_Rd = N_c_Rd * self.ureg.kN
        equation=N_Ed/N_c_Rd
        if equation>1:
            Verification="Fail"
        else:
            Verification="Pass"
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{N_{Ed}}{N_{c,Rd}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\] {Verification}"))
        return equation, Verification
        
    def Eqn_8_23(self, Av, fy, gamma_M0=1):
        if not hasattr(Av, 'dimensionality'):
            Av = Av * self.ureg.meter**2
        if not hasattr(fy, 'dimensionality'):
            fy = fy * self.ureg.megapascal
        if not hasattr(gamma_M0, 'dimensionality'):
            gamma_M0 = gamma_M0 * self.ureg.dimensionless
        equation = Av*(fy/(3**0.5))/gamma_M0
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{A_v\left(\frac{f_y}{\sqrt{3}}\right)}{\gamma_{M0}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.to(self.ureg.kN):.2f} \\]"))
        return equation.to(self.ureg.kN)
    
    def Eqn_8_22(self, V_Ed, V_c_Rd):
        if not hasattr(V_Ed, 'dimensionality'):
            V_Ed = V_Ed * self.ureg.kN
        if not hasattr(V_c_Rd, 'dimensionality'):
            V_c_Rd = V_c_Rd * self.ureg.kN
        equation=V_Ed/V_c_Rd
        if equation>1:
            Verification="Fail"
        else:
            Verification="Pass"
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{V_{Ed}}{V_{c,Rd}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\] {Verification}"))
        return equation, Verification

    def Av(self, A, b, tf, tw, r, eta, hw):
        #Currently only for doubly symmetric rolled I and H sections
        if not hasattr(A, 'dimensionality'):
            A = A * self.ureg.m**2
        if not hasattr(b, 'dimensionality'):
            b = b * self.ureg.m
        if not hasattr(tf, 'dimensionality'):
            tf = tf * self.ureg.m
        if not hasattr(tw, 'dimensionality'):
            tw = tw * self.ureg.m
        if not hasattr(r, 'dimensionality'):
            r = r * self.ureg.m
        if not hasattr(eta, 'dimensionality'):
            eta = eta * self.ureg.dimensionless
        if not hasattr(hw, 'dimensionality'):
            hw = hw * self.ureg.m
            
        equation = max(A-2*b*tf+(tw+2*r)*tf, eta*hw*tw)
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"A-2 \cdot b \cdot t_f+(t_w+2 \cdot r) \cdot t_f \geq \eta \cdot h_w \cdot t_w"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def Table_8_2(self, buckling_curve):
        display(IPImage(filename="Table 8.2.png"))
        if buckling_curve=="a0" or buckling_curve=="Buckling curve a0":
            return 0.13
        if buckling_curve=="a" or buckling_curve=="Buckling curve a":
            return 0.21
        if buckling_curve=="b" or buckling_curve=="Buckling curve b":
            return 0.34
        if buckling_curve=="c" or buckling_curve=="Buckling curve c":
            return 0.49
        if buckling_curve=="d" or buckling_curve=="Buckling curve d":
            return 0.76
        
    def Table_8_3(self, h, b, tf, grade, buckling_axis="z-z", type="Rolled I or H sections"):
        #Currently just for Rolled I or H sections
        display(IPImage(filename="Table 8.3 part 1.png"))
        display(IPImage(filename="Table 8.3 part 2.png"))
        if type=="Rolled I or H sections":
            if h/b>1.2:
                if tf<=0.04:
                    if buckling_axis=="z-z":
                        if grade=="S235" or grade=="S275" or grade=="S355" or grade=="S420":
                            return "Buckling curve b"
                        else:
                            return "Buckling curve a"
                    else:
                        if grade=="S235" or grade=="S275" or grade=="S355" or grade=="S420":
                            return "Buckling curve a"
                        else:
                            return "Buckling curve a0"
                else:
                    if buckling_axis=="z-z":
                        if grade=="S235" or grade=="S275" or grade=="S355" or grade=="S420":
                            return "Buckling curve c"
                        else:
                            return "Buckling curve b"
                    else:
                        if grade=="S235" or grade=="S275" or grade=="S355" or grade=="S420":
                            return "Buckling curve b"
                        else:
                            return "Buckling curve a"
            else:
                if tf<=0.1:
                    if buckling_axis=="z-z":
                        if grade=="S235" or grade=="S275" or grade=="S355" or grade=="S420":
                            return "Buckling curve c"
                        else:
                            return "Buckling curve b"
                    else:
                        if grade=="S235" or grade=="S275" or grade=="S355" or grade=="S420":
                            return "Buckling curve b"
                        else:
                            return "Buckling curve a"
                else:
                    if buckling_axis=="z-z":
                        if grade=="S235" or grade=="S275" or grade=="S355" or grade=="S420":
                            return "Buckling curve d"
                        else:
                            return "Buckling curve c"
                    else:
                        if grade=="S235" or grade=="S275" or grade=="S355" or grade=="S420":
                            return "Buckling curve d"
                        else:
                            return "Buckling curve c"
                        
    def Eqn_8_74(self, alpha, lambda_bar):
        if not hasattr(alpha, 'dimensionality'):
            alpha = alpha * self.ureg.dimensionless
        if not hasattr(lambda_bar, 'dimensionality'):
            lambda_bar = lambda_bar * self.ureg.dimensionless
            
        equation = 0.5*(1+alpha*(lambda_bar-0.2)+lambda_bar**2)
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"0.5 \cdot \left(1+\alpha \cdot \left(\bar{\lambda}-0.2\right)+\bar{\lambda}^2\right)"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\]"))
        return equation
    
    def Eqn_8_73(self, phi, lambda_bar):

        if not hasattr(phi, 'dimensionality'):
            phi = phi * self.ureg.dimensionless
        if not hasattr(lambda_bar, 'dimensionality'):
            lambda_bar = lambda_bar * self.ureg.dimensionless
            
        equation = min(1, 1/(phi+(phi**2-lambda_bar**2)**0.5))
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{1}{\phi+\sqrt{\phi^2-\bar{\lambda}^2}} \qquad but \qquad \chi \leq 1"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\]"))
        return equation
    
    def Eqn_8_68(self, chi, A, fy, gamma_M1=1):
        
        if not hasattr(chi, 'dimensionality'):
            chi = chi * self.ureg.dimensionless
        if not hasattr(A, 'dimensionality'):
            A = A * self.ureg.m**2
        if not hasattr(fy, 'dimensionality'):
            fy = fy * self.ureg.MPa
        if not hasattr(gamma_M1, 'dimensionality'):
            gamma_M1 = gamma_M1 * self.ureg.dimensionless
        
        equation = chi*A*fy/gamma_M1
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{\chi \cdot A \cdot f_y}{\gamma_{M1}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.to(self.ureg.kN):.2f} \\]"))
        return equation.to(self.ureg.kN)

    def Eqn_8_67(self, N_Ed, N_b_Rd):
        if not hasattr(N_Ed, 'dimensionality'):
            N_Ed = N_Ed * self.ureg.kN
        if not hasattr(N_b_Rd, 'dimensionality'):
            N_b_Rd = N_b_Rd * self.ureg.kN
        equation=N_Ed/N_b_Rd
        if equation>1:
            Verification="Fail"
        else:
            Verification="Pass"
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{N_{Ed}}{N_{b,Rd}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\] {Verification}"))
        return equation, Verification
    
    def Eqn_8_27(self, hw, tw, epsilon, eta):
        if not hasattr(hw, 'dimensionality'):
            hw = hw * self.ureg.m
        if not hasattr(tw, 'dimensionality'):
            tw = tw * self.ureg.m
        if not hasattr(epsilon, 'dimensionality'):
            epsilon = epsilon * self.ureg.dimensionless
        if not hasattr(eta, 'dimensionality'):
            eta = eta * self.ureg.dimensionless
        
        equation_LHS=hw/tw
        equation_RHS=72*epsilon/eta
        if equation_LHS>equation_RHS:
            Verification=True
        else:
            Verification=False
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{h_w}{t_w} \leq 72 \cdot \frac{\epsilon}{\eta}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation_LHS.magnitude:.2f} \\] \\[ {equation_RHS.magnitude:.2f} \\] {Verification}"))
        return equation_LHS, equation_RHS, Verification
            
    def Eqn_8_88(self, N_Ed, N_b_Rd, M_y_Ed, M_b_Rd, M_z_Ed, M_c_z_Rd, kyy, kyz):
        if not hasattr(N_Ed, 'dimensionality'):
            N_Ed = N_Ed * self.ureg.kN
        if not hasattr(N_b_Rd, 'dimensionality'):
            N_b_Rd = N_b_Rd * self.ureg.kN
        if not hasattr(M_y_Ed, 'dimensionality'):
            M_y_Ed = M_y_Ed * self.ureg.kNm
        if not hasattr(M_b_Rd, 'dimensionality'):
            M_b_Rd = M_b_Rd * self.ureg.kNm
        if not hasattr(M_z_Ed, 'dimensionality'):
            M_z_Ed = M_z_Ed * self.ureg.kNm
        if not hasattr(M_c_z_Rd, 'dimensionality'):
            M_c_z_Rd = M_c_z_Rd * self.ureg.kNm
        if not hasattr(kyy, 'dimensionality'):
            kyy = kyy * self.ureg.dimensionless
        if not hasattr(kyz, 'dimensionality'):
            kyz = kyz * self.ureg.dimensionless        
        
        equation=N_Ed/N_b_Rd+kyy*M_y_Ed/M_b_Rd+kyz*M_z_Ed/M_c_z_Rd
        
        if equation>1:
            Verification="Fail"
        else:
            Verification="Pass"
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{N_{Ed}}{N_{b,Rd}}+k_{yy} \cdot \frac{M_{y,Ed}}{M_{b,Rd}}+k_{yz} \cdot \frac{M_{z,Ed}}{M_{c,z,Rd}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\] {Verification}"))
        return equation, Verification

    def Eqn_8_89(self, N_Ed, N_b_Rd, M_y_Ed, M_b_Rd, M_z_Ed, M_c_z_Rd, kzy, kzz):
        if not hasattr(N_Ed, 'dimensionality'):
            N_Ed = N_Ed * self.ureg.kN
        if not hasattr(N_b_Rd, 'dimensionality'):
            N_b_Rd = N_b_Rd * self.ureg.kN
        if not hasattr(M_y_Ed, 'dimensionality'):
            M_y_Ed = M_y_Ed * self.ureg.kNm
        if not hasattr(M_b_Rd, 'dimensionality'):
            M_b_Rd = M_b_Rd * self.ureg.kNm
        if not hasattr(M_z_Ed, 'dimensionality'):
            M_z_Ed = M_z_Ed * self.ureg.kNm
        if not hasattr(M_c_z_Rd, 'dimensionality'):
            M_c_z_Rd = M_c_z_Rd * self.ureg.kNm
        if not hasattr(kzy, 'dimensionality'):
            kzy = kzy * self.ureg.dimensionless
        if not hasattr(kzz, 'dimensionality'):
            kzz = kzz * self.ureg.dimensionless        
        
        equation=N_Ed/N_b_Rd+kzy*M_y_Ed/M_b_Rd+kzz*M_z_Ed/M_c_z_Rd
        
        if equation>1:
            Verification="Fail"
        else:
            Verification="Pass"
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{N_{Ed}}{N_{b,Rd}}+k_{zy} \cdot \frac{M_{y,Ed}}{M_{b,Rd}}+k_{zz} \cdot \frac{M_{z,Ed}}{M_{c,z,Rd}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\] {Verification}"))
        return equation, Verification

class BS_EN_1993_1_5:
    
    def __init__(self):
        # self.ureg = pint.UnitRegistry()
        # self.ureg.load_definitions('Units.txt')
        self.ureg=ureg
        
        return
    
    def import_data(self, file_path=None, index_col=0):
        """
        Imports data from a CSV file into a DataFrame.
    
        Parameters:
        file_path (str): The path to the CSV file.
        index_col (str): The column to set as the index. Default is column 0.
    
        Returns:
        DataFrame: The imported data as a pandas DataFrame.
        """
        df = pd.read_csv(file_path, header=0, index_col=index_col)
        return df
    
    def Cl_11_1_2(self, t_w, epsilon):
        
        if not hasattr(t_w, 'dimensionality'):
            t_w = t_w * self.ureg.m
        # if not hasattr(t_s, 'dimensionality'):
        #     t_s = t_s * self.ureg.m
        # if not hasattr(h_s, 'dimensionality'):
        #     h_s = h_s * self.ureg.m
        # if not hasattr(b_s, 'dimensionality'):
        #     b_s = b_s * self.ureg.m
        # if not hasattr(l_buck, 'dimensionality'):
        #     l_buck = l_buck * self.ureg.m
        # if not hasattr(r, 'dimensionality'):
        #     r = r * self.ureg.m
        if not hasattr(epsilon, 'dimensionality'):
            epsilon = epsilon * self.ureg.dimensionless
        
        equation = 15*epsilon*t_w
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"15 \cdot \epsilon \cdot t_w"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def Stiff_Eff_Area(self, stiff_web_width, t_w, t_stiff, b):
        #For full width flats only        
        if not hasattr(stiff_web_width, 'dimensionality'):
            stiff_web_width = stiff_web_width * self.ureg.m
        if not hasattr(t_w, 'dimensionality'):
            t_w = t_w * self.ureg.m
        if not hasattr(t_stiff, 'dimensionality'):
            t_stiff = t_stiff * self.ureg.m
        if not hasattr(b, 'dimensionality'):
            b = b * self.ureg.m
            
        equation = 2*stiff_web_width*t_w + t_stiff*b
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"2 \cdot 15 \cdot \epsilon \cdot t_w^2 + t_s \cdot b"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def I_xx_stiff(self, t_stiff, b):
        #For full width flats only
        
        if not hasattr(t_stiff, 'dimensionality'):
            t_stiff = t_stiff * self.ureg.m
        if not hasattr(b, 'dimensionality'):
            b = b * self.ureg.m
            
        equation = t_stiff*b**3/12
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{t_s \cdot b^3}{12}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.4f} \\]"))
        return equation
    
    def i_x_stiff(self, I_xx, A_eff):
        #For full width flats only
        
        if not hasattr(I_xx, 'dimensionality'):
            I_xx = I_xx * self.ureg.m**4
        if  not hasattr(A_eff, 'dimensionality'):
            A_eff = A_eff * self.ureg.m**2
            
        equation = (I_xx/A_eff)**0.5
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\left(\frac{I_{s,xx}}{A_{s,eff}}\right)^\frac{1}{2}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
class BS_EN_1993_1_8:
    
    def __init__(self):
        # self.ureg = pint.UnitRegistry()
        # self.ureg.load_definitions('Units.txt') 
        self.ureg=ureg
        self.Table_6_1_data=self.import_data(file_path="EN 1993_1_8 Table 6.1.csv", index_col=None)
        return
    
    def import_data(self, file_path=None, index_col=0):
        """
        Imports data from a CSV file into a DataFrame.
    
        Parameters:
        file_path (str): The path to the CSV file.
        index_col (str): The column to set as the index. Default is column 0.
    
        Returns:
        DataFrame: The imported data as a pandas DataFrame.
        """
        df = pd.read_csv(file_path, header=0, index_col=index_col)
        return df
    
    def Table_5_9_shear(self, bolt_grade, A_s, gamma_M2 = 1.25):

        x = int(bolt_grade) # Integer part
        y = int(round((bolt_grade - x) * 10)) # First digit after the decimal

        f_y = x * y * 10
        f_ub = x * 100
  
        if bolt_grade == 4.6 or bolt_grade == 5.6 or bolt_grade == 8.8:
            alpha_v = 0.6
        elif bolt_grade == 4.8 or bolt_grade == 5.8 or bolt_grade == 6.8 or bolt_grade == 10.9:
            alpha_v= 0.5

        if not hasattr(A_s, 'dimensionality'):
            A_s = A_s * self.ureg.m**2
        if not hasattr(f_ub, 'dimensionality'):
            f_ub = f_ub * self.ureg.megapascal
        if not hasattr(gamma_M2, 'dimensionality'):
            gamma_M2 = gamma_M2 * self.ureg.dimensionless
        if not hasattr(alpha_v, 'dimensionality'):
            alpha_v = alpha_v * self.ureg.dimensionless
        
        equation = alpha_v*f_ub*A_s/gamma_M2
        equation = equation.to("kN")
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{\alpha_v \cdot f_{ub} \cdot A_s}{\gamma_{M2}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def Table_5_9_bearing(self, bolt_grade, end_inner, spacing_e1_p1, d_0, d, t, f_u, k_m = 0.9, gamma_M2 = 1.25):

        x = int(bolt_grade) # Integer part
        y = int(round((bolt_grade - x) * 10)) # First digit after the decimal

        f_y = x * y * 10
        f_ub = x * 100
  
        if end_inner == "end":
            alpha_b = min(spacing_e1_p1/d_0, 3*f_ub/f_u, 3)
        elif end_inner == "inner":
            alpha_b = min(spacing_e1_p1/d_0 - 0.5, 3* f_ub/f_u, 3)

        if not hasattr(spacing_e1_p1, 'dimensionality'):
            spacing_e1_p1 = spacing_e1_p1 * self.ureg.m
        if not hasattr(d_0, 'dimensionality'):
            d_0 = d_0 * self.ureg.m
        if not hasattr(d, 'dimensionality'):
            d = d * self.ureg.m
        if not hasattr(t, 'dimensionality'):
            t = t * self.ureg.m
        if not hasattr(k_m, 'dimensionality'):
            k_m = k_m * self.ureg.dimensionless
        if not hasattr(f_u, 'dimensionality'):
            f_u = f_u * self.ureg.megapascal
        if not hasattr(f_ub, 'dimensionality'):
            f_ub = f_ub * self.ureg.megapascal
        if not hasattr(alpha_b, 'dimensionality'):
            alpha_b = alpha_b * self.ureg.dimensionless
        if not hasattr(gamma_M2, 'dimensionality'):
            gamma_M2 = gamma_M2 * self.ureg.dimensionless
        
        equation = k_m * alpha_b * f_u * d * t/gamma_M2
        equation = equation.to("kN")
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{k_m \cdot \alpha_b \cdot f_u \cdot d \cdot t}{\gamma_{M2}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
                
    def beta_w(self, Grade, series="EN 10025 series"):

        df=self.Table_6_1_data.set_index(series)        
        result = df.loc[Grade,"Correlation factor beta_w"]
        
        result = result*self.ureg.dimensionless
        
        return result
    
    def Eqn_6_5(self, fu, beta_w, gamma_M2=1.25):
                
        if not hasattr(fu, 'dimensionality'):
            fu = fu * self.ureg.megapascal
        if  not hasattr(beta_w, 'dimensionality'):
            beta_w = beta_w * self.ureg.dimensionless
        if not hasattr(gamma_M2, 'dimensionality'):
            gamma_M2 = gamma_M2 * self.ureg.dimensionless
            
        equation = fu/((3**0.5)*beta_w*gamma_M2)
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{f_u}{\sqrt{3} \cdot \beta_w \cdot \gamma_{M2}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def Eqn_6_4(self, f_vw_d, a):
        
        if not hasattr(f_vw_d,'dimensionality'):
            f_vw_d = f_vw_d * self.ureg.megapascal
        if not hasattr(a, 'dimensionality'):
            a = a * self.ureg.m
            
        equation = f_vw_d*a
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"f_{vw,d} \cdot a"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.to('kN/m'):.2f} \\]"))
        return equation.to('kN/m')
    
    def Weld_group_res(self, F_w_Rd, total_length):
        #assumes single weld size
        
        if not hasattr(F_w_Rd, 'dimensionality'):
            F_w_Rd = F_w_Rd * self.ureg('kN/m')
        if not hasattr(total_length, 'dimensionality'):
            total_length = total_length * self.ureg.m
            
        equation = F_w_Rd*total_length
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"F_{w,Rd} \cdot \sum{weld \, lengths}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
class BS_5400_4:
    
    def __init__(self):
        # self.ureg = pint.UnitRegistry()
        # self.ureg.load_definitions('Units.txt') 
        self.ureg=ureg
        self.Table_3_data=self.import_data(file_path="Table 3.csv", index_col=0)

        return
    
    def import_data(self, file_path=None, index_col=0):
        """
        Imports data from a CSV file into a DataFrame.
    
        Parameters:
        file_path (str): The path to the CSV file.
        index_col (str): The column to set as the index. Default is column 0.
    
        Returns:
        DataFrame: The imported data as a pandas DataFrame.
        """
        df = pd.read_csv(file_path, header=0, index_col=index_col)
        return df
                      
    def eqn_1(self, f_y, A_s, z):
        if not hasattr(f_y, 'dimensionality'):
            f_y = f_y * self.ureg.MPa
        if not hasattr(A_s, 'dimensionality'):
            A_s = A_s * self.ureg.meter**2
        if not hasattr(z, 'dimensionality'):
            z = z * self.ureg.meter

        equation = (0.87 * f_y) * A_s * z
        equation = equation.to('kN * m')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\left( 0.87 \cdot f_{y} \right) \cdot A_{s} \cdot z"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_5(self, f_y, A_s, f_cu, b, d):
        if not hasattr(f_y, 'dimensionality'):
            f_y = f_y * self.ureg.MPa
        if not hasattr(A_s, 'dimensionality'):
            A_s = A_s * self.ureg.meter**2
        if not hasattr(f_cu, 'dimensionality'):
            f_cu = f_cu * self.ureg.MPa
        if not hasattr(b, 'dimensionality'):
            b = b * self.ureg.meter
        if not hasattr(d, 'dimensionality'):
            d = d * self.ureg.meter

        equation = (1-(1.1*f_y*A_s)/(f_cu*b*d))*d
        #equation = equation.to('kN * m')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\left( 1 - \frac{1.1 \cdot f_{y} \cdot A_{s}}{f_{cu} \cdot b \cdot d} \right) \cdot d"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_8(self, V, b, d):
        if not hasattr(V, 'dimensionality'):
            V = V * self.ureg.kN
        if not hasattr(b, 'dimensionality'):
            b = b * self.ureg.meter
        if not hasattr(d, 'dimensionality'):
            d = d * self.ureg.meter

        equation = V/(b*d)
        equation = equation.to('MPa')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{V}{b \cdot d}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_table_8(self, A_s, b_w, d, f_cu, gamma_m = 1.25):
        if not hasattr(A_s, 'dimensionality'):
            A_s = A_s * self.ureg.meter**2
        if not hasattr(b_w, 'dimensionality'):
            b_w = b_w * self.ureg.meter
        if not hasattr(d, 'dimensionality'):
            d = d * self.ureg.meter
        if not hasattr(f_cu, 'dimensionality'):
            f_cu = f_cu * self.ureg.MPa
        #if not hasattr(gamma_m, 'dimensionality'):
        #    gamma_m = gamma_m * self.ureg.dimensionless
            
        f_cu_root = (f_cu.magnitude) ** (1/3)
        A_root = (100*A_s.magnitude/(b_w.magnitude * d.magnitude))**(1/3)

        equation = (0.27/gamma_m)*A_root*(f_cu_root)
        equation = equation * self.ureg.MPa
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{0.27}{\gamma_{m}} \cdot \left( \frac{100 \cdot A_{s}}{b_{w} \cdot d} \right) ^ \frac{1}{3} \cdot \left( f_{cu} \right) ^ \frac{1}{3}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_table_9(self, d):
        if not hasattr(d, 'dimensionality'):
            d = d * self.ureg.meter
        
        numerator = 500
        numerator = numerator * self.ureg.meter
        
        equation = max((numerator/(1000*d))**(1/4), 0.70)
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"max \left( \left( \frac{500}{d} \right)^\frac{1}{4}; 0.70 \right)"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_table_7(self, v, xi_s, v_c, b, f_yv):
        if not hasattr(v, 'dimensionality'):
            v = v * self.ureg.MPa
        if not hasattr(xi_s, 'dimensionality'):
            xi_s = xi_s * self.ureg.dimensionless
        if not hasattr(v_c, 'dimensionality'):
            v_c = v_c * self.ureg.MPa
        if not hasattr(b, 'dimensionality'):
            b = b * self.ureg.meter
        if not hasattr(f_yv, 'dimensionality'):
            f_yv = f_yv * self.ureg.MPa
        
        if v <= xi_s * v_c:
            equation = 0.4 * self.ureg.MPa * b / (0.87 * f_yv)
        else:
            equation = b * (v + 0.4 * self.ureg.MPa - xi_s * v_c) / (0.87 * f_yv)
        
        equation = equation.to('mm**2 / m')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        if v <= xi_s * v_c:
            latex_eqn = r"\frac{A_{sv}}{s_{v}} \ge \frac{0.4 \cdot b}{0.87 \cdot f_{yv}}"
        else:
            latex_eqn = r"\frac{A_{sv}}{s_{v}} \ge \frac{b \cdot \left(\nu + 0.4-\xi_{s} \cdot \nu_{c} \right)}{0.87 \cdot f_{yv}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_a_cr(self, c, dia, spacing):
        if not hasattr(c, 'dimensionality'):
            c = c * self.ureg.m
        if not hasattr(dia, 'dimensionality'):
            dia = dia * self.ureg.m
        if not hasattr(spacing, 'dimensionality'):
            spacing = spacing * self.ureg.m

        
        equation = ((c+dia/2)**2 + (spacing/2)**2)**0.5 - dia/2
        
        equation = equation.to('mm')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\left( \left( c + \frac{\phi}{2} \right)^{2} + \left( \frac{s}{2} \right)^{2} \right) ^{0.5} - \frac{\phi}{2}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation

    def eqn_E_c_transf(self, E_c, M_g, M_q):
        if not hasattr(E_c, 'dimensionality'):
            E_c = E_c * self.ureg.MPa
        if not hasattr(M_g, 'dimensionality'):
            M_g = M_g * self.ureg.kNm
        if not hasattr(M_q, 'dimensionality'):
            M_q = M_q * self.ureg.kNm

        
        equation = E_c * (1-0.5*M_g/(M_g+M_q))
        
        #equation = equation.to('mm')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"E_{c} \cdot \left(1-\frac{0.5 \cdot M_{g}}{M_{g}+M_{q}} \right)"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_alpha_0(self, E_c, E_s):
        if not hasattr(E_c, 'dimensionality'):
            E_c = E_c * self.ureg.MPa
        if not hasattr(E_s, 'dimensionality'):
            E_s = E_s * self.ureg.MPa

        
        equation = E_s / E_c
        
        #equation = equation.to('mm')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{E_{s}}{E_{c}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_rebar_ratio(self, A_s, b, d):
        if not hasattr(A_s, 'dimensionality'):
            A_s = A_s * self.ureg.m**2
        if not hasattr(b, 'dimensionality'):
            b = b * self.ureg.m
        if not hasattr(d, 'dimensionality'):
            d = d * self.ureg.m

        
        equation = A_s / (b*d)
        
        #equation = equation.to('mm')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{A_{s}}{b \cdot d}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2e} \\]"))
        return equation
    
    def eqn_NA_depth(self, d, r, alpha_0):
        if not hasattr(d, 'dimensionality'):
            d = d * self.ureg.m
        if not hasattr(r, 'dimensionality'):
            r = r * self.ureg.dimensionless
        if not hasattr(alpha_0, 'dimensionality'):
            alpha_0 = alpha_0 * self.ureg.dimensionless

        
        equation = d*((2*r*alpha_0+(r*alpha_0)**2)**0.5 - r*alpha_0)
        
        #equation = equation.to('mm')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"d \cdot \left( \left( 2 \cdot r \cdot \alpha_{0} + \left( r \cdot \alpha_{0} \right)^{2} \right)^{\frac{1}{2}}-r \cdot \alpha_{0} \right)"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_lever_arm(self, d, x):
        if not hasattr(d, 'dimensionality'):
            d = d * self.ureg.m
        if not hasattr(x, 'dimensionality'):
            x = x * self.ureg.m

        
        equation = d-x/3
        
        #equation = equation.to('mm')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"d - \frac{x}{3}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_steel_stress(self, A_s, a, M_g, M_q):
        if not hasattr(A_s, 'dimensionality'):
            A_s = A_s * self.ureg.m**2
        if not hasattr(a, 'dimensionality'):
            a = a * self.ureg.m
        if not hasattr(M_g, 'dimensionality'):
            M_g = M_g * self.ureg.kilonewton_meter
        if not hasattr(M_q, 'dimensionality'):
            M_q = M_q * self.ureg.kilonewton_meter
        
        equation = (M_g+M_q)/(a*A_s)
        
        equation = equation.to('MPa')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{M_{g}+M_{q}}{a \cdot A_{s}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_epsilon_1(self, dist_from_bottom, epsilon_s, h, x, d):
        if not hasattr(dist_from_bottom, 'dimensionality'):
            dist_from_bottom = dist_from_bottom * self.ureg.m
        if not hasattr(epsilon_s, 'dimensionality'):
            epsilon_s = epsilon_s * self.ureg.dimensionless
        if not hasattr(h, 'dimensionality'):
            h = h * self.ureg.m
        if not hasattr(x, 'dimensionality'):
            x = x * self.ureg.m
        if not hasattr(d, 'dimensionality'):
            d = d * self.ureg.m
        
        equation = epsilon_s * ((h-dist_from_bottom-x)/(d-x))
        
        #equation = equation.to('MPa')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\epsilon_{s} \cdot \frac{h-dist \ from \ bottom -x}{d-x}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2e} \\]"))
        return equation
    
    def eqn_24(self, a_cr, epsilon_m, c_nom, h, d_c):
        if not hasattr(a_cr, 'dimensionality'):
            a_cr = a_cr * self.ureg.m
        if not hasattr(epsilon_m, 'dimensionality'):
            epsilon_m = epsilon_m * self.ureg.dimensionless
        if not hasattr(c_nom, 'dimensionality'):
            c_nom = c_nom * self.ureg.m
        if not hasattr(h, 'dimensionality'):
            h = h * self.ureg.meter
        if not hasattr(d_c, 'dimensionality'):
            d_c = d_c * self.ureg.m
        
        equation = 3*a_cr*epsilon_m/(1+2*(a_cr-c_nom)/(h-d_c))
        
        equation = equation.to('mm')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{3 \cdot a_{cr} \cdot \epsilon_{m}}{1+ \frac{2 \cdot \left( a_{cr}-c_{nom} \right)}{\left( h-d_{c} \right)}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_25(self, epsilon_1, epsilon_s, b_t, h, d_c, a_dash, A_s, M_g, M_q):
        if not hasattr(epsilon_1, 'dimensionality'):
            epsilon_1 = epsilon_1 * self.ureg.dimensionless
        if not hasattr(epsilon_s, 'dimensionality'):
            epsilon_s = epsilon_s * self.ureg.dimensionless
        if not hasattr(b_t, 'dimensionality'):
            b_t = b_t * self.ureg.m
        if not hasattr(h, 'dimensionality'):
            h = h * self.ureg.meter
        if not hasattr(d_c, 'dimensionality'):
            d_c = d_c * self.ureg.m
        if not hasattr(a_dash, 'dimensionality'):
            a_dash = a_dash * self.ureg.m
        if not hasattr(A_s, 'dimensionality'):
            A_s = A_s * self.ureg.m**2
        if not hasattr(M_g, 'dimensionality'):
            M_g = M_g * self.ureg.kNm
        if not hasattr(M_q, 'dimensionality'):
            M_q = M_q * self.ureg.kNm
        
        equation = epsilon_1-((3.8*b_t*h*(a_dash-d_c))/(epsilon_s*A_s*(h-d_c)))*((1-M_q/M_g)*10**-9)
        equation = min(epsilon_1, equation)
        
        #equation = equation.to('mm')
                
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"min \left( \epsilon_{1}, \ \epsilon_{1}-\left(\frac{3.8 \cdot b_{t} \cdot h \cdot \left( a' - d_{c} \right)}{\epsilon_{s} \cdot A_{s} \cdot \left( h-d_{c} \right)} \right) \cdot \left( \left(1- \frac{M_{q}}{M_{g}} \right) \cdot 10^{-9} \right) \right)"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2e} \\]"))
        return equation
    
class TMH7_3:
    
    def __init__(self):
        # self.ureg = pint.UnitRegistry()
        # self.ureg.load_definitions('Units.txt') 
        self.ureg=ureg

        return
    
    def import_data(self, file_path=None, index_col=0):
        """
        Imports data from a CSV file into a DataFrame.
    
        Parameters:
        file_path (str): The path to the CSV file.
        index_col (str): The column to set as the index. Default is column 0.
    
        Returns:
        DataFrame: The imported data as a pandas DataFrame.
        """
        df = pd.read_csv(file_path, header=0, index_col=index_col)
        return df
    
    def eqn_k_v(self, v, xi_s, v_c):
        if not hasattr(v, 'dimensionality'):
            v = v * self.ureg.MPa
        if not hasattr(xi_s, 'dimensionality'):
            xi_s = xi_s * self.ureg.dimensionless
        if not hasattr(v_c, 'dimensionality'):
            v_c = v_c * self.ureg.MPa
     
        x = v/(xi_s*v_c)
        
        if x < 1:
            equation = 1
        elif x > 3:
            equation = 0
        else:
            equation = -x * 1/2 + 3/2
            
        
        #equation = equation.to('mm**2 / m')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        #latex_eqn = r"-\frac{v}{\xi_{s} \cdot v_{c}} \cdot \frac{1}{2} + \frac{3}{2} \qquad for \qquad 1 < \frac{v}{\xi_{s} \cdot v_{c}} < 3 \n 1 \qquad for \qquad \frac{v}{\xi_{s} \cdot v_{c}} < 1 \n 0 \qquad for \qquad \frac{v}{\xi_{s} \cdot v_{c}} > 3"
        latex_eqn = r"""
                    k_{v} =
                    \begin{cases}
                    -\dfrac{1}{2}\dfrac{v}{\xi_{s} v_{c}} + \dfrac{3}{2}, & \text{for } 1 \le \dfrac{v}{\xi_{s} v_{c}} \le 3, \\[6pt]
                    1, & \text{for } \dfrac{v}{\xi_{s} v_{c}} < 1, \\[6pt]
                    0, & \text{for } \dfrac{v}{\xi_{s} v_{c}} > 3.
                    \end{cases}
                    """

        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_9d(self, v, b, k_v, xi_s, v_c, f_yv):
        if not hasattr(v, 'dimensionality'):
            v = v * self.ureg.MPa
        if not hasattr(b, 'dimensionality'):
            b = b * self.ureg.m
        if not hasattr(k_v, 'dimensionality'):
            k_v = k_v * self.ureg.dimensionless
        if not hasattr(xi_s, 'dimensionality'):
            xi_s = xi_s * self.ureg.dimensionless
        if not hasattr(v_c, 'dimensionality'):
            v_c = v_c * self.ureg.MPa
        if not hasattr(f_yv, 'dimensionality'):
            f_yv = f_yv * self.ureg.MPa        
        
        equation = (b*(v-k_v*xi_s*v_c)/(0.87*f_yv))
        equation = equation.to('mm**2 / m')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{A_{sv}}{s_{v}} \ge \frac{b \cdot \left (v-k_{v} \cdot \xi_{s} \cdot v_{c} \right )}{0.87 \cdot f_{yv}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_9d_min(self, b, f_yv):

        if not hasattr(b, 'dimensionality'):
            b = b * self.ureg.m
        if not hasattr(f_yv, 'dimensionality'):
            f_yv = f_yv * self.ureg.MPa        
        
        equation = (b*(0.4*self.ureg.MPa)/(0.87*f_yv))
        equation = equation.to('mm**2 / m')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{A_{sv}}{s_{v}} \ge \frac{0.4 \cdot b}{0.87 \cdot f_{yv}}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_9e(self, v, k_v, xi_s, v_c):
        if not hasattr(v, 'dimensionality'):
            v = v * self.ureg.MPa
        if not hasattr(k_v, 'dimensionality'):
            k_v = k_v * self.ureg.dimensionless
        if not hasattr(xi_s, 'dimensionality'):
            xi_s = xi_s * self.ureg.dimensionless
        if not hasattr(v_c, 'dimensionality'):
            v_c = v_c * self.ureg.MPa        
        
        equation = v-k_v*xi_s*v_c
        #equation = equation.to('mm**2 / m')
        
        if equation.magnitude < 0.4:
            Verification = 'Fail'
        else:
            Verification = 'Pass'
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"v - k_{v} \cdot \xi_{s} \cdot v_{c} \ge 0.4"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation.magnitude:.2f} \\] {Verification}"))
        return equation, Verification

    def eqn_9f(self, V, f_yL):
        if not hasattr(V, 'dimensionality'):
            V = V * self.ureg.kN
        if not hasattr(f_yL, 'dimensionality'):
            f_yL = f_yL * self.ureg.MPa
        
        equation = V/(2*0.87*f_yL)
        equation = equation.to('mm**2')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{V}{2 \cdot \left( 0.87 \cdot f_{yL} \right)}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
class SCI_P354:
    
    def __init__(self):
        # self.ureg = pint.UnitRegistry()
        # self.ureg.load_definitions('Units.txt') 
        self.ureg=ureg

        return
    
    def import_data(self, file_path=None, index_col=0):
        """
        Imports data from a CSV file into a DataFrame.
    
        Parameters:
        file_path (str): The path to the CSV file.
        index_col (str): The column to set as the index. Default is column 0.
    
        Returns:
        DataFrame: The imported data as a pandas DataFrame.
        """
        df = pd.read_csv(file_path, header=0, index_col=index_col)
        return df
    
    def eqn_16(self, f_p):

        if not hasattr(f_p, 'dimensionality'):
            f_p = f_p * self.ureg.Hz

        
        equation = 1.67*self.ureg.m*self.ureg.s*f_p**2 - 4.83*self.ureg.m*f_p + 4.5*self.ureg.m/self.ureg.s
        equation = equation.to('m/s')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"1.67 \cdot f_{p}^{2} - 4.83 \cdot f_{p} + 4.50"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.4f} \\]"))
        return equation
    
    def eqn_37(self, ζ, L_p, f_p, ν):
        if not hasattr(ζ, 'dimensionality'):
            ζ = ζ * self.ureg.dimensionless
        if not hasattr(L_p, 'dimensionality'):
            L_p = L_p * self.ureg.m
        if not hasattr(f_p, 'dimensionality'):
            f_p = f_p * self.ureg.Hz
        if not hasattr(ν, 'dimensionality'):
            ν = ν * self.ureg.m / self.ureg.s
        
        equation = 1 - math.exp(-2*math.pi*ζ*L_p*f_p/ν)
        #equation = equation.to('m/s**2')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"1-e^{\left(\frac{-2 \cdot \pi \cdot \zeta \cdot L_{p} \cdot f_{p}}{\nu} \right)}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.4f} \\]"))
        return equation
    
    def eqn_38(self, a_w_rms):
        if not hasattr(a_w_rms, 'dimensionality'):
            a_w_rms = a_w_rms * self.ureg.m/self.ureg.s**2
        
        equation = a_w_rms/(0.005*self.ureg.m/self.ureg.s**2)
        #equation = equation.to('m/s**2')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{a_{w,rms}}{0.005}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_39(self, a_w_rms):
        if not hasattr(a_w_rms, 'dimensionality'):
            a_w_rms = a_w_rms * self.ureg.m/self.ureg.s**2
        
        equation = a_w_rms/(0.00357*self.ureg.m/self.ureg.s**2)
        #equation = equation.to('m/s**2')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{a_{w,rms}}{0.00357}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_50(self, μ_e, μ_r, Q, M, ζ, W, ρ):
        if not hasattr(μ_e, 'dimensionality'):
            μ_e = μ_e * self.ureg.dimensionless
        if not hasattr(μ_r, 'dimensionality'):
            μ_r = μ_r * self.ureg.dimensionless
        if not hasattr(Q, 'dimensionality'):
            Q = Q * self.ureg.N
        if not hasattr(M, 'dimensionality'):
            M = M * self.ureg.kg
        if not hasattr(ζ, 'dimensionality'):
            ζ = ζ * self.ureg.dimensionless
        if not hasattr(W, 'dimensionality'):
            W = W * self.ureg.dimensionless
        if not hasattr(ρ, 'dimensionality'):
            ρ = ρ * self.ureg.dimensionless
        
        equation = μ_e * μ_r * ((0.1 * Q)/(2 * M * ζ * 2**0.5)) * W * ρ
        equation = equation.to('m/s**2')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\mu_{e} \cdot \mu_{r} \cdot \frac{0.1 \cdot Q}{2 \cdot \sqrt{2} \cdot M \cdot \zeta} \cdot W \cdot \rho"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.4f} \\]"))
        return equation
    
class BD_28_87:
    
    def __init__(self):
        # self.ureg = pint.UnitRegistry()
        # self.ureg.load_definitions('Units.txt') 
        self.ureg=ureg

        return
    
    def import_data(self, file_path=None, index_col=0):
        """
        Imports data from a CSV file into a DataFrame.
    
        Parameters:
        file_path (str): The path to the CSV file.
        index_col (str): The column to set as the index. Default is column 0.
    
        Returns:
        DataFrame: The imported data as a pandas DataFrame.
        """
        df = pd.read_csv(file_path, header=0, index_col=index_col)
        return df
    
    def Cl_5_1_f_ct_star(self, f_cu):
        if not hasattr(f_cu, 'dimensionality'):
            f_cu = f_cu * self.ureg.MPa
            
        f_cu_power = f_cu**0.7/self.ureg('MPa**0.7')
        f_cu_power = f_cu_power * self.ureg.MPa
        
        equation = 0.12 * f_cu_power
        equation = equation.to('MPa')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"0.12 \cdot \left( f_{cu} \right)^{0.7}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation
    
    def eqn_2(self, f_ct_star, f_y, A_c):
        if not hasattr(f_ct_star, 'dimensionality'):
            f_ct_star = f_ct_star * self.ureg.MPa
        if not hasattr(f_y, 'dimensionality'):
            f_y = f_y * self.ureg.MPa
        if not hasattr(A_c, 'dimensionality'):
            A_c = A_c * self.ureg('mm**2')
            
        
        equation = f_ct_star * A_c / f_y
        #equation = equation.to('MPa')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{\left(f_{ct}^{*} \right)}{f_{y}} \cdot A_{c}"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation

    def eqn_3(self, f_ct_star, f_b, A_c, phi, w, R, epsilon_sh, epsilon_th, epsilon_ult=200):
        if not hasattr(f_ct_star, 'dimensionality'):
            f_ct_star = f_ct_star * self.ureg.MPa
        if not hasattr(f_b, 'dimensionality'):
            f_b = f_b * self.ureg.MPa
        if not hasattr(A_c, 'dimensionality'):
            A_c = A_c * self.ureg('mm**2')
        if not hasattr(phi, 'dimensionality'):
            phi = phi * self.ureg.mm
        if not hasattr(w, 'dimensionality'):
            w = w * self.ureg.mm
        if not hasattr(R, 'dimensionality'):
            R = R *self.ureg.dimensionless
        if not hasattr(epsilon_sh, 'dimensionality'):
            epsilon_sh = epsilon_sh * self.ureg.dimensionless
        if not hasattr(epsilon_ult, 'dimensionality'):
            epsilon_ult = epsilon_ult * self.ureg.dimensionless
            
        equation = (f_ct_star/f_b) * A_c * (phi/(2*w)) *(R*(epsilon_sh + epsilon_th) - 0.5 * epsilon_ult)

        #equation = equation.to('MPa')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"\frac{\left(f_{ct}^{*} \right)}{f_{b}} \cdot A_{c} \cdot \frac{\phi}{2 \cdot w} \cdot \left(R \cdot \left( \epsilon_{sh} + \epsilon_{th} \right) - 0.5 \cdot \epsilon_{ult} \right)"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2f} \\]"))
        return equation

    def eqn_4(self, alpha, T_1, T_2):
        if not hasattr(alpha, 'dimensionality'):
            alpha = alpha * self.ureg('delta_degC**-1')
        if not hasattr(T_1, 'dimensionality'):
            T_1 = T_1 * self.ureg('delta_degC')
        if not hasattr(T_2, 'dimensionality'):
            T_2 = T_2 * self.ureg('delta_degC')
            
        T_sum = T_1 + T_2
        equation = 0.8 * alpha * T_sum

        #equation = equation.to('MPa')
        
        text_before = "The equation is:"
        text_after = "This results in the value below:"
        latex_eqn = r"0.8 \cdot \alpha \cdot \left(T_{1} + T_{2} \right)"
        display(Latex(f"{text_before} \\[ {latex_eqn} \\] {text_after} \\[ {equation:.2e} \\]"))
        return equation               
    