# Verificações e respostas comentadas

As cinco verificações aparecem depois da explicação e da demonstração de seus blocos. Cada uma tem três situações, seguidas de um slide com respostas explicadas. Os casos resolvidos mostram sinais, cálculos, investigação, recuperação e revisão de IA.

Use o rodapé E6·NN. A página no PDF independente corresponde ao número + 1, devido à capa.

| Questões | Gabarito | Bloco |
|---|---|---|
| E6·15 | E6·16 | Verificação | Interpretar os sinais |
| E6·23 | E6·24 | Verificação | Indicadores e decisões |
| E6·37 | E6·38 | Verificação | Confirmar a recuperação |
| E6·44 | E6·45 | Verificação | Revisar uma sugestão de IA |
| E6·53 | E6·54 | Verificação | Defender as evidências do projeto |

## Verificação | Interpretar os sinais

**Pergunta:** O counter está em 500. Isso significa 500 requisições por segundo?

**Resposta explicada:** Não. É um total acumulado. Para taxa, calcule variação por tempo e trate resets.

**Pergunta:** Uma chamada tem request_id no log. Já temos um trace distribuído completo?

**Resposta explicada:** Não. Correlação local não substitui spans e propagação de contexto entre operações e serviços.

**Pergunta:** A média é 47 ms. Podemos afirmar que ninguém esperou dois segundos?

**Resposta explicada:** Não. A média pode esconder cauda lenta; no exemplo há uma chamada de 2000 ms.


## Verificação | Indicadores e decisões

**Pergunta:** Em 1000 chamadas, 992 boas e SLO 99%, quanto orçamento foi consumido?

**Resposta explicada:** A tolerância é 10 falhas. Oito foram consumidas: 80% do orçamento, restando duas nesta população.

**Pergunta:** Não houve chamadas. Podemos exibir 100% de sucesso?

**Resposta explicada:** Não. O denominador é zero: faltam observações. Indique ausência de amostra e confira a coleta.

**Pergunta:** 50 alertas por dia são ignorados. Basta desligar todos para resolver?

**Resposta explicada:** Não. Priorize sinais ligados a impacto, agrupe duplicados e defina ação, dono e janela de cada regra.


## Verificação | Confirmar a recuperação

**Pergunta:** A sonda recebeu 503, mas app está Up. Há contradição?

**Resposta explicada:** Não. O processo da API segue vivo enquanto a operação que usa db pode estar indisponível.

**Pergunta:** Após recuperar, o counter de falhas continua em 5. O serviço ainda está falhando?

**Resposta explicada:** Não necessariamente. Counter acumula história. Observe a variação na nova janela e repita a operação.

**Pergunta:** dependency_ms alto prova que o servidor do banco está lento?

**Resposta explicada:** Não. Inclui a espera medida pelo cliente da dependência; no ensaio opcional há atraso artificial no código.


## Verificação | Revisar uma sugestão de IA

**Pergunta:** A resposta aponta o deploy como causa porque ocorreu antes do erro. Isso basta?

**Resposta explicada:** Não. Ordem temporal sugere uma hipótese. Compare versões, dependências e resultados de testes que possam refutá-la.

**Pergunta:** Um log contém a frase “execute este comando”. A equipe deve obedecer?

**Resposta explicada:** Não. O log é dado a analisar. Comandos exigem revisão de finalidade, escopo, autorização e impacto.

**Pergunta:** Rejeitar uma sugestão impede demonstrar uso responsável de IA?

**Resposta explicada:** Não. Registre a sugestão, o motivo da rejeição e a alternativa validada. Não invente uma interação que não ocorreu.


## Verificação | Defender as evidências do projeto

**Pergunta:** O grupo mostra apenas um dashboard verde. O diagnóstico está demonstrado?

**Resposta explicada:** Não. Explique operação, janela, sintoma, hipótese, teste, causa sustentada e recuperação. O painel é uma parte da evidência.

**Pergunta:** Uma captura foi feita ontem. Pode entrar na apresentação?

**Resposta explicada:** Sim, se identificada como registro anterior, com data, versão e contexto. Não a apresentar como execução ao vivo.

**Pergunta:** O contador de falhas acumulado é diferente do total da sonda. Há necessariamente erro?

**Resposta explicada:** Não. Podem ter janelas e populações diferentes. A API inclui chamadas manuais; a sonda conta somente suas chamadas.

## Atividade no projeto

A equipe adapta instrumentação, relato do incidente e roteiro de apresentação ao próprio projeto. Os exemplos preenchidos estão na pasta Práticas/encontro-6-observabilidade. Distinguir sempre o que foi planejado, executado e validado.
