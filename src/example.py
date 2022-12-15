class Example:
    # deve receber os parâmetros nomeados necessários e o barramento utilizado (seja SPI, Serial ou I2C)
    def __init__(self, spi_bus):
        self.spi_bus = spi_bus

    # método **OPCIONAL** que reseta o estado interno do sensor
    def reset(self):
        pass

    # método **OPCIONAL** que inicia o sensor
    def setup(self):
        pass

    # método **OBRIGATÓRIO** que realiza leituras do sensor
    def read(self):
        # raw: os valores puros que foram lidos do sensor que se está trabalhando
        # value: representa o valor após conversão de unidades para ser apresentado diretamente ao usuário final
        # unit: unidade de medida
        return { 'raw': {}, 'value': 0.0, 'unit': '' }
