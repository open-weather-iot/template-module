# TEMPLATE DE MÓDULO
Esse repositório é um template para um módulo de sensor.

## Utilizando esse template
Para criar um novo módulo, siga os seguintes passos:
- Crie um repositório no GitHub nesta organização (`open-weather-iot`)
- Selecione o template `template-module`
<img src="img/template-picker.png">

- Dê um nome no formato `{sensor}-module`. Exemplo: `temperature-module`
<img src="img/repo-name.png">

- Não é necessário escrever uma descrição
- Deixe o projeto público. **Não faça upload de nenhum arquivo com informações sensíveis**
<img src="img/visibility.png">

Após a inicialização do repositório:
- Reescreva o arquivo README.md com a descrição do projeto, incluindo o que é, informações necessárias, detalhes de execução e o restante que julgar pertinente.
- Inclua os arquivos necessários nas pastas descritas em na seção seguinte ([Organização de pastas e arquivos](#organizacao))

## Organização de pastas e arquivos <a id="organizacao"></a>
- `altium/`: arquivos do Altium
- `documents/`: especificações e PDFs utilizados para o desenvolvimento do sub-projeto
- `gerber_files/`: export de arquivos Gerber
- `img/`: imagens utilizadas na descrição do README.md
- `lib/`: bibliotecas utilizadas pelos módulos de sensores
- `src/`: diretório do código-fonte. Todo código deverá ser colocado aqui, exceto quando é utilizado exclusivamente para testes
  - `example.py`: módulo exemplo de um sensor
- `test/`: diretório com os arquivos para execução de testes
  - `main.py`: arquivo principal da rotina de execução de testes. Importa as classes e funções do diretório do código-fonte (`src/`)
- `util/`: códigos comuns ("utilitários"). São utilizados por vários módulos de sensores
  - `bus.py`: utilitário de barramentos SPI, Serial e I2C
  - `fast_sampling.py`: faz a amostragem rápida do sensor especificado
  - `has_method.py`: verifica se uma classe possui um método com o nome especificado

Os arquivos `.gitkeep` existem nas pastas vazias para que elas sejam reconhecidas pelo git e incluídas no template. Após popular seu conteúdo, esses arquivos devem ser removidos.

## Base para uma classe de sensor <a id="base-sensor"></a>
A base para um sensor é uma classe, a qual obedece aos seguintes métodos (funções):
- `__init__(self, *, ...)`: o construtor da classe deve receber os parâmetros nomeados necessários e o barramento utilizado (seja SPI, Serial ou I2C)
- `reset(self)` (**opcional**): contém as rotinas de reset do estado interno do módulo do sensor, caso necessário. É executado em caso de erro no sensor (uma *Exception* foi lançada durante a leitura)
- `setup(self)` (**opcional**): contém as rotinas de inicialização do módulo do sensor, caso necessário. É executado no momento de inicialização da estação
- `read(self)` (**obrigatório**): retorna um dicionário com as seguintes chaves:
  - `raw`: contém um dicionário com os valores puros que foram lidos do sensor que se está trabalhando
  - `value`: representa o valor final após conversão de unidades para ser apresentado diretamente ao usuário
  - `unit`: unidade de medida do campo `value`. Exemplos: `'ºC'`, `'V'`, `'m/s'`

```py
class Example:
    # deve receber os parâmetros nomeados necessários e o barramento utilizado (seja SPI, Serial ou I2C)
    def __init__(self, i2c_bus):
        self.i2c_bus = i2c_bus

    # método **OPCIONAL** que reseta o estado interno do sensor
    def reset(self):
        pass

    # método **OPCIONAL** que inicia o sensor
    def setup(self):
        pass

    # método **OBRIGATÓRIO** que realiza leituras do sensor
    def read(self):
        return { 'raw': {}, 'value': 0.0, 'unit': '' }

```

## Utilitários
Alguns utilitários básicos são definidos na pasta `util/`.

### `bus.py`
Utilitário de barramentos SPI e I2C.

**SPI**: A classe respectiva para o barramento SPI obedece à seguinte especificação:
- construtor `SPI(port)`:
- `select()`: ativa o dispositivo SPI
- `deselect()`: desativa o dispositivo SPI
- gerenciador de contexto `with`: inicia uma sessão de utilização do SPI. Ativa e desativa o *chip select* automaticamente
- `_spi`: Atributo utilizado internamente que armazena a instância `machine.SPI`. Não é recomendável utilizar diretamente esse atributo, exceto nos casos de bibliotecas de componentes que recebem uma instância `machine.SPI`.
- `_cs_pin`: Atributo utilizado internamente que armazena o número do pino de *chip select*. Não é recomendável utilizar diretamente esse atributo, exceto nos casos de bibliotecas de componentes que recebem o número do pino de *chip select*.
- `_cs`: Atributo utilizado internamente que armazena a instância `machine.Pin` (*output*) do *chip select*. Não é recomendável utilizar diretamente esse atributo, exceto nos casos de bibliotecas de componentes que recebem uma instância `machine.Pin`.

#### Exemplo
```py
from util.bus import SPI
from xyz42 import XYZ42_SPI

spi_bus = SPI(port=1)

# ativa e desativa o dispositivo SPI automaticamente dentro desse contexto/bloco
with spi_bus as spi:
    spi.write(b'12345678') # escreve os bytes 12345678
    MSB = spi.read(1) # lê 1 byte
    LSB = spi.read(1) # lê 1 byte

# (1) ativa o dispositivo SPI, (2) escreve os bytes 12345678, (3) desativa o dispositivo SPI
spi_bus.select()
spi_bus._spi.write(b'12345678')
spi_bus.deselect()

# expondo para o módulo hipotético XYZ42 a instância interna `machine.SPI` e o `machine.Pin` do chip select
xyz = XYZ42_SPI(spi=spi_bus._spi, cs=spi_bus._cs)
```

**I2C**: A função que constrói um barramento I2C obedece à seguinte especificação:
- `def I2C(bus)`: são suportados os barramentos (*bus*) `0` e `1`. Retorna uma instância `machine.I2C` conectada nos pinos respectivos do barramento selecionado

#### Exemplo
```py
from util.bus import I2C
from xyz42 import XYZ42_I2C

i2c_bus = I2C(bus=1)

xyz = XYZ42_I2C(i2c=i2c_bus)
```

### `fast_sampling.py`
Utilitário que realiza a amostragem rápida do sensor especificado.

A implementação atual não suporta a utilização mais de uma vez do *FastSampling* (como a Raspberry Pi Pico possui apenas dois núcleos, o código principal roda no núcleo *core0* e a thread para amostragem rápida no *core1*, não sendo possível criar mais threads).

Requisitos:
- a classe do sensor deve possuir o método `read` definido [acima](#base-sensor)
- se o parâmetro `sampling_rate_hz` não for informado, é utilizado o atributo `sampling_rate_hz` do sensor. Especifica a taxa de amostragem e deve ser uma string
- se o parâmetro `reducer` não for informado, é utilizado o método `reducer` do sensor. Especifica a função de agregação das amostragens, recebe como parâmetro a lista de amostras e deve retornar os dados no mesmo formato que o `read` do sensor
- o método `reset` chama o método `reset` do sensor, caso ele exista
- o método estático `stop_thread` deve ser executado quando for necessário encerrar a thread criada (para não ocorrer erros ao iniciar novamente o *FastSampling*)


#### Exemplo
```py
from util.bus import I2C
from util.fast_sampling import FastSampling
from src.example import Example

def main():
    # ...

    sensors = {
        'example_sensor': FastSampling(Example(I2C(bus=0))),
    }

    # ...

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        FastSampling.stop_thread()
        print(f'got error `{type(e).__name__}: {e}` on main')
```

### `has_method.py`
Utilitário que verifica se uma classe possui um método com o nome especificado.

#### Exemplo
```py
from util.has_method import has_method

if has_method(sensor, 'reset'):
    sensor.reset()
```

## Orientações gerais
### Import
Não importe módulos inteiros.

> ❌
> ```py
> from example import *
> ```

> ✅
> ```py
> from example import Example
> ```

---

### Variáveis e instruções globais
Evite utilizar variáveis e instruções globais para prover uma melhor modularização do código.

> ❌
> ```py
> # src/blink_led.py
> from time import sleep_ms
> from machine import Pin
>
> led_builtin = Pin(25, Pin.OUT)
> led_builtin.value(1)
> interval = 1000
>
> def blink():
>     while True:
>         led_builtin.toggle()
>         sleep_ms(interval)
>
> # test/main.py
> from src.blink_led import blink
>
> blink()
> ```

> ✅
> ```py
> # src/blink_led.py
> from time import sleep_ms
> from machine import Pin
>
> def blink():
>     led_builtin = Pin(25, Pin.OUT)
>     led_builtin.value(1)
>     interval = 1000
>
>     while True:
>         led_builtin.toggle()
>         sleep_ms(interval)
>
> # test/main.py
> from src.blink_led import blink
>
> if __name__ == "__main__":
>     blink()
> ```

> 💡 Note que com essa alteração, agora é possível parametrizar o pino do led e intervalo, deixando o código mais genérico e personalizável.
> ```py
> # src/blink_led.py
> from time import sleep_ms
> from machine import Pin
>
> def blink(*, led_pin=25, interval=1000):
>     led = Pin(led_pin, Pin.OUT)
>     led.value(1)
>
>     while True:
>         led.toggle()
>         sleep_ms(interval)
> ```

---

### Identação
Tome cuidado para identar o código com **4 espaços**.

> ❌ Exemplo: 3 espaços
> ```py
> def test():
>    return 42
> ```

> ✅
> ```py
> def test():
>     return 42
> ```

---

### Parâmetros nomeados
Quando uma classe ou função tem objetivo de comunicar com o usuário final, dê preferência a receber e passar parâmetros pelo nome, em vez de pela ordem de passagem de parâmetros, principalmente quando há muitos parâmetros.

Essa recomendação propõe que os nomes dos parâmetros sejam expostos ao usuário da classe ou função, assim, facilitando a leitura dos parâmetros sem a necessidade de abrir o código e analisar a ordem dos parâmetros.

> ❌
> ```py
> class Example:
>     # Inicialização da classe Example
>     # recebe os pinos utilizados para o SPI
>     def __init__(self, clk_pin, sdi_tx_pin, sdo_rx_pin, cs_pin, spi_id):
>         pass
>
> # ...
>
> ex = Example(10, 11, 12, 13, 1)
> ```

> ✅
> ```py
> class Example:
>     # Inicialização da classe Example
>     # recebe os pinos utilizados para o SPI
>     def __init__(self, *, clk_pin, sdi_tx_pin, sdo_rx_pin, cs_pin, spi_id):
>         pass
>
> # ...
>
> ex = Example(clk_pin=10, sdi_tx_pin=11, sdo_rx_pin=12, cs_pin=13, spi_id=1)
> ```

> 💡 Note que basta colocar `*` na posição a partir da qual deseja-se que os parâmetros seguintes sejam passados pelo nome, não por ordem

> 💡 Não é sempre necessário utilizar parâmetros nomeados, por exemplo, quando há poucos parâmetros e os valores são auto-descritivos
> ```py
> # src/max31865.py
> class MAX31865:
>     def __init__(self, spi_bus):
>         self.spi_bus = spi_bus
>
> # test/main.py
> from src.max31865 import MAX31865
> from util.bus import SPI
>
> def main():
>     sensors = {
>         "t1": MAX31865(SPI(port=1))
>     }
>
>     # ...
>
> if __name__ == "__main__":
>     main()
> ```

---

### Parâmetros de inicialização de classes
Valores padrão podem ser utilizados para parâmetros que definam comportamentos do módulo/função. Porém, não utilize valores padrão quando se refere ao hardware (por exemplo, um pino).

Essa recomendação facilita no momento de integração de códigos e resolução de conflito de pinagem.

> ❌
> ```py
> class Example:
>     # Inicialização da classe Example
>     # recebe os pinos utilizados para o SPI
>     def __init__(self, *, clk_pin=10, sdi_tx_pin=11, sdo_rx_pin=12, cs_pin=13, spi_id=1):
>         pass
> ```

> ✅
> ```py
> class Example:
>     # Inicialização da classe Example
>     # recebe os pinos utilizados para o SPI
>     def __init__(self, *, clk_pin, sdi_tx_pin, sdo_rx_pin, cs_pin, spi_id):
>         pass
> ```

> ✅
> ```py
> # interval: intervalo de envio de dados (em segundos)
> def send(interval=10):
>     pass
> ```
