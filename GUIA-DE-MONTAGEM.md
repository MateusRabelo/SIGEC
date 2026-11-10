# Guia de Montagem e Esquema de Ligações Elétricas — SIGEC
**Documento Técnico de Bancada — Revisão D (Versão Mínima Essencial)**  
**Projeto:** SIGEC — Sistema Inteligente de Gestão e Eficiência na Climatização  
**Instituição:** Universidade Federal do Ceará (UFC) — Campus Russas  

---

## 1. O Que Foi Simplificado Nesta Revisão?
Para viabilizar a montagem imediata com o que você já tem em bancada, eliminamos todas as peças dispensáveis:
- **Transistor / MOSFET eliminado:** O LED infravermelho agora é acionado direto pelo pino do ESP32 com apenas um resistor em série. Para bancada e testes a até 1–2 metros do split, a corrente do GPIO é mais que suficiente.
- **Segundo capacitor (C3) eliminado:** Mantivemos apenas o único capacitor eletrolítico (C1 de 10 µF), estritamente necessário para estabilizar o offset de 1,65V do sensor de corrente. O C3 era apenas um filtro passa-baixa opcional.
- **Resistores extras eliminados:** Sem transistor, foram descartados os resistores de base (R5) e pull-down (R6). O resistor R3 de proteção também foi removido, ligando o SCT direto no pino analógico.
- **LED azul externo dispensado:** O ESP32 DevKit já possui um LED azul soldado na própria placa no GPIO 2. Zero fios e zero resistores extras para a sinalização de rede.
- **Trilho de 5V na protoboard dispensado:** Todo o circuito opera em 3,3V e terra (GND), alimentado direto pela USB do ESP32.

---

## 2. Lista Enxuta de Componentes (Apenas o Essencial)

| Item | Componente | Função |
| :--- | :--- | :--- |
| 1 | **ESP32 DevKit v1** | Microcontrolador central (alimentado via cabo USB) |
| 2 | **Sensor SCT-013-000** | Sensor alicate de corrente AC (com conector Jack P2 ou fios expostos) |
| 3 | **Sensor Sensirion SCD40** | Módulo de CO₂, temperatura e umidade (comunicação I2C) |
| 4 | **LED Infravermelho 940 nm** | Emissor de comandos para o ar-condicionado (KY-005 ou LED avulso) |
| 5 | **1x Capacitor Eletrolítico (10 µF)** | Filtro de estabilização da tensão de offset (VBIAS = 1,65V) |
| 6 | **2x Resistores Iguais (10 kΩ ou 100 kΩ)** | Divisor de tensão para criar o offset de 1,65V |
| 7 | **1x Resistor de Carga (Burden Rb = 10 Ω a 33 Ω)** | Converte a corrente de saída do SCT em tensão de leitura |
| 8 | **1x Resistor de 100 Ω a 220 Ω** | Limitador de corrente para o LED infravermelho |
| 9 | **(Opcional) 1x LED Amarelo + 1x Resistor 220 Ω** | Apenas se quiser sinalizador de envio de dados no GPIO 18 |
| 10 | **Protoboard e Jumpers** | Para as interconexões |

---

## 3. Esquema das Conexões Ponto a Ponto

### Circuito 1: Sensor de Corrente SCT-013 (Condicionamento Mínimo)
O sensor gera corrente alternada. O divisor com dois resistores iguais e o seu capacitor cria uma referência estável de 1,65V para o ESP32 conseguir ler a senoide completa sem semiciclo negativo:

```
        +3.3V (do ESP32)
          │
        [10 kΩ]
          │
          ├─── Ponto VBIAS (1,65V) ──────────────────────────┐
          │                                                  │
        [10 kΩ]       [Capacitor 10 µF]                      │
          │                  │                               │
         GND                GND                              │
                                                             │
SCT-013 (Jack P2)                                            │
[ Terminal B / Base ] ───────────────────────────────────────┘
          │
        [Rb: 10 Ω a 33 Ω]
          │
[ Terminal A / Ponta ] ─────────────────────── GPIO 34 (ADC1 do ESP32)
```

**Passo a passo:**
1. Ligue um resistor de 10 kΩ entre o pino **3V3** do ESP32 e um ponto livre da protoboard (vamos chamar de **nó VBIAS**).
2. Ligue o outro resistor de 10 kΩ entre o **nó VBIAS** e o **GND**.
3. Ligue o seu único capacitor de 10 µF em paralelo com esse segundo resistor:
   - Perna longa (positivo `+`) no **nó VBIAS**.
   - Perna curta / faixa com traço (negativo `-`) no **GND**.
