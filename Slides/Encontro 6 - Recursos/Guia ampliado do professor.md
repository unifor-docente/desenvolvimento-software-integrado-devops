# Encontro 6 — Guia ampliado do professor

59 slides de conteúdo + capa institucional • 26/09/2026 • 4h presenciais. No conjunto principal: posições 257–316. Revisão: 23/09/2026.

Sequência: fundamentos e sinais → indicadores e objetivos → investigação → demonstração → revisão de IA → preparação e apresentação do projeto. Preservar 35 minutos de preparação e 56 de apresentações (até sete equipes, falas de 5–7 minutos). O exemplo da API não substitui o projeto escolhido. As verificações têm gabaritos comentados; os últimos quatro slides são consulta.

## E6.01 — Fechar o ciclo: da entrega à evidência

Encontro 6 • observabilidade, diagnóstico e apresentação final

**Retomar:** E4: executar e integrar. E5: entregar e recuperar. E6: observar o efeito da mudança.

**Compreender:** Logs, métricas e traces. Indicadores, objetivos e alertas. Incidente com causa comprovada.

**Demonstrar:** Instrumentação mínima. Relatório do incidente. Apresentação do mesmo projeto da equipe.

**Como explicar:** Comece pela experiência do usuário, não pela lista de ferramentas. A equipe já tem aplicação, pipeline, containerização e plano de entrega. Hoje precisa explicar o que aconteceu na execução, como soube e o que fez com essa informação. O projeto não muda, e a API do professor é apenas uma demonstração. A apresentação final tem cinco a sete minutos e usa evidências do repositório, sem uma entrega paralela fora dele.

**Conclusão prática:** Uma entrega só gera aprendizado quando seu comportamento pode ser observado e explicado.

## E6.02 — Quatro horas com espaço para as apresentações

Planejamento para até sete equipes • ajustar ao número real de grupos

**0–80 min | Base:** 0–10: contexto. 10–40: sinais e instrumentação. 40–60: SLI/SLO e alertas. 60–80: diagnóstico de incidente.

**80–180 min | Aplicar:** 80–95: intervalo. 95–125: demo guiada. 125–145: IA e revisão. 145–180: preparação das equipes.

**180–240 min | Fechar:** 180–236: até 7 blocos de 8 min. Cada fala: 5–7 min. 236–240: síntese e submissão final.

**Como explicar:** São 240 minutos, com 15 de intervalo, 35 de preparação e 56 reservados às apresentações. Cada bloco de oito minutos inclui a fala de cinco a sete e o restante para feedback ou transição. Com menos equipes, devolva o tempo à preparação ou ao feedback. O número de sete blocos acomoda a faixa usual de vinte a trinta estudantes em grupos de quatro a cinco; não é uma nova regra de formação. Se a turma tiver mais grupos, replaneje a exposição antes da aula, preservando o tempo oficial de cada fala.

**Conclusão prática:** O último encontro precisa de tempo para observar, preparar evidências e apresentar; não apenas exposição.

## E6.03 — Comece pelo caminho que o usuário percorre

Exemplo conhecido: consultar o contador de visitas

**Cliente:** GET /visitas Espera resposta correta

**API:** Recebe e processa Consulta a dependência

**Banco:** Lê o contador Responde à consulta

**Cliente:** Recebe status e corpo Percebe tempo e resultado

**Como explicar:** Trace a operação do ponto de vista de quem a utiliza. Um processo vivo ou uma conexão SQL isolada não comprovam que o resultado final chegou corretamente. Na demonstração, o cliente mede o tempo total da chamada e a API mede a parte executada no servidor. Os valores podem diferir por incluir etapas diferentes. Esse mapa orienta onde instrumentar e qual dado procurar quando o usuário relata erro ou lentidão.

**Conclusão prática:** Observe uma operação relevante; CPU baixa ou container Up não provam que ela funciona.

## E6.04 — Monitoramento e observabilidade: capacidades próximas

Medir o conhecido e investigar o comportamento do sistema

**Monitorar:** Acompanhar condições escolhidas. Ex.: erro e duração de uma rota. Detectar desvio de um critério.

**Investigar:** Combinar sinais e contexto. Explorar uma falha ainda não prevista. Formular e testar hipóteses.

**Instrumentar:** Emitir dados úteis no código. Preservar versão, tempo e contexto. Coletar e consultar os sinais.

**Como explicar:** Evite apresentar monitoramento e observabilidade como produtos rivais. As capacidades se sobrepõem: um painel pode revelar um problema e uma investigação pode usar o mesmo dado com outra pergunta. Instalar um dashboard não cria observabilidade automaticamente. É preciso emitir sinais pertinentes, coletá-los e interpretá-los. No projeto pequeno, um log estruturado, uma medição definida e um teste funcional já apoiam uma investigação concreta.

**Conclusão prática:** Ferramenta organiza dados; a instrumentação e o contrato da aplicação dão significado a eles.

## E6.05 — Logs, métricas e traces: três perspectivas

Cada sinal responde melhor a um tipo de pergunta

| Sinal | O que representa | Exemplo |
| --- | --- | --- |
| Log | Registro de um evento com contexto. | Requisição terminou com 503 e código de erro. |
| Métrica | Medição agregada ao longo do tempo. | 5 falhas em 20 requisições. |
| Trace | Caminho e duração de operações correlacionadas. | API aguardou uma chamada à dependência. |

**Como explicar:** Uma linha de log descreve um evento; a métrica permite comparar volume ou distribuição; o trace relaciona operações de uma execução. Eles não são os únicos sinais possíveis, nem é obrigatório implantar os três em todo projeto. O laboratório gera logs e métricas; traces serão explicados por um diagrama conceitual. Não chamaremos um request_id isolado de tracing distribuído. A escolha deve seguir o que a equipe precisa investigar.

**Conclusão prática:** Combine perspectivas; não espere que um único sinal prove sozinho toda a causa.

## E6.06 — Log estruturado: campos que apoiam o diagnóstico

Exemplo ilustrativo com valores fictícios • JSON facilita consulta

**Contexto:** timestamp: quando. version: qual código. request_id: qual chamada.

**Resultado:** route e status: operação e resposta. duration_ms: tempo no servidor. error_code: pista da falha.

```
{"timestamp":"2026-09-26T12:00:00Z",
 "service":"api-visitas",
 "version":"3.0.0-observabilidade",
 "request_id":"exemplo-123",
 "method":"GET", "route":"/visitas",
 "status":503, "duration_ms":12.4,
 "error_code":"ECONNREFUSED"}
```

**Como explicar:** Leia os campos na ordem da investigação. A hora situa o evento, versão liga ao release, rota define a operação e request_id permite localizar o mesmo atendimento. O exemplo não deve ser copiado como resultado real da equipe. A duração da API mede do recebimento até preparar a resposta; não inclui toda a rede do cliente. O log não inclui senha, corpo enviado ou query string. Um error_code é evidência a interpretar, não diagnóstico final sem contexto.

**Conclusão prática:** Um log útil permite localizar o evento sem expor dados que a investigação não precisa.

## E6.07 — O que registrar — e o que não precisa ir para o log

Utilidade, retenção e acesso fazem parte do desenho

**Registrar:** Evento, hora e serviço. Rota normalizada, status e duração. Versão e identificador de correlação.

**Evitar:** Senha, token e cabeçalho de autorização. Payload completo sem necessidade. Dados pessoais e URLs sensíveis.

**Controlar:** Quem consulta e por quanto tempo. Volume e nível dos eventos. Separar produção de dados fictícios.

