# Guia de Montagem e Esquema de Ligações Elétricas — SIGEC
**Documento Técnico de Bancada — Revisão C (27/10/2026)**  
**Projeto:** SIGEC — Sistema Inteligente de Gestão e Eficiência na Climatização  
**Instituição:** Universidade Federal do Ceará (UFC) — Campus Russas  

---

## 1. Lista de Materiais e Componentes (BOM)

| Item | Componente | Descrição / Especificação | Quantidade |
| :--- | :--- | :--- | :--- |
| 1 | **ESP32 DevKit v1** | Microcontrolador Dual-Core 240MHz, 30 pinos, Wi-Fi 2.4 GHz | 1 un |
| 2 | **SCT-013-000** | Sensor de Corrente Não-Invasivo (100 A / 50 mA) | 1 un |
| 3 | **Jack P2 3.5 mm Fêmea** | Conector de painel ou breakout para o plugue do SCT-013 | 1 un |
| 4 | **Sensirion SCD40** | Sensor Fotoacústico de CO₂ (400–2000 ppm), Temp e Umidade (I2C) | 1 un |
| 5 | **LED IR 940 nm** | Diodo Emissor Infravermelho 940 nm (ou módulo KY-005) | 1 un |
| 6 | **BC547 (ou 2N2222)** | Transistor Bipolar de Junção NPN (Encapsulamento TO-92) | 1 un |
| 7 | **LED Difuso Azul 5 mm** | Sinalizador de Conexão de Rede (Wi-Fi / MQTT) | 1 un |
| 8 | **LED Difuso Amarelo 5 mm**| Sinalizador de Heartbeat / Telemetria ativa | 1 un |
| 9 | **Resistor 10 Ω (1%)** | $R_b$ — Resistor de Carga (*Burden*) para o secundário do SCT | 1 un |
| 10 | **Resistor 10 kΩ (5%)** | $R_1$ e $R_2$ — Divisor de tensão para offset $V_{\text{BIAS}} = 1,65\text{ V}$ | 2 un |
| 11 | **Resistor 1 kΩ (5%)** | $R_3$ (proteção ADC GPIO34) e $R_5$ (base do transistor IR) | 2 un |
| 12 | **Resistor 220 Ω (5%)** | $R_4$ (limitador do LED IR) e limitadores dos LEDs Azul e Amarelo | 3 un |
| 13 | **Resistor 100 kΩ (5%)** | $R_6$ — Resistor de *Pull-down* de segurança na base do transistor | 1 un |
| 14 | **Capacitor 10 µF (16V+)** | $C_1$ — Eletrolítico polarizado (estabilização de $V_{\text{BIAS}}$) | 1 un |
| 15 | **Capacitor 100 nF** | $C_3$ — Cerâmico tipo disco/pastilha (filtro passa-baixa ADC) | 1 un |
| 16 | **Protoboard 830 pontos** | Matriz de contatos com barramentos laterais | 1 un |
| 17 | **Jumpers Macho-Macho** | Cabos flexíveis coloridos de interconexão | Kit variado |

---

## 2. Identificação Física de Pinos dos Componentes

- **ESP32 DevKit v1 (30 pinos):**
  - **Lado Esquerdo (descendo da antena):** EN, VP (36), VN (39), **GPIO 34**, GPIO 35, GPIO 32, GPIO 33, GPIO 25, GPIO 26, GPIO 27, GPIO 14, GPIO 12, **GND**, **VIN (5V)**.
  - **Lado Direito (descendo da antena):** GPIO 23, **GPIO 22 (SCL)**, TX0, RX0, **GPIO 21 (SDA)**, GPIO 19, **GPIO 18**, GPIO 5, GPIO 17, GPIO 16, **GPIO 4**, **GPIO 2**, GPIO 15, **GND**, **3V3**.
- **Transistor NPN BC547 (TO-92, olhando para a face plana com a inscrição de frente):**
  - Pino 1 (Esquerda): **Coletor (C)**
  - Pino 2 (Meio): **Base (B)**
  - Pino 3 (Direita): **Emissor (E)**
