import serial
import time
import matplotlib.pyplot as plt
from datetime import datetime

# CONFIGURAÇÕES
PORTA = 'COM20'            
BAUDRATE = 115200           # Velocidade de comunicação
NUM_MEDIDAS = 10            # Quantas medidas fazer
INTERVALO = 1.0             # 1 segundo entre medidas

def configura_medidor(ser):
    ser.write(b"UNIT:DBM\n")
    time.sleep(0.2)
    ser.write(b"SYST:ZCH\n")
    time.sleep(0.2)

def ler_medida(ser):
    ser.write(b"MEAS:POW?\n")
    resposta = ser.readline().decode().strip()
    try:
        return float(resposta)
    except:
        return None

def main():
    print("Conectando ao medidor PM61CH...")
    
    ser = serial.Serial(PORTA, BAUDRATE, timeout=2)
    time.sleep(1)
    configura_medidor(ser)
    print("Conectado! Iniciando medições...")
    print("")
    
    medidas = []
    
    plt.ion()
    fig, ax = plt.subplots()
    
    for i in range(NUM_MEDIDAS):
        potencia = ler_medida(ser)
        
        if potencia is not None:
            medidas.append(potencia)
            print(f"Medida {i+1}: {potencia:.3f} dBm")
            
            media_ate_agora = sum(medidas) / len(medidas)
            
            ax.clear()
            ax.plot(medidas, 'bo-')
            ax.set_xlabel('Número da medida')
            ax.set_ylabel('Potência (dBm)')
            ax.set_title(f'Média até agora: {media_ate_agora:.3f} dBm')
            ax.grid(True)
            plt.pause(0.01)
        else:
            print(f"Medida {i+1}: erro na leitura")
        
        if i < NUM_MEDIDAS - 1:
            time.sleep(INTERVALO)
    
    ser.close()
    print("")
    print("Terminei as medições!")
    
    media_final = sum(medidas) / len(medidas)
    minimo = min(medidas)
    maximo = max(medidas)
    incerteza = (maximo - minimo) / 2.0
    
    print("")
    print("RESULTADOS FINAIS")
    print("")
    print(f"Medidas feitas: {len(medidas)}")
    print(f"Média:          {media_final:.4f} dBm")
    print(f"Mínimo:         {minimo:.4f} dBm")
    print(f"Máximo:         {maximo:.4f} dBm")
    print(f"Incerteza:      ± {incerteza:.4f} dB")
    print("")
    
    nome_arquivo = f"medidas_power_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(nome_arquivo, "w") as arquivo:
        arquivo.write("PM61CH - Medidas de Potência\n")
        arquivo.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        arquivo.write(f"Medidas: {NUM_MEDIDAS}\n")
        arquivo.write(f"Intervalo: {INTERVALO}s\n")
        arquivo.write("\n")
        arquivo.write("Medida, Potencia(dBm)\n")
        
        for num, valor in enumerate(medidas):
            arquivo.write(f"{num+1}, {valor:.4f}\n")
        
        arquivo.write("\n")
        arquivo.write(f"Media, {media_final:.4f}\n")
        arquivo.write(f"Minimo, {minimo:.4f}\n")
        arquivo.write(f"Maximo, {maximo:.4f}\n")
        arquivo.write(f"Incerteza, ±{incerteza:.4f}\n")
    
    print(f"Arquivo salvo: {nome_arquivo}")
    
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()