**Como explicar:** Um dump de environment ou request completo pode vazar informação. Níveis info, warn e error ajudam a filtrar, mas precisam de uma convenção coerente. Um aviso não é automaticamente um incidente; um evento info pode mostrar uma mudança importante. IDs também podem permitir correlação com pessoas, dependendo do sistema, então não assuma que todo identificador é irrelevante para privacidade. Para a aula, use requisições e registros fictícios e apenas os campos necessários.

**Conclusão prática:** Mais texto não significa mais evidência; selecione contexto que ajude a responder a uma pergunta.

## E6.08 — Identificação da requisição: ligar resposta e evento

No laboratório a API gera X-Request-Id para cada chamada

**Resposta HTTP:** Cabeçalho com o ID Copiar o valor observado

**Log da API:** Mesmo request_id Status, versão e duração

**Investigação:** Localizar aquele evento Comparar com outros sinais

**Como explicar:** Demonstre curl -i para obter o cabeçalho e depois procure o ID exato no log. A API gera um UUID, sem confiar em um valor arbitrário do cliente. Isso permite correlacionar o atendimento local. Um trace distribuído ainda exige propagar contexto entre serviços e registrar spans relacionados. O identificador não deve ser usado como label de métrica, pois criaria uma série por requisição. Mostre essa distinção antes de introduzir histogramas e traces.

**Conclusão prática:** request_id é uma chave de correlação; sozinho não descreve o caminho distribuído.

## E6.09 — Tipos de métrica: conte, meça e distribua

Escolher o tipo evita interpretações erradas

| Tipo | Comportamento | Exemplo |
| --- | --- | --- |
| Counter | Acumula eventos; pode zerar na reinicialização. | Total de respostas 503. |
| Gauge | Valor que pode subir e descer. | Memória usada ou fila atual. |
| Histograma | Conta observações em faixas de valores. | Duração das requisições. |

**Como explicar:** Counter não é a quantidade de requisições por segundo: é o total acumulado desde uma referência. Para taxa, compare a variação e o intervalo, considerando reinícios. Gauge representa um estado atual, como tamanho de fila. Histograma organiza uma distribuição; no formato clássico do Prometheus as faixas são cumulativas. O laboratório expõe counters e histograma em memória; docker stats oferece uma observação de recursos, sem histórico por si só.

**Conclusão prática:** Diga sempre o nome, a unidade, a população e o intervalo da medição.

## E6.10 — De contador a taxa: exemplo resolvido

Mesma instância, sem reinício entre as duas leituras

| Observação | Cálculo e interpretação |
| --- | --- |
| 12:00:00 → total 100 | Primeira leitura do counter. |
| 12:00:10 → total 140 | Foram concluídas 40 requisições no intervalo. |
| Taxa média | (140 − 100) / 10 s = 4 requisições/s. |
| Se o valor caiu para 3 | Pode ter ocorrido reset; não calcular uma taxa negativa. |

**Como explicar:** Faça a subtração no quadro antes de usar uma função de consulta. O exemplo exige a mesma série e um intervalo definido. Um reset por reinício da API muda a referência do contador; sistemas de consulta podem tratar isso, mas duas leituras soltas não reconstroem todos os eventos perdidos. Agregar contadores de instâncias sem separar resets também exige cuidado. Não confunda requisições por segundo com latência em segundos por requisição.

**Conclusão prática:** Counter é total; taxa é variação por tempo; reinícios mudam como a variação deve ser interpretada.

## E6.11 — Média e percentil mostram coisas diferentes

Exemplo sintético: 100 requisições ordenadas por duração

**Como explicar:** A distribuição tem 95 valores de 20 ms, quatro de 200 ms e um de 2000 ms. A média é (95×20 + 4×200 + 1×2000)/100 = 47 ms. Pelo método nearest-rank, p95 é o 95º valor, 20 ms, e p99 é o 99º, 200 ms. A requisição de dois segundos fica além do p99 neste conjunto. Métodos de percentil e estimativas por buckets podem diferir. Explique a população e a janela; não transforme uma amostra curta numa garantia para o mês.

**Conclusão prática:** Uma média baixa pode conviver com requisições lentas; percentil também depende da amostra e do método.

## E6.12 — Trace: visualizar a duração e a relação entre operações

Diagrama conceitual • valores ilustrativos, não capturados no laboratório

**Como explicar:** Um trace reúne spans ligados por contexto. Um span representa uma operação com início, fim e atributos; o vínculo pai-filho ajuda a reconstruir a execução. No desenho a API dura 120 ms e a chamada ao banco ocupa parte desse intervalo, 80 ms. Não some duração do span pai com a do filho: os intervalos se sobrepõem. Operações paralelas também impedem somas ingênuas. Um trace amostrado conta a história daquele atendimento, não garante cobertura de todas as chamadas.

**Conclusão prática:** Spans mostram relações e intervalos; duração maior sugere onde investigar, não prova a causa sozinha.

## E6.13 — Do código ao painel: como a telemetria chega à consulta

Separar instrumentação, transporte, armazenamento e uso

**Emitir:** Aplicação registra Logs, medidas ou spans

**Coletar:** Agente/coletor obtém Processa e encaminha

**Armazenar:** Backend indexa Mantém histórico

**Usar:** Consultar e visualizar Alertar e investigar

**Como explicar:** OpenTelemetry fornece padrões e componentes para instrumentar, coletar e exportar; não é, por si só, o banco que armazena todos os dados nem o dashboard final. Prometheus pode coletar métricas por scraping; ferramentas de visualização consultam fontes configuradas. A demonstração mínima lê logs pelo Docker e consulta o endpoint de métricas e uma sonda Python. Não vamos fingir que essa combinação já tem retenção centralizada, tracing ou alta disponibilidade de observabilidade.

**Conclusão prática:** O dado precisa chegar à consulta com contexto; emitir um endpoint não cria automaticamente histórico.

## E6.14 — Ferramentas: reconhecer a responsabilidade de cada uma

Exemplos de componentes • nenhuma plataforma paga é exigida

| Componente | Papel típico | Na aula |
| --- | --- | --- |
| Logs do Docker | Acessar a saída emitida pelo processo. | Usado na demonstração. |
| Prometheus | Coletar e consultar séries de métricas. | Formato de exposição e consulta conceitual. |
| Grafana | Visualizar dados de fontes configuradas. | Exemplo de finalidade de dashboard. |
| OpenTelemetry / Jaeger | Instrumentar/exportar; analisar traces, respectivamente. | Conceitos e diagrama. |

**Como explicar:** Não trate ferramentas como uma lista de instalação obrigatória. Docker logs não produz logs que a aplicação não emitiu. Grafana depende de uma fonte e de consultas corretas. Um coletor pode encaminhar sinais para backends distintos. O projeto deve demonstrar observabilidade mínima com ferramentas compatíveis com seu contexto. O laboratório não instala Prometheus, Grafana ou Jaeger; evita consumir o tempo das apresentações com infraestrutura adicional.

**Conclusão prática:** Comece pela pergunta operacional; depois escolha como emitir, guardar e consultar o sinal.

## E6.15 — Verificação | Interpretar os sinais

Depois dos conceitos e exemplos • explique a evidência

**1. Situação:** O counter está em 500. Isso significa 500 requisições por segundo?

**2. Situação:** Uma chamada tem request_id no log. Já temos um trace distribuído completo?

**3. Situação:** A média é 47 ms. Podemos afirmar que ninguém esperou dois segundos?

**Como explicar:** Peça respostas breves apoiadas nos exemplos anteriores. Revele o gabarito depois de ouvir justificativas. Se houver confusão, volte à figura ou ao cálculo pertinente. As verificações são formativas e de discussão em grupo, sem criar nota individual ou alterar os pesos oficiais.

