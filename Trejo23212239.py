"""
Práctica 4: Sistema endócrino

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Gabriel Fernando Trejo Paz
Número de control: 23212239
Correo institucional: L23212239@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

#Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N = round(tend/dt) + 1
t = np.linspace(t0,tend,N)
#Ve = np.ones(N) #Step
Ve = (t >= 1.0).astype(float)

# Circuitos eléctricos para control y caso: [R1, L, C, R2]
params_circuito = {
    'Control': [1E3, 680E-6, 1E-6, 100E3],
    'Caso': [1E3, 680E-6, 1000E-6, 1E3]
}
def sistema(R1, L, C, R2):
    num = [L, R2]
    den =[R1*L*C, R1*R2*C+L, R1+R2]
    sys = ctrl.tf(num,den)
    P = np.roots(den)

    print(f"Función de transferencia de ['nombre'] en lazo abierto: {sys}\n")
    return sys, P

Control, P_co = sistema(*params_circuito['Control'])
Caso, P_ca = sistema(*params_circuito['Caso'])

print(f"Polos del sistema Control: P1 = {P_co[0]:.3e}, P2 = {P_co[1]:.3e}\n")
print(f"Polos del sistema Caso: P1 = {P_ca[0]:.3e}, P2 = {P_ca[1]:.3e}\n")


# Componentes del controlador
kP, kI, kD = 1319.6, 322481.1343, 0.17971
Cr = 1E-6
Re = 1/(Cr*kI) 
Rr = kP*Re
Ce = kD/Rr
numPID = [Re*Rr*Ce*Cr, Re*Ce+Rr*Cr, 1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID,denPID)
print(f"El valor de la resistencia Re es de {Re} Ohms.\n")
print(f"El valor de la resistencia Rr es de {Rr} Ohms.\n")
print(f"El valor de la capacitancia Ce es de {Ce} Faradios.\n")
print(f"Función de transferencia del controlador PID: {PID}\n")

# Sistema de control en lazo cerrado
sysPID = ctrl.feedback(ctrl.series(PID,Caso),1,sign = -1)
print(f"Función de transferencia del sistema de control en lazo cerrado: {sysPID}")

#Colores
clr1 = np.array([9,21,64])/255
clr2 = np.array([27,94,32])/255
clr3 = np.array([246,36,64])/255
clr4 = np.array([245, 153, 198])/255

_, Vex = ctrl.forced_response(Control, t, Ve, x0)
_, Vey = ctrl.forced_response(Caso, t, Ve, x0)
_, VePID = ctrl.forced_response(sysPID, t, Vex, x0)

#Respuestas: Simulaciones numéricas
fg = plt.figure(1)
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,Ve,'--',color=clr1,label='Ve(t)')
plt.plot(t,Vex,'-',color=clr2,label='Fs(t): Control')
plt.plot(t,Vey,'--',color=clr3,label='Fs(t): Caso')
plt.plot(t,VePID,':',color=clr4,label='PID(t): Tratamiento')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1);plt.yticks(np.arange(-0.1,1.2,0.1))
plt.xlabel('t [s]')
plt.ylabel('Ve(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=4,frameon=False)
plt.show()
fg.savefig('Respuesta_python.pdf',bbox_inches='tight')