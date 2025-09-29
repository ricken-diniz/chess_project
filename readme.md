### Xadrez

O código foi feito completamente em cima das bibliotecas padrões do python, logo, para conseguir rodá-lo, é simples, basta executar: ```$python3 -m main```
Lembre de executar na raiz do projeto.

Se tiver interesse em jogar o modo multijogador, saiba que ele é ideal para VMs (do inglês, Virtual MAchine), o intuito é conseguir estabelecer a comunicação entre diferentes usuários em um terminal linux.

Para isso, um usuário irá interagir com a interface pelo script python que será executado, e o outro irá ler um arquivo de "pipeline", enquanto envia suas respostas por outro arquivo identico.

Em uma tela, execute: ```$cat /tmp/fifow```
Nesta tela você conseguirá assistir o jogo por completo.

Em outra tela (terminal), execute: ```$tee -a /tmp/fifor```
Nesta tela você será capaz de enviar suas respostas.

Vale salientar que o modo multiplayer exige que você execute os comandos sempre após o script python ser executado, e, se você tiver dificuldades com permissões para ler e escrever, tente executar todos os comandos, inclusive o script python, com permissão de sudouser. (Ex.: sudo python3 -m main)

Se divirta!


### Parte Técnica

Foram aplicadas manipulações de terminal e comandos linux, usando o pacote python padrão os, e, para a lógica, conceitos de Programação Orientada a Objetos, aplicando técnicas de Classes, Heranças, Polimorfismo e Encapsulamento, com o intuito de diminuir redundâncias, melhorar a legibilidade do código e facilitar a manuntenção.

Além disso, vários conceitos de lógica de programação foram aplicados, como algoritmos conhecidos como: contador, distância euclidiana, função afim, e diversos tipos de lógicas para possibilitar a criação de todas as regras!

Para completar, a infraestrutura foi montada em cima do modo de jogo local e multiplayer, permitindo jogar de forma competitiva em diferentes desktops, acessando uma mesma máquina. Para isso, foi utilizado a técnica em pipeline conhecida como fifo, que permite a transição de entradas e saídas dinâmicas.
                                                                                                          