**Conclusão prática:** O próximo slide traz as três respostas explicadas.

## E6.16 — Respostas comentadas | Interpretar os sinais

Gabarito • do conceito à decisão

**1. Resposta:** Não. É um total acumulado. Para taxa, calcule variação por tempo e trate resets.

**2. Resposta:** Não. Correlação local não substitui spans e propagação de contexto entre operações e serviços.

**3. Resposta:** Não. A média pode esconder cauda lenta; no exemplo há uma chamada de 2000 ms.

**Como explicar:** Pergunta: O counter está em 500. Isso significa 500 requisições por segundo?
Resposta: Não. É um total acumulado. Para taxa, calcule variação por tempo e trate resets.

Pergunta: Uma chamada tem request_id no log. Já temos um trace distribuído completo?
Resposta: Não. Correlação local não substitui spans e propagação de contexto entre operações e serviços.

Pergunta: A média é 47 ms. Podemos afirmar que ninguém esperou dois segundos?
Resposta: Não. A média pode esconder cauda lenta; no exemplo há uma chamada de 2000 ms.

**Conclusão prática:** Diferencie o que foi observado, o que é hipótese e o que foi confirmado.

## E6.17 — SLI: definir exatamente o que será medido

Indicador de nível de serviço ligado a uma experiência do usuário

**População:** GET /visitas elegíveis. Janela declarada. Origem da observação identificada.

**Evento bom:** Status 200 e total inteiro válido. Falha de conexão também importa na visão do cliente.

**Indicador:** Chamadas boas / chamadas elegíveis. Reportar volume e resultado. Sem chamadas: sem amostra.

**Como explicar:** A sonda do laboratório verifica status e conteúdo; uma métrica do servidor baseada apenas em HTTP 200 não observa exatamente o mesmo contrato. Requisições que não chegam à API não aparecem em seu counter. Por isso declare o ponto de observação. Excluir healthchecks evita que chamadas automáticas verdes diluam a falha da operação de negócio. Zero tráfego não prova sucesso de 100%; é ausência de amostra para esse cálculo.

**Conclusão prática:** Um SLI é útil quando população, sucesso, janela e origem estão definidos.

## E6.18 — SLI calculado: explicação passo a passo

Exemplo fictício de uma janela já encerrada

| Dado | Cálculo / significado |
| --- | --- |
| Elegíveis | 1000 chamadas de GET /visitas. |
| Boas | 992 retornaram o contrato esperado. |
| Falhas | 1000 − 992 = 8 chamadas não boas. |
| SLI de sucesso | 992 / 1000 × 100 = 99,2%. |

**Como explicar:** Use números pequenos o suficiente para que todos acompanhem. As oito falhas podem incluir status de erro, corpo inválido ou falta de resposta, desde que a coleta do indicador consiga observar esses casos. Não misture consultas administrativas no denominador nem selecione somente os logs bem-sucedidos. A janela terminou; o cálculo não estima sozinho a disponibilidade de uma janela maior ou a experiência de outra população.

**Conclusão prática:** 99,2% descreve esta população nesta janela; não é uma promessa para todas as situações.

## E6.19 — SLI, SLO e SLA: medida, objetivo e compromisso

A meta deve fazer sentido para quem usa o serviço

| Termo | Significado | Exemplo didático |
| --- | --- | --- |
| SLI | Indicador observado. | 99,2% de chamadas boas na janela. |
| SLO | Objetivo para indicador e janela definidos. | Pelo menos 99% no período acordado. |
| SLA | Compromisso formal com condições próprias. | Nível acordado e consequências previstas. |

**Como explicar:** O SLO não nasce de copiar um número popular. Depende do impacto, da viabilidade e da política da equipe. SLA é um compromisso formal, que pode ter condições e consequências; a aula não está criando um contrato jurídico. Um relatório de dez sondas locais não prova cumprimento de um SLO mensal. A meta fictícia de 99% serve para explicar o cálculo e a decisão, não para impor um padrão universal ao projeto.

**Conclusão prática:** Medida observada, meta interna e compromisso formal são objetos diferentes.

## E6.20 — Error budget: quanto da tolerância já foi consumido

Mesmo exemplo: 1000 chamadas • SLO 99% • 8 falhas

**Como explicar:** No período encerrado, a tolerância de 1% de 1000 é dez chamadas. Oito falhas consumiram 80% desse orçamento; restaram duas, ou 20%. Se houver mais de dez falhas nessa população, a meta não foi atendida. Em uma janela viva, população e orçamento podem variar; este desenho não é um contador de falhas futuras autorizado indefinidamente. O efeito sobre releases depende de uma política acordada, não de punição automática. Priorizar correções pode reduzir o risco de continuar consumindo a tolerância.

**Conclusão prática:** Orçamento permitido: 10 • consumido: 8 • restante: 2; a política define como isso orienta decisões.

## E6.21 — Alertas: condição, impacto e ação

Exemplos ilustrativos; calibrar janela e volume para o serviço

| Alerta | Problema ou mérito | Melhoria / ação |
| --- | --- | --- |
| CPU > 80% em uma amostra | Pode não representar falha percebida. | Relacionar a saturação e impacto; observar duração. |
| Erros aumentaram na operação | Sinal próximo do resultado do usuário. | Definir janela, amostra mínima e destino. |
| Dependência indisponível | Contexto útil, mas pode duplicar alertas. | Agrupar por incidente e consultar runbook. |
| Sonda sem dados | Não é sucesso nem falha medida da aplicação. | Investigar a coleta e o acesso ao destino. |

**Como explicar:** Um alerta acionável diz o que mudou, em qual serviço, por quanto tempo e qual primeiro passo seguir. Nem toda métrica alta merece interromper alguém. Uma regra precisa tratar falta de dados, volume pequeno e ruído. Evite prometer que uma correlação automática elimina causas distintas. No laboratório a equipe observa a falha com comandos; não há envio automático de mensagens nem serviço de paging configurado.

**Conclusão prática:** Alerta é um convite a agir com contexto, não apenas uma cor vermelha no painel.

## E6.22 — Dashboard mínimo: quatro perguntas operacionais

Esboço didático • cada painel precisa de unidade, janela e contexto

**Como explicar:** Explique o que se espera aprender ao olhar cada quadro. Tráfego ajuda a perceber ausência ou mudança de demanda; erros mostram resultados ruins; latência descreve o tempo; saturação mostra pressão sobre recursos. Nenhum número está representando medição real nesta figura. Registre versão e período para comparar antes/depois de uma entrega. Uma visualização bonita com denominador errado continua induzindo uma decisão errada. No projeto pequeno, uma tabela de medições bem definida pode cumprir o objetivo didático.

**Conclusão prática:** Quatro sinais úteis: tráfego, erros, latência e saturação; associe-os à operação que importa.

## E6.23 — Verificação | Indicadores e decisões

Depois dos conceitos e exemplos • explique a evidência

**1. Situação:** Em 1000 chamadas, 992 boas e SLO 99%, quanto orçamento foi consumido?

**2. Situação:** Não houve chamadas. Podemos exibir 100% de sucesso?

**3. Situação:** 50 alertas por dia são ignorados. Basta desligar todos para resolver?

**Como explicar:** Peça respostas breves apoiadas nos exemplos anteriores. Revele o gabarito depois de ouvir justificativas. Se houver confusão, volte à figura ou ao cálculo pertinente. As verificações são formativas e de discussão em grupo, sem criar nota individual ou alterar os pesos oficiais.

**Conclusão prática:** O próximo slide traz as três respostas explicadas.

