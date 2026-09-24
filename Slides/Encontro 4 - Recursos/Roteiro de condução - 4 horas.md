# Encontro 4 — roteiro de condução em quatro horas

**Base antes de perguntas:** explique o componente, mostre seu funcionamento, execute um exemplo e só então peça uma previsão ou resposta. O primeiro checkpoint é E4·23, depois de fundamentos e demonstrações. O slide seguinte resolve as três situações.

A apresentação tem **78 slides + capa**: 69 na trilha principal e 9 de consulta. Os slides dividem a explicação em passos; não é necessário ler todo o texto ou todas as notas em voz alta. O guia em PowerPoint é uma seleção compacta, com os mesmos identificadores E4·NN.

## Distribuição do tempo

| Minutos | Slides | Condução |
|---|---|---|
| 0–10 | E4·01–02 | Apresentar objetivo e percurso; abrir o exemplo sem pedir respostas ainda. |
| 10–50 | E4·03–18 | Definir processo, kernel, runtimes, container, imagem, Docker e Compose. Comparar VMs somente após a base. Mapa dos recursos. |
| 50–65 | E4·19–24 | Executar versão e servidor; mostrar inspeção e ciclo de vida. Fazer a primeira verificação e explicar o gabarito. |
| 65–95 | E4·25–35 | Explicar arquivos, Dockerfile, cache e build; demonstrar API isolada. Diferenciar imagem e integração. |
| 95–110 | — | Intervalo de 15 minutos. |
| 110–145 | E4·36–53 | Ler Compose, rede, configuração e montagens. Explicar saúde, limites e restart. Subir, testar e comprovar persistência. Verificação comentada. |
| 145–165 | E4·54–59 | Seguir uma hipótese até a evidência. Demonstrar a queda do banco; usar os outros dois casos resolvidos para comparar sintomas. |
| 165–235 | E4·60–67 | 70 minutos no projeto da equipe; orientações e critérios entram nos primeiros minutos. Executar, diagnosticar e registrar. Verificação final durante a revisão das equipes. |
| 235–240 | E4·68–69 | Fechar com as evidências e ligação com E5. Indicar consulta disponível. |

Total: **240 minutos**, incluindo intervalo e laboratório. O tempo das verificações e gabaritos está dentro de cada bloco.

## Preparação e ritmo

Antes da aula, baixe as imagens, ensaie os comandos e confira portas. Comece com PRIMEIROS-PASSOS.md; a API com banco só entra depois. Deixe os arquivos completos abertos para alternar entre slide e terminal, sem pedir transcrição de YAML de uma imagem.

O bloco de integração é denso: use os slides como apoio visual e concentre a execução em subir, consultar, gravar e ler após recriação. Limites, políticas de reinício e redução de privilégios são explicados com exemplos, sem uma segunda rodada obrigatória de configuração. O mapa de recursos permite retomar dúvidas depois.

Se houver atraso, preserve a distinção dos runtimes, imagem/container, fluxo da requisição, persistência, alcance do healthcheck, uma falha comprovada e os 70 minutos no projeto. Nas tabelas de comandos, demonstre uma operação representativa e deixe as demais como referência. Não suprima o gabarito de uma pergunta que foi apresentada.

Durante os 70 minutos, as equipes trabalham em paralelo: 0–20 empacotar; 20–45 integrar; 45–70 validar e registrar. Apresente critérios nos primeiros minutos e use a verificação final na conversa de revisão. A rubrica continua com os pesos oficiais; Containers/Compose corresponde a 20%.

## Como explicar os pontos difíceis

**Runtime:** “Node executa o nosso JavaScript. O runtime de containers prepara a execução isolada do processo. Os dois aparecem no desenho porque têm trabalhos diferentes.”

**Imagem e container:** “A imagem fornece os arquivos de origem. A instância recebe comando, rede, configuração e uma camada gravável. Duas instâncias da mesma imagem podem ter estados diferentes.”

**Docker e Compose:** “A CLI pede operações ao Engine. Compose transforma a descrição dos serviços em operações sobre esse Engine. Dockerfile constrói; Compose descreve a execução integrada.”

**VM:** “Na VM há um kernel convidado. Containers Linux compartilham o kernel do ambiente Linux em que rodam. Esse ambiente pode ser uma VM, como no Desktop.”

**localhost:** “Primeiro identifique quem inicia a conexão. Dentro da API, localhost aponta para a própria instância. Para chegar ao banco do exemplo, a API usa db:5432.”

**Persistência:** “O teste é comparar o valor antes e depois da recriação, usando o mesmo volume. A existência da palavra volumes no YAML não substitui essa observação.”

**Saúde e reinício:** “Healthcheck observa um contrato. Restart reage ao encerramento do processo. Uma marca unhealthy não aciona automaticamente uma política de reinício.”

**Recursos:** “Logs explicam o que a aplicação emitiu; inspect consulta o objeto; exec inicia outro comando; stats mostra consumo. Cada comando responde a uma pergunta diferente.”

## Consulta depois do fechamento

E4·70–78: registry/tag/digest, multi-stage, imagem no CI, tmpfs, drivers de rede, profiles, overrides/Watch, BuildKit/Buildx e outros recursos do ecossistema. São explicações adicionais, sem aumentar a entrega obrigatória. Use conforme as perguntas e a stack das equipes.

- [Mapa dos recursos do Docker](Mapa%20dos%20recursos%20do%20Docker.md)
- [Verificações e gabaritos](Índice%20de%20perguntas%20e%20respostas.md)
- [Explicações por slide](Guia%20ampliado%20do%20professor.md)