4. Ligue o resistor de carga (Burden Rb de 10 Ω a 33 Ω) entre os dois fios do sensor SCT-013 (Terminal A e Terminal B do Jack P2).
5. Ligue o **Terminal B** do sensor direto no **nó VBIAS**.
6. Ligue o **Terminal A** do sensor direto no pino **GPIO 34** do ESP32.

---

### Circuito 2: Emissor Infravermelho (Acionamento Direto sem Transistor)
Ligação simplificada direto do pino GPIO do microcontrolador:

```
ESP32 GPIO 4 ─── [Resistor 100 Ω ou 220 Ω] ─── (Ânodo +) [LED IR 940nm] (Cátodo -) ─── GND
```

**Passo a passo:**
1. Ligue um fio do pino **GPIO 4** do ESP32 em uma perna do resistor de 100 Ω (ou 220 Ω).
2. Ligue a outra perna do resistor no **Ânodo (+, perna maior)** do LED IR.
3. Ligue o **Cátodo (-, perna menor)** do LED IR direto no **GND**.
*(Se você estiver usando o módulozinho pronto KY-005, ligue o pino de sinal no GPIO 4 através do resistor e o pino `-` no GND).*

---

### Circuito 3: Sensor de Qualidade do Ar Sensirion SCD40 (I2C Direto)
Apenas 4 fios conectando o módulo breakout direto nos pinos do ESP32:

- **VCC do SCD40** $\rightarrow$ Pino **3V3** do ESP32
- **GND do SCD40** $\rightarrow$ Pino **GND** do ESP32
- **SDA do SCD40** $\rightarrow$ Pino **GPIO 21** do ESP32
- **SCL do SCD40** $\rightarrow$ Pino **GPIO 22** do ESP32

---

### Circuito 4: LEDs de Diagnóstico
- **LED Azul (Conexão Wi-Fi / Broker MQTT):** Não precisa espetar nada na protoboard! O firmware já controla o LED azul soldado direto na placa do ESP32 (GPIO 2 onboard).
- **LED Amarelo (Heartbeat / Envio de Pacote):** Se você tiver um LED comum e um resistor de 220 Ω a 1 kΩ sobrando, ligue:
  - **GPIO 18** $\rightarrow$ Resistor $\rightarrow$ Ânodo (+) do LED $\rightarrow$ Cátodo (-) no **GND**.
  - Se não tiver, pode ignorar totalmente essa ligação; o sistema funciona normalmente e você acompanha o heartbeat pelo monitor serial da IDE.

---

## 4. Tabela Resumo das Conexões Físicas

| Componente | Terminal | Conectar Em |
| :--- | :--- | :--- |
| **Resistor R1 (10 kΩ)** | Terminal 1 | ESP32 **3V3** |
| **Resistor R1 (10 kΩ)** | Terminal 2 | Nó central VBIAS |
| **Resistor R2 (10 kΩ)** | Terminal 1 | Nó central VBIAS |
| **Resistor R2 (10 kΩ)** | Terminal 2 | ESP32 **GND** |
| **Capacitor C1 (10 µF)** | Positivo (+) | Nó central VBIAS |
| **Capacitor C1 (10 µF)** | Negativo (-) | ESP32 **GND** |
| **SCT-013 Jack P2** | Terminal A (Ponta) | ESP32 **GPIO 34** + lado 1 do resistor Rb |
| **SCT-013 Jack P2** | Terminal B (Base) | Nó central VBIAS + lado 2 do resistor Rb |
| **Resistor Burden (Rb)** | Terminais | Em paralelo entre Terminal A e Terminal B do SCT |
| **Resistor IR (100–220 Ω)** | Entrada | ESP32 **GPIO 4** |
| **Resistor IR (100–220 Ω)** | Saída | LED IR Ânodo (+) |
| **LED IR 940 nm** | Cátodo (-) | ESP32 **GND** |
| **Sensirion SCD40** | VCC | ESP32 **3V3** |
| **Sensirion SCD40** | GND | ESP32 **GND** |
| **Sensirion SCD40** | SDA | ESP32 **GPIO 21** |
| **Sensirion SCD40** | SCL | ESP32 **GPIO 22** |

---

## 5. Dicas Importantes para o Teste
- **Alimentação:** Ligue o ESP32 na porta USB do computador. Não precisa de fonte externa de 5V.
- **Medição no Ar-Condicionado:** O alicate do SCT-013 deve abraçar **apenas um fio** do cabo de energia do ar (apenas a fase), nunca o cabo duplo inteiro junto.
- **Alinhamento do LED IR:** Como está sem transistor de potência, aponte a cabeça do LED IR diretamente para a frente do receptor do ar-condicionado a uma distância de até 1 a 2 metros durante os testes.