## E6.24 — Respostas comentadas | Indicadores e decisões

Gabarito • do conceito à decisão

**1. Resposta:** A tolerância é 10 falhas. Oito foram consumidas: 80% do orçamento, restando duas nesta população.

**2. Resposta:** Não. O denominador é zero: faltam observações. Indique ausência de amostra e confira a coleta.

**3. Resposta:** Não. Priorize sinais ligados a impacto, agrupe duplicados e defina ação, dono e janela de cada regra.

**Como explicar:** Pergunta: Em 1000 chamadas, 992 boas e SLO 99%, quanto orçamento foi consumido?
Resposta: A tolerância é 10 falhas. Oito foram consumidas: 80% do orçamento, restando duas nesta população.

Pergunta: Não houve chamadas. Podemos exibir 100% de sucesso?
Resposta: Não. O denominador é zero: faltam observações. Indique ausência de amostra e confira a coleta.

Pergunta: 50 alertas por dia são ignorados. Basta desligar todos para resolver?
Resposta: Não. Priorize sinais ligados a impacto, agrupe duplicados e defina ação, dono e janela de cada regra.

**Conclusão prática:** Diferencie o que foi observado, o que é hipótese e o que foi confirmado.

## E6.25 — Incidente: do impacto à recuperação e ao aprendizado

Sequência de resposta • algumas etapas ocorrem em paralelo

**Detectar:** Perceber o sintoma Delimitar o impacto

**Investigar:** Coletar evidências Testar hipóteses

**Recuperar:** Conter ou corrigir Validar a operação

**Aprender:** Registrar fatores Prevenir recorrência

**Como explicar:** Incidente é uma degradação que exige resposta coordenada, não toda mensagem error em um log. A prioridade pode ser mitigar o impacto antes de entender todos os fatores. Registre o que se sabe e o que ainda está em investigação. Coordenação e atualização das pessoas envolvidas podem ocorrer durante as etapas. No ensaio a falha é provocada em um projeto local de dados fictícios; a equipe não deve experimentar indisponibilidade em um serviço real sem contexto e autorização próprios.

**Conclusão prática:** Restaurar o serviço e explicar a causa são objetivos relacionados; um não substitui o outro.

## E6.26 — Linha do tempo: medir intervalos com definições

Exemplo fictício de um único incidente

**Como explicar:** No exemplo, o impacto começa às 10:00, é detectado às 10:02 e o serviço é restaurado às 10:07. Tempo até detectar: dois minutos; do início à restauração: sete; da detecção à restauração: cinco. Especifique qual intervalo você está reportando. MTTD e MTTR costumam designar médias sobre vários eventos e MTTR tem expansões diferentes. Não chame um único intervalo de média nem confunda recuperação do serviço com conclusão de toda ação preventiva.

**Conclusão prática:** Início → detecção: 2 min • início → restauração: 7 min • detecção → restauração: 5 min.

## E6.27 — Sintoma, hipótese e causa confirmada

Exemplo: GET /visitas retorna 503

| Etapa | O que dizer | Como sustentar |
| --- | --- | --- |
| Sintoma | A consulta falhou para o cliente. | Status e corpo da chamada. |
| Hipótese | A dependência está indisponível. | Verificar estado do db e códigos de erro. |
| Teste | Recuperar a dependência no ensaio. | Repetir a mesma operação. |
| Conclusão | A parada do banco causou a falha provocada. | Linha do tempo, estado e teste após recuperação. |

**Como explicar:** Uma hipótese não vira causa apenas por soar plausível ou ter sido gerada por IA. Use um teste que a diferencie de alternativas, como hostname errado, credencial ou schema ausente. No laboratório sabemos a intervenção feita e podemos observar sua reversão. Em produção, correlação temporal entre deploy e erro não prova por si só qual alteração foi responsável. Evite chamar todo problema de causa raiz única: fatores de detecção e resposta também podem ter contribuído.

**Conclusão prática:** Uma causa confirmada explica as evidências e o efeito da intervenção, não só repete o sintoma.

## E6.28 — Relatório sem culpa: transformar o incidente em melhoria

Contexto e decisões do sistema, sem procurar um culpado

**Descrever:** Impacto, início e recuperação. Evidências e linha do tempo. O que era conhecido em cada decisão.

**Explicar:** Causa técnica e fatores contribuintes. O que funcionou e o que atrasou. Limites da investigação.

**Melhorar:** Ação concreta, responsável e prazo. Como verificar a melhoria. Runbook, teste ou alerta atualizado.

**Como explicar:** Sem culpa não significa sem responsabilidade. Significa investigar condições e decisões com as informações disponíveis, sem reduzir a explicação a erro humano. Uma ação como prestar mais atenção não muda o sistema de forma verificável. Compare com adicionar um teste funcional ao processo de promoção, com responsável e evidência de execução. O relatório deve reconhecer o que não foi confirmado e não preencher lacunas com uma narrativa convincente inventada.

**Conclusão prática:** Uma boa prevenção tem mudança verificável, responsável e prazo; não apenas uma recomendação vaga.

## E6.29 — Demonstração: observar a mesma API em três momentos

Ambiente E6 separado dos projetos E4 e E5

**Antes:** Operação funciona Coletar referência

**Durante:** Parar somente db Observar 503 e logs

**Depois:** Retomar db Repetir teste e conferir dados

**Como explicar:** A API ganha logs estruturados e métricas, mas continua usando PostgreSQL e o contador conhecido. O compose usa outro nome de projeto e outra porta, evitando misturar dados dos encontros anteriores. A sonda executa um número finito de chamadas e mostra status, conteúdo válido e tempo no cliente. A instrumentação é didática e manual, não uma instalação de OpenTelemetry. Traces permanecem conceituais; não afirmaremos capturá-los neste ensaio.

**Conclusão prática:** A prova é a comparação da mesma operação antes, durante e após uma intervenção controlada.

## E6.30 — Preparar o laboratório de observabilidade

Bash/zsh • Docker/Compose e Python 3 • porta 18086 livre

**Arquivo completo:** Terminal na pasta do E6. Build cria a API instrumentada. O banco usa dados fictícios.

**Contratos:** /health/live: processo HTTP. /health/ready: consulta básica. /visitas: operação de negócio.

```
cd Práticas/encontro-6-observabilidade
docker compose config --quiet
docker compose up -d --build --wait
curl -fsS localhost:18086/version
python3 observar.py --amostras 10
```

**Como explicar:** Construa e teste antes da aula para antecipar downloads. Se outra cópia do projeto estiver ativa, escolha nome e porta exclusivos conforme o README. O script observar.py usa somente a biblioteca padrão do Python e não instala dependências. --wait aguarda os checks, mas não substitui a validação funcional. Guarde data, versão e nome do projeto para relacionar os resultados. Não execute comandos num diretório ou contexto que aponta para outro ambiente.

**Conclusão prática:** A preparação identifica destino e versão antes de provocar qualquer falha.

## E6.31 — 1. Capturar a referência e correlacionar uma chamada

Saídas reais variam: anote os valores observados

**Referência:** POST incrementa o contador. Anote o total N. Sonda deve ter 10 boas de 10.

**Correlação:** curl -i mostra X-Request-Id. Localize o ID no log da API. Compare status e rota.

```
curl -fsS -X POST localhost:18086/visitas
curl -i localhost:18086/visitas
python3 observar.py --amostras 10
docker compose logs --tail=40 app
curl -fsS localhost:18086/metrics
```