- **Capacitor Eletrolítico $C_1$ (10 µF):**
  - Terminal Longo: **Positivo (+)**
  - Terminal Curto / Faixa cinza com traço `-`: **Negativo (-)**
- **LEDs (Azul, Amarelo e IR):**
  - Terminal Longo / Face arredondada: **Ânodo (+)**
  - Terminal Curto / Face chanfrada achatada: **Cátodo (-)**
- **Conector Jack P2 (3.5 mm) do SCT-013:**
  - **Ponta (Tip):** Terminal Ativo A (Sinal)
  - **Manga (Sleeve / Base):** Terminal Ativo B (Retorno)
  - *(O anel central / Ring geralmente fica deserto ou unificado no modelo de 2 vias).*

---

## 3. Conexões de Alimentação e Barramentos da Protoboard

> [!CAUTION]
> **Regra Estrita de Segurança Elétrica:**  
> **NUNCA** una o barramento de $3,3\text{ V}$ ao barramento de $+5\text{ V}$. Os barramentos positivos devem ser fisicamente isolados em lados opostos da protoboard. Apenas as linhas de terra (**GND**) devem ser unificadas.

1. **Trilho Superior / Direito Vermelho (+):** Conectar ao pino **VIN (5V)** do ESP32 (Alimentação USB de $+5\text{ V}$).
2. **Trilho Inferior / Esquerdo Vermelho (+):** Conectar ao pino **3V3** do ESP32 (Linha regulada de $3,3\text{ V}$).
3. **Trilhos Azuis/Pretos (-):** Conectar ambos os trilhos de terra entre si por uma ponte de fio e ligar ao pino **GND** do ESP32.

---

## 4. Circuito 1: Condicionamento de Sinal do Sensor de Corrente (SCT-013-000)

O sensor SCT-013-000 gera uma corrente alternada proporcional no seu secundário ($50\text{ mA}$ para $100\text{ A}$ no primário). Este circuito converte essa corrente em tensão, injeta um *offset* de corrente contínua de $+1,65\text{ V}$ para permitir leitura da senoide pelo ADC e filtra ruídos de amostragem.

```
       +3.3V
         │
        [R1: 10k]
         │
         ├─── VBIAS (1.65V) ──────────────────────────┐
         │                                            │
        [R2: 10k]    [C1: 10uF]                       │
         │               │                            │
        GND             GND                           │
                                                      │
SCT-013 Jack P2                                       │
[ Terminal B ] ───────────────────────────────────────┘
       │
      [Rb: 10R 1%]
       │
[ Terminal A ] ─── [R3: 1k] ──┬─── GPIO 34 (ADC1)
                              │
                          [C3: 100nF]
                              │
                             GND
```

### Passo a passo das ligações:
1. **Resistor de Carga (*Burden* $R_b$ = 10 Ω, 1%):**  
   - Conectar um terminal de $R_b$ ao **Terminal A** do Jack P2.  
   - Conectar o outro terminal de $R_b$ ao **Terminal B** do Jack P2.
2. **Divisor de Tensão de Offset ($V_{\text{BIAS}} = 1,65\text{ V}$):**  
   - Conectar uma perna de $R_1$ ($10\text{ k}\Omega$) ao trilho **3V3**.  
   - Conectar a outra perna de $R_1$ ao nó central de referência ($V_{\text{BIAS}}$).  
   - Conectar uma perna de $R_2$ ($10\text{ k}\Omega$) ao nó central ($V_{\text{BIAS}}$).  
   - Conectar a outra perna de $R_2$ ao trilho **GND**.
3. **Capacitor de Desacoplamento ($C_1$ = 10 µF eletrolítico):**  
   - Terminal Positivo (+) de $C_1$ ligado ao nó central $V_{\text{BIAS}}$.  
   - Terminal Negativo (-) de $C_1$ ligado ao trilho **GND**.
4. **Referência no Sensor:**  
   - Ligar o **Terminal B** do Jack P2 diretamente ao nó central $V_{\text{BIAS}}$ ($1,65\text{ V}$).
