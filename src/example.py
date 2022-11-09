class Example:
    # deve receber como parâmetros os pinos em que o sensor deverá se conectar
    def __init__(self):
        pass

    # método obrigatório da classe que realiza leituras do sensor
    def read(self):
        # raw: os valores puros que foram lidos do sensor que se está trabalhando
        # value: representa o valor após conversão de unidades para ser apresentado diretamente ao usuário final
        # unit: unidade de medida
        return { 'raw': {}, 'value': 0.0, 'unit': '' }