**Como explicar:** A requisição manual e a sonda são chamadas diferentes, cada uma com seu ID. O cabeçalho permite localizar exatamente uma resposta no log, não qualquer evento que ocorreu perto no tempo. O total depende de uso prévio do volume. Os tempos são medidos no ambiente atual e não devem ser substituídos pelos números ilustrativos dos slides. O arquivo de métrica acumula chamadas desde a partida e pode incluir leituras manuais além das dez sondas.

**Conclusão prática:** Mesmo período e mesma população são necessários para comparar números.

## E6.32 — 2. Provocar uma falha na dependência

Somente no projeto local do laboratório

**O que muda:** db fica parado. A API continua viva. A operação dependente falha.

**Resultado esperado:** /health/live: 200. /visitas: 503. Sonda: 0 boas de 5.

```
docker compose stop db
curl -i localhost:18086/health/live
curl -i localhost:18086/visitas
python3 observar.py --amostras 5 --esperado 503
docker compose ps -a
```

**Como explicar:** stop mantém o container e os dados; não remove o volume. Espere que as consultas falhem e colete os sinais. O retorno exato de erro do driver pode variar entre conexão encerrada e recusada conforme o momento; não exija uma única string para reconhecer a dependência indisponível. O argumento esperado=503 diz ao script para confirmar a falha induzida: exit code zero nesse modo não quer dizer serviço saudável. Interprete o resumo, que continua registrando chamadas não boas.

**Conclusão prática:** Processo vivo, healthcheck e função de negócio observam contratos diferentes.

## E6.33 — 3. Reunir evidência antes de decidir

Estado + evento + resultado funcional

**Estado:** ps -a mostra db parado. app pode estar Up e depois unhealthy.

**Evento e métrica:** Log associa 503, rota e ID. Counter de falhas aumenta. A janela da sonda mostra impacto.

```
docker compose ps -a
docker compose logs --since=5m --tail=80 app
curl -fsS localhost:18086/metrics
# No log: request_id, route, status, error_code
# Nas métricas: método, rota, status e duração
```

**Como explicar:** Identifique o último evento pertinente, pois o tail pode incluir sucessos anteriores e probes. Logs não contêm automaticamente toda a história: retenção e volume limitam o que está disponível. Métricas da API excluem as rotas de saúde e métricas; request_id não aparece como label. Leia a unidade do histograma: segundos, enquanto os logs e a sonda usam milissegundos. A hipótese banco parado é sustentada por estado e intervenção conhecida, não apenas por um número vermelho.

**Conclusão prática:** A soma dos sinais deve sustentar a hipótese; guarde também o contexto e os limites da coleta.

## E6.34 — 4. Recuperar e repetir o mesmo teste

O processo da API trata a indisponibilidade e aceita novas consultas

**Recuperar:** start db retoma o banco. Aguardar /health/ready. Não recriar app neste ensaio.

**Validar:** Sonda volta a 10 boas de 10. Contador permanece N. Novos logs têm status 200.

```
docker compose start db
python3 aguardar.py
# Se a espera falhar, investigar antes de seguir.
python3 observar.py --amostras 10
curl -fsS localhost:18086/visitas
docker compose logs --tail=30 app
```

**Como explicar:** O helper aguardar.py repete /health/ready com limite de tentativas; assim verifica a conexão a partir da API, inclusive a recuperação do pool. A prontidão não substitui o teste de /visitas. Se a espera falhar, investigar antes de iniciar a janela depois. Não use up --wait na stack toda só para recuperar o banco, pois pode alterar instâncias e confundir a comparação. O comportamento de recuperação depende do código desta API; não generalize para uma aplicação que encerra ao perder a dependência. Após retornar, registre também a ação preventiva.

**Conclusão prática:** Recuperação comprovada = operação restaurada + dados conferidos + evidência registrada.

## E6.35 — Antes, durante e depois: interpretar sem misturar janelas

Exemplo de resultados esperados • tempos reais vêm da execução

| Janela da sonda | Resultado | Conclusão |
| --- | --- | --- |
| Antes: 10 chamadas | 10 boas; 0 falhas. | Referência funcional observada. |
| Durante: 5 chamadas | 0 boas; 5 falhas. | Dependência indisponível afetou a operação. |
| Depois: 10 chamadas | 10 boas; 0 falhas. | Recuperação funcional observada. |
| Todo o ensaio: 25 | 20 / 25 = 80% boas. | Agregado mistura referência e falha deliberada. |

**Como explicar:** O agregado de 80% está matematicamente correto para as 25 sondas, mas descreve um experimento de falha, não uma disponibilidade mensal. Chamadas manuais e healthchecks não entram nesse denominador da sonda. Os contadores da API podem mostrar outro total, porque registram chamadas manuais de /visitas também. Um teste com falha induzida não deve ser usado para comparar equipes por desempenho. Ele serve para demonstrar detecção, explicação e recuperação.

**Conclusão prática:** Informe a janela e o propósito do ensaio; o mesmo conjunto de dados admite resumos com sentidos diferentes.

## E6.36 — Caso resolvido: HTTP 200, mas o usuário espera demais

Cenário ilustrativo; atraso opcional reproduzível no README

**Sintoma:** Sucesso por status continua alto. Duração da chamada aumenta. Usuário percebe lentidão.

**Evidência:** Compare cliente e servidor. Veja tempo da dependência. Confira configuração e versão.

**Causa no ensaio:** DEMO_DELAY_MS adiciona espera no código. Remover o atraso e repetir a sonda. Não atribuir automaticamente ao banco.

**Como explicar:** O atraso artificial é inserido no wrapper da consulta e aparece no campo dependency_ms. Esse campo mede a espera da aplicação ao redor da operação, não somente processamento SQL no servidor do banco. Por isso um tempo alto não prova banco lento. O exercício opcional recria app para aplicar a variável, o que zera contadores em memória. Compare novas janelas da sonda, sem subtrair counters de processos diferentes. Isso introduz a diferença entre sucesso e objetivo de latência.

**Conclusão prática:** Uma operação pode estar disponível e ainda falhar no objetivo de tempo; medir apenas status deixa essa falha invisível.

## E6.37 — Verificação | Confirmar a recuperação

Depois dos conceitos e exemplos • explique a evidência

**1. Situação:** A sonda recebeu 503, mas app está Up. Há contradição?

**2. Situação:** Após recuperar, o counter de falhas continua em 5. O serviço ainda está falhando?

**3. Situação:** dependency_ms alto prova que o servidor do banco está lento?

**Como explicar:** Peça respostas breves apoiadas nos exemplos anteriores. Revele o gabarito depois de ouvir justificativas. Se houver confusão, volte à figura ou ao cálculo pertinente. As verificações são formativas e de discussão em grupo, sem criar nota individual ou alterar os pesos oficiais.

**Conclusão prática:** O próximo slide traz as três respostas explicadas.

## E6.38 — Respostas comentadas | Confirmar a recuperação

Gabarito • do conceito à decisão

**1. Resposta:** Não. O processo da API segue vivo enquanto a operação que usa db pode estar indisponível.

**2. Resposta:** Não necessariamente. Counter acumula história. Observe a variação na nova janela e repita a operação.

**3. Resposta:** Não. Inclui a espera medida pelo cliente da dependência; no ensaio opcional há atraso artificial no código.

**Como explicar:** Pergunta: A sonda recebeu 503, mas app está Up. Há contradição?
Resposta: Não. O processo da API segue vivo enquanto a operação que usa db pode estar indisponível.

Pergunta: Após recuperar, o counter de falhas continua em 5. O serviço ainda está falhando?
Resposta: Não necessariamente. Counter acumula história. Observe a variação na nova janela e repita a operação.

Pergunta: dependency_ms alto prova que o servidor do banco está lento?
Resposta: Não. Inclui a espera medida pelo cliente da dependência; no ensaio opcional há atraso artificial no código.

