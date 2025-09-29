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