5. **Filtragem e Entrada no ADC:**  
   - Ligar o **Terminal A** do Jack P2 a um terminal do resistor de proteção $R_3$ ($1\text{ k}\Omega$).  
   - Ligar a outra ponta de $R_3$ ao nó do **GPIO 34 (ADC1)** do ESP32.  
   - Ligar o capacitor cerâmico $C_3$ ($100\text{ nF}$) entre esse pino do **GPIO 34** e o trilho **GND**.

---

## 5. Circuito 2: Emissor Infravermelho para Controle do Split (KY-005)

Como o ESP32 fornece apenas ~12 mA por GPIO e um emissor IR precisa de pulsos de ~80–100 mA para alcançar o ar-condicionado a 4 metros de distância, utiliza-se um transistor NPN como chave saturada com alimentação em $+5\text{ V}$.

```
    +5V (VIN)
      │
     [R4: 220R]
      │
      ▲  LED IR 940nm (Ânodo)
     ───
      │  (Cátodo)
      │
      ├── Coletor (C)
      │
GPIO 4 ── [R5: 1k] ──┬── Base (B)  [Q1: BC547]
                     │
                 [R6: 100k]
                     │
                    GND
                     │
                    Emissor (E)
                     │
                    GND
```

### Passo a passo das ligações:
1. Conectar uma ponta de $R_4$ ($220\ \Omega$) ao trilho de **+5V (VIN)**.
2. Conectar a outra ponta de $R_4$ ao **Ânodo (+)** do LED IR de 940 nm (ou terminal de sinal do módulo KY-005).
3. Conectar o **Cátodo (-)** do LED IR ao pino **Coletor (C)** do transistor BC547.
4. Conectar o pino **Emissor (E)** do transistor BC547 diretamente ao trilho **GND**.
5. Conectar o resistor de *pull-down* $R_6$ ($100\text{ k}\Omega$) entre a **Base (B)** do BC547 e o trilho **GND** (impede rajadas espúrias no boot do chip).
6. Conectar o resistor de base $R_5$ ($1\text{ k}\Omega$) entre a **Base (B)** do BC547 e o pino **GPIO 4** do ESP32.

---

## 6. Circuito 3: Sensor de Qualidade do Ar Sensirion SCD40 (I2C)

O SCD40 faz leituras digitais de CO₂, temperatura e umidade relativa via protocolo I2C nativo.

| Pino do Módulo SCD40 | Conectar em | Função / Observação |
| :--- | :--- | :--- |
| **VCC** | Trilho **3V3** | Alimentação regulada de $3,3\text{ V}$ |
| **GND** | Trilho **GND** | Referência de terra |
| **SDA** | **GPIO 21** do ESP32 | Linha de Dados Bidirecional I2C |
| **SCL** | **GPIO 22** do ESP32 | Linha de Clock I2C |

---

## 7. Circuito 4: LEDs de Diagnóstico e Sinalização Visual

Os dois LEDs oferecem confirmação imediata da operação sem necessidade de monitor serial:

### LED Azul (Status de Rede Wi-Fi & Broker MQTT):
- Pino **GPIO 2** do ESP32 $\rightarrow$ Resistor de $220\ \Omega$ $\rightarrow$ **Ânodo (+)** do LED Azul.
- **Cátodo (-)** do LED Azul $\rightarrow$ Trilho **GND**.
- *Comportamento:* Piscando lento = Conectando à rede / broker; Aceso fixo = Conexão estabelecida e operando.

### LED Amarelo (Heartbeat / Ciclo de Telemetria Ativo):
- Pino **GPIO 18** do ESP32 $\rightarrow$ Resistor de $220\ \Omega$ $\rightarrow$ **Ânodo (+)** do LED Amarelo.
- **Cátodo (-)** do LED Amarelo $\rightarrow$ Trilho **GND**.
- *Comportamento:* Pisca em pulso rápido de 100 ms a cada 5 segundos no momento exato em que a telemetria é calculada e transmitida.

---

## 8. Tabela Netlist Ponto a Ponto (De $\rightarrow$ Para)

Esta tabela consolida todas as conexões individuais para conferência rápida com multímetro:

| Origem (De) | Destino (Para) | Função |
| :--- | :--- | :--- |
| **ESP32 VIN** | Trilho Positivo Superior | Alimentação $+5\text{ V}$ USB |
| **ESP32 3V3** | Trilho Positivo Inferior | Alimentação $+3,3\text{ V}$ LDO |
| **ESP32 GND** | Trilho Negativo (Comum) | Referência $0\text{ V}$ Unificada |
| **Trilho 3V3** | Resistor $R_1$ ($10\text{ k}\Omega$) | Entrada Divisor de Offset |
| **Resistor $R_1$** | Nó Central $V_{\text{BIAS}}$ | Ponto de $1,65\text{ V}$ |
| **Nó $V_{\text{BIAS}}$** | Resistor $R_2$ ($10\text{ k}\Omega$) | Saída Divisor de Offset |
| **Resistor $R_2$** | Trilho GND | Aterramento do Divisor |
| **Nó $V_{\text{BIAS}}$** | Capacitor $C_1$ Terminal (+) | Desacoplamento do Offset |
| **Capacitor $C_1$ Terminal (-)** | Trilho GND | Aterramento de $C_1$ |
| **Nó $V_{\text{BIAS}}$** | Jack P2 Terminal B | Referência do Secundário do SCT |
| **Jack P2 Terminal A** | Resistor $R_b$ ($10\ \Omega$) | Carga de Corrente (*Burden*) |
| **Jack P2 Terminal B** | Resistor $R_b$ ($10\ \Omega$) | Fechamento de Carga (*Burden*) |
| **Jack P2 Terminal A** | Resistor $R_3$ ($1\text{ k}\Omega$) | Entrada de Proteção do ADC |
| **Resistor $R_3$ (Saída)** | **ESP32 GPIO 34 (ADC1)** | Linha de Sinal Analógico Amostrada |
| **ESP32 GPIO 34** | Capacitor $C_3$ ($100\text{ nF}$) | Filtro Passa-Baixa de Ruído |
| **Capacitor $C_3$** | Trilho GND | Aterramento do Filtro $C_3$ |
| **Trilho +5V** | Resistor $R_4$ ($220\ \Omega$) | Limitador de Corrente do IR |
| **Resistor $R_4$** | LED IR 940nm (Ânodo) | Alimentação do Emissor |
| **LED IR 940nm (Cátodo)** | Transistor $Q_1$ Coletor (Pino 1) | Chaveamento de Potência NPN |
| **Transistor $Q_1$ Emissor (Pino 3)**| Trilho GND | Aterramento do Emissor de $Q_1$ |
| **ESP32 GPIO 4** | Resistor $R_5$ ($1\text{ k}\Omega$) | Saída PWM 38 kHz para o IR |
| **Resistor $R_5$ (Saída)** | Transistor $Q_1$ Base (Pino 2) | Disparo da Base do Transistor |
| **Transistor $Q_1$ Base (Pino 2)** | Resistor $R_6$ ($100\text{ k}\Omega$) | *Pull-down* de Proteção |
| **Resistor $R_6$ (Saída)** | Trilho GND | Aterramento do *Pull-down* |
| **Trilho 3V3** | Módulo SCD40 VCC | Alimentação do Sensor CO₂ |
| **Trilho GND** | Módulo SCD40 GND | Aterramento do SCD40 |
| **ESP32 GPIO 21** | Módulo SCD40 SDA | Linha de Dados I2C |
| **ESP32 GPIO 22** | Módulo SCD40 SCL | Linha de Clock I2C |
| **ESP32 GPIO 2** | Resistor $220\ \Omega$ Azul | Sinalização de Wi-Fi/MQTT |
| **Resistor $220\ \Omega$ Azul** | LED Azul (Ânodo) | Alimentação do LED Azul |
| **LED Azul (Cátodo)** | Trilho GND | Aterramento do LED Azul |
| **ESP32 GPIO 18** | Resistor $220\ \Omega$ Amarelo | Sinalização de Heartbeat |
| **Resistor $220\ \Omega$ Amarelo**| LED Amarelo (Ânodo) | Alimentação do LED Amarelo |
| **LED Amarelo (Cátodo)** | Trilho GND | Aterramento do LED Amarelo |

---

## 9. Mapeamento Físico de Coordenadas na Protoboard (Matriz 830 Furos)