**Conclusão prática:** Diferencie o que foi observado, o que é hipótese e o que foi confirmado.

## E6.39 — IA na investigação: propor, confrontar e registrar

Retomar a governança do encontro 5

**Entrada útil:** Sintoma, janela e versão. Logs mínimos sem segredos. O que já foi testado.

**Saída esperada:** Hipóteses com evidência. Teste que possa refutá-las. Limitações e próximo passo.

**Decisão humana:** Revisar comandos e impacto. Executar teste controlado. Registrar resultado e divergências.

**Como explicar:** A IA pode organizar um conjunto de eventos e sugerir hipóteses, mas uma explicação plausível não prova causalidade. Peça que diferencie fatos fornecidos de inferências. O aluno deve conseguir explicar por que aceitou ou rejeitou uma sugestão. Não enviar credenciais, dados pessoais ou dumps completos. Quando não houver autorização para usar um serviço externo, use dados sintéticos e faça a revisão em sala.

**Conclusão prática:** A evidência vem do sistema e do teste; a resposta da IA é uma contribuição a revisar.

## E6.40 — Exemplo de prompt com critérios verificáveis

Dados sintéticos • copiar e adaptar ao contexto autorizado

**Peça vínculo:** Cada hipótese deve citar um fato. Se faltar dado, declarar a lacuna.

**Peça um teste:** Indicar o resultado esperado. Definir o que refutaria a hipótese.

```
Contexto: laboratório local, API versão 3.0.0.
Fatos: /health/live=200; /visitas=503; db está parado.
Mudança conhecida: executei compose stop db.
Não há evidência de perda de dados.
Separe fatos e hipóteses. Para cada hipótese:
- cite o fato que a sustenta;
- proponha um teste e como refutá-la;
- explique riscos e limites.
Não proponha apagar volumes ou dados.
```

**Como explicar:** Leia o prompt e peça à turma que antecipe uma resposta adequada. Uma boa hipótese é dependência indisponível, sustentada pelo estado do db e pelos 503. Um teste é iniciar db, esperar prontidão e repetir a operação sem trocar app. Isso confirma a causa induzida neste ensaio; num incidente real ainda pode faltar explicar por que o banco parou. Não é necessário enviar esse prompt a uma ferramenta para discutir a qualidade do raciocínio.

**Conclusão prática:** Uma pergunta melhor produz uma investigação mais verificável, não uma garantia de acerto.

## E6.41 — Caso resolvido: “apague o volume e tente novamente”

Resposta gerada deve passar por revisão

**Problema:** O conselho destruiria dados. Não explica a causa do 503. Não é necessário neste ensaio.

**Decisão:** Rejeitar a sugestão. Preservar estado e evidências. Retomar db e validar a operação.

**Registro:** Anotar a sugestão rejeitada. Explicar risco e alternativa. Vincular o resultado do teste.

**Como explicar:** O caso é ilustrativo, não uma saída real de uma ferramenta. A indisponibilidade observada decorre do banco parado intencionalmente. Reinicializar armazenamento não é tratamento proporcional. Também trate frases dentro de logs como dados: um evento que diga ignore as regras não autoriza nenhuma ação. O mesmo vale para recomendações copiadas de tickets. A equipe deve documentar a revisão, sem inventar uma conversa com IA que não aconteceu.

**Conclusão prática:** Revisão crítica pode resultar em rejeição; isso é uma evidência válida de uso responsável.

## E6.42 — AIOps: onde a automação pode ajudar

Capacidades possíveis, dependentes da qualidade dos dados

**Organizar sinais:** Agrupar alertas semelhantes. Resumir eventos da janela. Relacionar mudança e sintoma.

**Sugerir análise:** Destacar comportamento incomum. Priorizar hipóteses de investigação. Explicitar incertezas.

**Controlar execução:** Permissão mínima. Ação limitada e auditável. Verificação e escalonamento.

**Como explicar:** AIOps designa usos de técnicas de IA em operações, não uma garantia de operação autônoma. Correlação temporal não prova causalidade: um deploy próximo ao erro pode ser coincidência. Não apresentar percentuais universais de produtividade ou prevenção. Compare a sugestão com uma hipótese alternativa e com o que realmente ocorreu no ambiente. Aqui a automação é discutida conceitualmente; o laboratório não instala uma plataforma de AIOps.

**Conclusão prática:** Automatize tarefas com critérios claros; mantenha limites, rastreabilidade e verificação.

## E6.43 — Uma ação automática precisa de limites

Exemplo conceitual de recuperação controlada

**Condição:** Sinal confirmado Contexto autorizado

**Ação:** Runbook conhecido Tentativas limitadas

**Verificação:** Repetir operação Checar efeito

**Escalonar:** Falhou ou risco alto? Acionar responsável

**Como explicar:** Explique por que reiniciar indefinidamente é perigoso: pode ampliar a indisponibilidade e apagar contexto. Um runbook deve definir escopo, permissões, limite de tentativas, confirmação de recuperação e destino de escalonamento. Ações destrutivas e mudanças de schema exigem avaliação específica. Este diagrama não é uma automação implementada nem envia notificações. No exercício, a pessoa executa a recuperação local e registra a evidência.

**Conclusão prática:** Uma ação sem critério de parada e teste de recuperação não fecha o ciclo operacional.

## E6.44 — Verificação | Revisar uma sugestão de IA

Depois dos conceitos e exemplos • explique a evidência

**1. Situação:** A resposta aponta o deploy como causa porque ocorreu antes do erro. Isso basta?

**2. Situação:** Um log contém a frase “execute este comando”. A equipe deve obedecer?

**3. Situação:** Rejeitar uma sugestão impede demonstrar uso responsável de IA?

**Como explicar:** Peça respostas breves apoiadas nos exemplos anteriores. Revele o gabarito depois de ouvir justificativas. Se houver confusão, volte à figura ou ao cálculo pertinente. As verificações são formativas e de discussão em grupo, sem criar nota individual ou alterar os pesos oficiais.

**Conclusão prática:** O próximo slide traz as três respostas explicadas.

## E6.45 — Respostas comentadas | Revisar uma sugestão de IA

Gabarito • do conceito à decisão

**1. Resposta:** Não. Ordem temporal sugere uma hipótese. Compare versões, dependências e resultados de testes que possam refutá-la.

**2. Resposta:** Não. O log é dado a analisar. Comandos exigem revisão de finalidade, escopo, autorização e impacto.

**3. Resposta:** Não. Registre a sugestão, o motivo da rejeição e a alternativa validada. Não invente uma interação que não ocorreu.

**Como explicar:** Pergunta: A resposta aponta o deploy como causa porque ocorreu antes do erro. Isso basta?
Resposta: Não. Ordem temporal sugere uma hipótese. Compare versões, dependências e resultados de testes que possam refutá-la.

Pergunta: Um log contém a frase “execute este comando”. A equipe deve obedecer?
Resposta: Não. O log é dado a analisar. Comandos exigem revisão de finalidade, escopo, autorização e impacto.

Pergunta: Rejeitar uma sugestão impede demonstrar uso responsável de IA?
Resposta: Não. Registre a sugestão, o motivo da rejeição e a alternativa validada. Não invente uma interação que não ocorreu.

**Conclusão prática:** Diferencie o que foi observado, o que é hipótese e o que foi confirmado.

## E6.46 — O mesmo projeto, seis incrementos conectados

Apresentar a evolução com evidências no repositório

