# Roteiro de condução — 26/09/2026 — 240 minutos

Os slides apoiam a explicação; não ler cada nota em voz alta. Os quatro slides de consulta são aprofundamento fora do percurso cronometrado. A API é demonstração do professor; cada equipe continua seu projeto. Preparar build e links antes da aula.

| Minutos | Bloco | Como conduzir |
|---|---|---|
| 0–10 | Contexto | Retomar E4/E5, objetivo e trajetória do usuário. |
| 10–40 | Sinais | Logs, métricas, traces, arquitetura de coleta; primeira verificação. |
| 40–60 | Objetivos | Calcular SLI, SLO e orçamento de erro; discutir alertas e gabarito. |
| 60–80 | Incidente | Linha do tempo, hipóteses e post-mortem sem culpabilização. |
| 80–95 | Intervalo | 15 minutos. |
| 95–125 | Demonstração | Referência, banco parado, evidências, recuperação, gabarito. |
| 125–145 | IA aplicada | Prompt, sugestão rejeitada, limites de automação e gabarito. |
| 145–180 | Preparação | 35 minutos para conferir o projeto, ensaio e evidências. |
| 180–236 | Apresentações | Até sete slots de 8 min; fala de 5–7 min + transição/feedback. |
| 236–240 | Fechamento | Conferir entrega no repositório e sintetizar aprendizado. |

Com menos equipes, usar o saldo para preparação e feedback. Se houver mais de sete, ajustar a exposição previamente, preservando o tempo oficial das falas. As verificações são formativas em grupo, sem nota individual adicional.

## Antes da aula

Executar o laboratório; confirmar Docker, porta e download das imagens. Abrir versão, logs e sonda em terminais preparados. Conferir número e ordem das equipes. Separar evidências prévias identificadas para contingência. Ler as notas dos slides de percentis, error budget e recuperação para não misturar populações/janelas.

## Durante a demonstração

Anotar total N antes da falha. Comparar a MESMA operação nas três janelas. Relacionar ID da resposta ao log correspondente. Explicar por que live=200 pode coexistir com visitas=503. Restaurar db, confirmar prontidão, repetir sonda e conferir N. Encerrar o ensaio sem remover volumes. A lentidão de 400 ms é opcional e fica na consulta.

## Durante as apresentações

Pedir evidência quando uma afirmação estiver vaga: “qual operação?”, “qual janela?”, “qual teste sustentou a causa?”. Não transformar a discussão em arguição com nota individual. Usar os pesos oficiais 25/25/20/15/10/5 e os descritores do enunciado. Captura anterior é aceitável se identificada; teste não executado deve ser apresentado como pendente.
