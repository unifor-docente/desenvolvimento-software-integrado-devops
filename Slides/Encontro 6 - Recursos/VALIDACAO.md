# Validação do encontro 6 — 23/09/2026

## Materiais

- 60 páginas na apresentação independente: capa institucional + 59 slides de conteúdo.
- Cinco verificações, 15 questões e 15 respostas explicadas; gabaritos imediatamente após as questões.
- 11 diagramas/esquemas editáveis; quatro slides opcionais de consulta.
- Notas do apresentador e referências oficiais em todos os slides de conteúdo.
- Conteúdo do E6 incorporado ao conjunto principal (257–316) e ao guia em PowerPoint.
- Comparação automatizada confirmou textos dos demais encontros e anexos preservados nas apresentações; outros capítulos preservados no DOCX.
- Inspeção visual das 60 páginas, incluindo capa, tabelas, código, figuras e gabaritos; sem cortes identificados.
- Verificação de texto nas 751 caixas do PDF: duas divergências de ordem de extração do sinal de menos, conferidas visualmente nas páginas 11 e 19; não são perdas de conteúdo.
- Sumário da apostila atualizado; E6 começa na página 107, projeto integrador na 134; apostila completa com 144 páginas.
- Roteiro de 240 minutos, com 35 para preparação e 56 para apresentações de até sete equipes. Pesos oficiais 25/25/20/15/10/5 preservados.

## Laboratório executado

Projeto Docker isolado; imagens construídas e Compose validado. O primeiro ensaio mostrou que prontidão do banco isoladamente não basta para iniciar a janela de recuperação. Foi incluído `aguardar.py`, que consulta a prontidão pela API; o ensaio final usou esse helper e passou.

| Janela | Boas / amostras | p95 do cliente (ms) |
|---|---|---|
| Antes | 10 / 10 | 18.65 |
| Banco parado | 0 / 5 | 1502.76 |
| Após recuperar | 10 / 10 | 28.13 |
| Atraso artificial de 400 ms | 10 / 10 | 418.76 |
| Atraso removido | 10 / 10 | 19.08 |

Também verificados: contador preservado; API não recriada durante a parada/retomada de db; correlação entre X-Request-Id e log; query string não registrada; buckets cumulativos e +Inf igual a count; reset de métricas após recriação de app no caso opcional. O projeto de teste foi encerrado com `down`, mantendo o volume.

Os tempos são amostras pequenas deste ambiente e não um benchmark ou SLO de produção. Traces e dashboards são explicados conceitualmente; o laboratório implementa logs, métricas e sonda, sem instalar uma plataforma de coleta. Resultado estruturado: `Práticas/encontro-6-observabilidade/resultado-validacao.json`.