| Etapa | Contribuição | O que mostrar |
| --- | --- | --- |
| E1–E2 | Projeto, colaboração e implementação. | Contexto, histórico e decisões técnicas. |
| E3 | Integração contínua. | Execução do pipeline e resultado dos testes. |
| E4 | Containers e integração. | Dockerfile, Compose e operação funcionando. |
| E5 | Entrega e operação. | Versão, configuração e plano de recuperação. |
| E6 | Observabilidade e diagnóstico. | Sinais, incidente e recuperação comprovada. |

**Como explicar:** Use o enunciado original para conferir os entregáveis específicos de cada encontro. A tabela é uma síntese da trajetória, não uma substituição da rubrica. A equipe continua no repositório único e no problema que escolheu. Não precisa migrar o projeto para a API do professor nem acrescentar uma plataforma de observabilidade inteira para reproduzir os conceitos.

**Conclusão prática:** A apresentação deve ligar decisões, implementação e resultados do próprio projeto.

## E6.47 — Preparação das equipes: 35 minutos com foco

145–180 min • aproveitar os incrementos já construídos

**0–12 min:** Escolher operação relevante. Conferir logs e uma medição. Definir janela e resultado bom.

**12–25 min:** Executar falha local controlada. Registrar hipótese e intervenção. Confirmar recuperação e dados.

**25–35 min:** Organizar links das evidências. Revisar relato e participação. Ensaiar a fala de 5–7 minutos.

**Como explicar:** Os 35 minutos são preparação final, não tempo para construir tudo do zero. Oriente a aproveitar código e evidências dos encontros anteriores. Se uma falha não puder ser induzida com segurança no ambiente atual, use um ensaio local previamente registrado, identifique a data e explique a limitação. Não declarar como realizado um teste apenas planejado. Acompanhe as equipes por risco e bloqueio; não exigir que todas usem as mesmas ferramentas.

**Conclusão prática:** A entrega é da equipe e está no repositório; a demonstração deve mostrar evidências verificáveis.

## E6.48 — Exemplo preenchido de relato de incidente

Exemplo didático • horários ilustrativos, não resultados medidos

| Campo | Preenchimento |
| --- | --- |
| Impacto e janela | 10:00–10:07: consulta /visitas indisponível no ensaio local. |
| Evidências | 5 sondas retornaram 503; db parado; logs ligados por request_id. |
| Causa do ensaio | Banco interrompido pelo comando deliberado compose stop db. |
| Recuperação | start db; prontidão confirmada; 10 sondas boas; contador preservado. |
| Ação e responsável | Equipe: adicionar teste de dependência ao runbook antes da entrega. |

**Como explicar:** Diferencie o gatilho controlado da causa que seria investigada em produção. Se o banco tivesse parado inesperadamente, seria necessário descobrir a razão: recurso, operação humana, configuração ou outro evento. O relatório pode dizer causa ainda não confirmada quando essa for a verdade. Cada evidência deve ganhar caminho ou link real no repositório. Os horários aqui servem para ensinar a estrutura; substitua pelos da execução da equipe.

**Conclusão prática:** Um relato útil permite reconstruir o raciocínio sem depender da memória de quem apresentou.

## E6.49 — Rubrica oficial: construção e integração

70% da avaliação • pesos preservados

| Critério | Peso | Evidência que ajuda a explicar |
| --- | --- | --- |
| Projeto | 25% | Problema, solução implementada e decisões do grupo. |
| CI | 25% | Pipeline executado, testes e tratamento de falhas. |
| Containers | 20% | Empacotamento, integração e execução reproduzível. |

**Como explicar:** Os três pesos somam 70%. Consulte a rubrica original para os descritores completos. O slide organiza evidências sem criar novos critérios ou avaliação individual. A apresentação curta não deve ocultar os entregáveis técnicos: deixe links diretos para o avaliador consultar.

**Conclusão prática:** Mostre o que foi implementado e executado; uma configuração isolada não comprova seu resultado.

## E6.50 — Rubrica oficial: entregar, diagnosticar e comunicar

30% da avaliação • total geral: 100%

| Critério | Peso | Evidência que ajuda a explicar |
| --- | --- | --- |
| Entrega e operação | 15% | Versão, configuração, execução e recuperação planejada. |
| Diagnóstico | 10% | Sintoma, hipótese, teste, causa e recuperação comprovada. |
| Apresentação | 5% | Narrativa clara de 5–7 min com evidências do grupo. |

**Como explicar:** Logs e métricas sustentam tanto a operação quanto o diagnóstico; não são um peso adicional. A avaliação permanece em grupo, conforme o enunciado. Não criar uma arguição com nota individual. Explique que mostrar o erro deliberado é positivo quando acompanhado por método, interpretação e recuperação. O resultado final não depende de esconder limitações.

**Conclusão prática:** Os pesos continuam 25 / 25 / 20 / 15 / 10 / 5; observabilidade conecta as evidências.

## E6.51 — Roteiro de apresentação: exemplo de seis minutos

Dentro do intervalo oficial de 5–7 minutos por equipe

**0–2 min:** 0–1: problema e solução. 1–2: CI e teste executado. Use links já abertos.

**2–4 min:** 2–3: containers e integração. 3–4: entrega e recuperação. Mostre versão e configuração.

**4–6 min:** 4–5: incidente e evidências. 5–6: decisões, IA e limites. Concluir com aprendizado.

**Como explicar:** É um roteiro sugerido, não seis novos itens de nota. Distribua a participação de acordo com o trabalho do grupo. Não consuma toda a fala aguardando build ou download: tenha evidências previamente produzidas e identifique quando usar gravação ou captura. Uma operação curta ao vivo pode apoiar a explicação. Cada slot de oito minutos inclui fala de cinco a sete e transição ou feedback; respeitar o relógio protege as demais equipes.

**Conclusão prática:** Selecione uma narrativa demonstrável: o problema, a entrega, a falha e o que a equipe aprendeu.

## E6.52 — Organizar evidências para quem não acompanhou a aula

Modelo de índice no README do repositório da equipe

**Caminhos reais:** Trocar exemplos pelos arquivos do grupo. Preferir links diretos e datas.

**Contexto mínimo:** Comando, versão, janela e resultado. Captura sem contexto é ambígua.

```
README.md
docs/arquitetura.md
docs/entrega-e-recuperacao.md
docs/incidente.md
docs/uso-de-ia.md
evidencias/ci/
evidencias/containers/
evidencias/antes.jsonl
evidencias/durante.jsonl
evidencias/depois.jsonl
```

**Como explicar:** O índice reduz o tempo gasto procurando arquivos durante a apresentação e a avaliação. Não versionar segredos ou logs contendo dados pessoais. Saídas de teste devem indicar a versão e a data. No registro de IA, distinguir sugestão, revisão e teste. Se a equipe não executou uma etapa, registrar como pendente em vez de inventar um resultado. Os nomes exibidos são apenas uma organização possível.

**Conclusão prática:** A evidência deve ser localizável e interpretável, não apenas existir em uma pasta.

## E6.53 — Verificação | Defender as evidências do projeto

Depois dos conceitos e exemplos • explique a evidência

**1. Situação:** O grupo mostra apenas um dashboard verde. O diagnóstico está demonstrado?

**2. Situação:** Uma captura foi feita ontem. Pode entrar na apresentação?

**3. Situação:** O contador de falhas acumulado é diferente do total da sonda. Há necessariamente erro?

**Como explicar:** Peça respostas breves apoiadas nos exemplos anteriores. Revele o gabarito depois de ouvir justificativas. Se houver confusão, volte à figura ou ao cálculo pertinente. As verificações são formativas e de discussão em grupo, sem criar nota individual ou alterar os pesos oficiais.

