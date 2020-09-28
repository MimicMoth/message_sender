# Projeto para filtro de mensagens

O projeto consiste em um filtro de mensagens a serem enviadas.

O arquivo de entrada é em formato .txt e cada linha possui a seguinte formatação:
IDMENSAGEM;DDD;CELULAR;OPERADORA;HORARIO_ENVIO;MENSAGEM

E o arquivo de saída é em formato .txt e possui a seguinte formatação:
IDMENSAGEM;IDBROKER

# Como utilizar

Para executar o projeto utiliza-se o comando:

    python3 main.py [arg1] [arg2]

O primeiro argumento representa o nome do arquivo de "input"
O segundo argumento representa o nome do arquivo de "output"
Caso apenas um agumento seja passado, será considerado como o nome do arquivo de "input"
Caso nenhum argumento seja passado, ele irá procurar por um arquivo padrão com o nome "input.txt" e o resultado será impresso em um arquivo "output.txt"

# Regra Implementadas:


  - mensagens com telefone inválido deverão ser bloqueadas(DDD+NUMERO)
  - mensagens que estão na blacklist deverão ser bloqueadas
  - mensagens para o estado de São Paulo deverão ser bloqueadas
  - mensagens com agendamento após as 19:59:59 deverão ser bloqueadas
  - as mensagens com mais de 140 caracteres deverão ser bloqueadas
  - caso possua mais de uma mensagem para o mesmo destino, apenas a mensagem apta com o menor horário deve ser considerada
  - DDD com 2 digitos
  - DDD deve ser válido
  - número celular deve conter 9 dígitos
  - numero celular deve começar com 9
  - o segundo dígito deve ser > 6;

| ID_BROKER | OPERADORAS |
| ------ | ------ |
| 1 | VIVO, TIM |
| 2 | CLARO, OI |
| 3 | NEXTEL |

# Unit Test

Foi utilizado o modulo unittest do Python para rodar os testes unitarios
O arquivo está em tests.py e pode ser rodado com:

    python3 test.py

Os teste unitarios buscam validar as funções utilizadas para o projeto

Também tem um arquivo "teste.txt" que pode ser rodado para validar os resultados

    python3 main.py teste.txt

A saída esperada é:

    05;1
    14;2
    15;3

# Tecnologias Utilizadas:
  - Python 3.6.9
  - Para regras do numero foi utilizado RegEx e para comparação de tempo foi utilizada datetime.time
  - Para teste foi utilizado o modulo unittest
  - VScode
  - Ambiente Linux