Seguindo a convenção padrão de protoboards (linhas numeradas de 1 a 60, colunas `a` a `e` na metade esquerda, canal central isolante, e colunas `f` a `j` na metade direita):

| Componente / Conexão | Coordenada Inicial | Coordenada Final | Observação |
| :--- | :--- | :--- | :--- |
| **Alimentação IR** | Trilho +5V | `a3` | Jumper Vermelho |
| **Resistor $R_4$ (220 Ω)** | `e3` | `e7` | Limitador do LED IR |
| **LED IR (Ânodo)** | `e7` | Terminal Ânodo | Módulo KY-005 |
| **LED IR (Cátodo)** | Terminal Cátodo | `e10` | Saída do emissor |
| **Ponte de Coletor** | `c10` | `c18` | Jumper de união |
| **Transistor $Q_1$ Coletor** | `e18` | — | Pino 1 do BC547 |
| **Transistor $Q_1$ Base** | `e19` | — | Pino 2 do BC547 |
| **Transistor $Q_1$ Emissor** | `e20` | Trilho GND esquerdo | Pino 3 do BC547 ao terra |
| **Resistor $R_5$ (1 kΩ)** | `e19` | `f19` | Atravessa o canal central |
| **Comando IR (GPIO 4)** | **ESP32 GPIO 4** | `j19` | Jumper Roxo (PWM 38 kHz) |
| **Resistor $R_6$ (100 kΩ)** | `a19` | `a24` | *Pull-down* de base |
| **Retorno de $R_6$** | `a24` | Trilho GND esquerdo | Jumper Preto ao terra |
| **Comando LED Azul** | **ESP32 GPIO 2** | `a29` | Jumper Azul |
| **Resistor Azul (220 Ω)** | `c29` | `c33` | Limitador de corrente |
| **LED Azul** | `e33` (Ânodo) | `f33` (Cátodo) | Atravessa canal central |
| **Retorno LED Azul** | `j33` | Trilho GND direito | Jumper Preto ao terra |
| **Comando LED Amarelo**| **ESP32 GPIO 18** | `a39` | Jumper Amarelo |
| **Resistor Amarelo (220 Ω)**| `c39` | `c43` | Limitador de corrente |
| **LED Amarelo** | `e43` (Ânodo) | `f43` (Cátodo) | Atravessa canal central |
| **Retorno LED Amarelo**| `j43` | Trilho GND direito | Jumper Preto ao terra |

---

## 10. Checklist de Validação com Multímetro (Antes de Ligar)

Execute este roteiro com o multímetro digital em bancada antes de energizar o circuito:

1. **Teste de Continuidade (Bip) contra Curtos-Circuitos:**
   - Ponta de prova entre **+5V** e **GND**: Resistência deve ser infinita (sem bip).
   - Ponta de prova entre **3V3** e **GND**: Resistência deve ser alta (sem bip).
   - Ponta de prova entre **+5V** e **3V3**: **NUNCA** pode haver continuidade (sem bip).
2. **Conferência da Tensão de Offset ($V_{\text{BIAS}}$):**
   - Conecte o ESP32 na porta USB do computador.
   - Coloque o multímetro na escala de **Tensão Contínua (DCV 20V)**.
   - Meça a tensão entre o nó $V_{\text{BIAS}}$ e o GND: Deve registrar exatamente entre **1,63 V e 1,67 V** (metade de 3,3V).
3. **Segurança do Secundário do SCT-013:**
   - Com o circuito desligado, meça a resistência entre o Terminal A e o Terminal B do Jack P2: O multímetro deve marcar exatamente **10 Ω** (o valor de $R_b$). Isso comprova que o secundário do transformador de corrente está protegido contra sobretensão induzida.
4. **Instalação do Alicate no Aparelho de Ar-Condicionado:**
   - Abra a trava do SCT-013 e abrace **EXCLUSIVAMENTE UMA DAS FASES** do cabo de alimentação do ar-condicionado.  
   - *Atenção:* Se você abraçar o cabo com fase e neutro juntos, os campos magnéticos opostos se anulam e a corrente medida será sempre 0 A!