**Conclusão prática:** O próximo slide traz as três respostas explicadas.

## E6.54 — Respostas comentadas | Defender as evidências do projeto

Gabarito • do conceito à decisão

**1. Resposta:** Não. Explique operação, janela, sintoma, hipótese, teste, causa sustentada e recuperação. O painel é uma parte da evidência.

**2. Resposta:** Sim, se identificada como registro anterior, com data, versão e contexto. Não a apresentar como execução ao vivo.

**3. Resposta:** Não. Podem ter janelas e populações diferentes. A API inclui chamadas manuais; a sonda conta somente suas chamadas.

**Como explicar:** Pergunta: O grupo mostra apenas um dashboard verde. O diagnóstico está demonstrado?
Resposta: Não. Explique operação, janela, sintoma, hipótese, teste, causa sustentada e recuperação. O painel é uma parte da evidência.

Pergunta: Uma captura foi feita ontem. Pode entrar na apresentação?
Resposta: Sim, se identificada como registro anterior, com data, versão e contexto. Não a apresentar como execução ao vivo.

Pergunta: O contador de falhas acumulado é diferente do total da sonda. Há necessariamente erro?
Resposta: Não. Podem ter janelas e populações diferentes. A API inclui chamadas manuais; a sonda conta somente suas chamadas.

**Conclusão prática:** Diferencie o que foi observado, o que é hipótese e o que foi confirmado.

## E6.55 — Fechamento: explicar o ciclo completo

Do problema ao aprendizado operacional

**Construir e integrar:** Mudanças rastreáveis. Testes e pipeline. Execução em containers.

**Entregar e observar:** Configuração e versão. Sinais com significado. Objetivos e recuperação.

**Aprender e comunicar:** Causa sustentada por evidência. Ação de melhoria com responsável. Repositório e apresentação final.

**Como explicar:** Nos quatro minutos finais, confira os links e a submissão no prazo estabelecido: até o fim do encontro 6. Retome uma decisão que cada equipe agora consegue explicar melhor. Os próximos slides são consulta e não precisam ser expostos antes das apresentações. O fechamento não cria outra entrega. Reforce o percurso do mesmo projeto e o uso crítico de automação e IA.

**Conclusão prática:** DevOps conecta colaboração, entrega e feedback; o projeto final deve tornar essa conexão visível.

## E6.56 — Consulta | Request ID não é tracing distribuído

Como evoluir a instrumentação depois do laboratório

**Correlação local:** Um ID liga resposta e log. Ajuda a buscar uma requisição. Não cria spans automaticamente.

**Trace distribuído:** Contexto propagado entre serviços. Spans com início, fim e relação. Instrumentação e exportação.

**Decisões:** Escolher pontos de coleta. Controlar dados e amostragem. Verificar custo e utilidade.

**Como explicar:** O laboratório usa somente request_id local; o diagrama de trace é conceitual. Para evoluir, a equipe pode estudar OpenTelemetry, contexto de trace e um backend adequado. A instrumentação precisa propagar contexto pelas chamadas relevantes. Amostragem reduz volume e pode deixar uma requisição fora do conjunto armazenado. Não prometer que todo evento estará disponível nem exigir essa evolução na entrega atual.

**Conclusão prática:** Adote tracing quando a pergunta exigir relações entre operações; não apenas para acrescentar uma ferramenta.

## E6.57 — Consulta | O custo de colocar tudo em labels

Métricas agregadas e eventos detalhados precisam de escolhas diferentes

**Labels úteis:** Método normalizado. Rota conhecida. Status HTTP.

**Evitar sem controle:** request_id único. URL com parâmetros livres. Identidade de cada usuário.

**Por quê?:** Cada combinação cria uma série. Mais séries elevam custo. Detalhes cabem em logs revisados.

**Como explicar:** Na API, as rotas desconhecidas são normalizadas e não entram nas métricas de /visitas. O ID aparece nos logs e no cabeçalho, não nas labels. A cardinalidade depende das combinações possíveis; se cada chamada ganha um valor novo, o conjunto cresce continuamente. Também definir retenção e acesso aos logs. Essa é uma escolha de projeto, não simplesmente remover dados sem compreender a pergunta de investigação.

**Conclusão prática:** Colete o contexto necessário no lugar apropriado e limite dimensões sem controle.

## E6.58 — Consulta | Ler os buckets de um histograma

No laboratório: duração no servidor em segundos; buckets cumulativos

**Exemplo didático:** le="0.1": 8 chamadas. le="0.3": 10 chamadas. 8 já estão contidas nas 10.

**Interpretação:** 2 chamadas entre 0,1 e 0,3 s. Não somar todos os buckets. +Inf deve igualar _count.

**Limitação:** Faixas não guardam cada duração. Percentis são estimados. A sonda tem amostras do cliente.

**Como explicar:** O histograma do servidor cobre GET /visitas, incluindo respostas de erro, e exclui as rotas de saúde e métricas. Os números deste slide são ilustrativos. _sum dividido por _count fornece a média das observações acumuladas quando count é positivo; não fornece p95. A sonda calcula nearest-rank sobre durações individuais do cliente. Medições em locais diferentes não precisam coincidir. Reiniciar app zera todas as métricas locais.

**Conclusão prática:** Unidade, população, janela e reinício precisam acompanhar qualquer cálculo.

## E6.59 — Consulta | Reproduzir a lentidão controlada

Opcional • executar somente no laboratório local

**Comparar:** Nova janela: status e p95. DEMO_DELAY_MS adiciona espera. Não é falha real do PostgreSQL.

**Restaurar:** Voltar a zero e repetir a sonda. A recriação zera métricas locais. O volume do banco permanece.

```
DEMO_DELAY_MS=400 docker compose up -d \
  --no-deps --force-recreate --wait app
python3 observar.py --amostras 10
curl -fsS localhost:18086/version
DEMO_DELAY_MS=0 docker compose up -d \
  --no-deps --force-recreate --wait app
python3 observar.py --amostras 10
```

**Como explicar:** Os comandos usam atribuição temporária de variável no shell, válida em Linux, macOS e WSL. O delay é aplicado ao wrapper da consulta e pode afetar a prontidão, mas 400 ms fica abaixo do timeout configurado. --no-deps recria apenas app. O teste demonstra que sucesso por status pode coexistir com latência ruim. O README oferece a sequência e exige confirmar a prontidão após a recriação. Não comparar counters antes e depois como se fossem do mesmo processo.

**Conclusão prática:** A mesma operação precisa atender ao resultado esperado e ao objetivo de tempo definido.

## Referências

- [OpenTelemetry: sinais](https://opentelemetry.io/docs/concepts/signals/)
- [OpenTelemetry: observabilidade](https://opentelemetry.io/docs/concepts/observability-primer/)
- [OpenTelemetry: traces](https://opentelemetry.io/docs/concepts/signals/traces/)
- [Prometheus: tipos de métricas](https://prometheus.io/docs/concepts/metric_types/)
- [Prometheus: histogramas](https://prometheus.io/docs/practices/histograms/)
- [Prometheus: nomes e labels](https://prometheus.io/docs/practices/naming/)
- [Google SRE: monitoramento](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Google SRE: implementação de SLOs](https://sre.google/workbook/implementing-slos/)
- [Google SRE: orçamento de erro](https://sre.google/workbook/error-budget-policy/)
- [Google SRE: alertas baseados em SLO](https://sre.google/workbook/alerting-on-slos/)
- [Google SRE: post-mortem](https://sre.google/sre-book/postmortem-culture/)
- [Docker Compose: serviços](https://docs.docker.com/reference/compose-file/services/)
- [OWASP: prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
