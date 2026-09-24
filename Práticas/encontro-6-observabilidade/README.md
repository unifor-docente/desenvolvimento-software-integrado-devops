# Encontro 6 — observar, investigar e recuperar

Demonstração do professor e referência para adaptação ao **mesmo projeto da equipe**. A API retoma o contador dos encontros anteriores, agora com logs JSON, request ID e métricas em memória. Não exige Prometheus, Grafana ou OpenTelemetry instalados: o endpoint `/metrics` expõe texto compatível com Prometheus; o tracing dos slides é conceitual.

## Pré-requisitos e início

Docker Engine/Desktop com Compose V2 (`docker compose`), Python 3 e curl; comandos em Linux/macOS/WSL. Porta local 18086 livre. Execute na raiz do repositório:

```sh
cd Práticas/encontro-6-observabilidade
docker compose config --quiet
docker compose up -d --build --wait
curl -fsS localhost:18086/version
mkdir -p evidencias
```

O primeiro build precisa baixar imagens e pacotes. As credenciais `aula` são públicas e fictícias, exclusivas deste ambiente local. A porta da API é publicada apenas em 127.0.0.1. O banco não publica porta no host. `PORTA_HOST=18087 docker compose up -d --build --wait` permite mudar a porta; nesse caso, ajuste todos os curls e use `--base http://localhost:18087` na sonda. Conserve a mesma configuração nas próximas operações.

## 1. Registrar a referência

```sh
curl -fsS -X POST localhost:18086/visitas
curl -i localhost:18086/visitas
python3 observar.py --amostras 10 > evidencias/antes.jsonl
cat evidencias/antes.jsonl
docker compose logs --no-color --tail=60 app > evidencias/logs-antes.txt
curl -fsS localhost:18086/metrics > evidencias/metricas-antes.txt
```

Anote o valor **N** de `total`; GET apenas lê, POST incrementa. Registre data, versão e comando no relato. Cada resposta traz `X-Request-Id`: procure o mesmo valor no log JSON. Cada chamada tem um ID diferente. O campo `request_id` não é um trace distribuído.

A última linha da sonda traz amostras, boas, falhas, sucesso e p95. Boa = HTTP 200 com `total` inteiro no corpo; o teste comprova esse contrato mínimo, não toda a correção do negócio. Resultado esperado nesta janela: **10 boas de 10**. O script retorna código 1 se o resultado divergir. A redireção preserva o código do script; confira-o antes de executar outro comando (`echo $?`).

## 2. Induzir a falha local

```sh
docker compose stop db
curl -i localhost:18086/health/live
curl -i localhost:18086/visitas
python3 observar.py --amostras 5 --esperado 503 > evidencias/durante.jsonl
cat evidencias/durante.jsonl
docker compose ps -a > evidencias/estado-durante.txt
docker compose logs --no-color --since=5m --tail=100 app > evidencias/logs-durante.txt
curl -fsS localhost:18086/metrics > evidencias/metricas-durante.txt
```

Esperado: processo vivo (`/health/live` 200), operação indisponível (`/visitas` 503), **0 boas de 5** na sonda. `--esperado 503` confirma a falha deliberada: código de saída zero nesse modo NÃO significa serviço saudável. O healthcheck do Compose usa `/health/ready`; pode levar alguns ciclos até marcar unhealthy. Não confundir estado do processo com resultado da operação.

Hipótese sustentada: o banco foi parado pela intervenção conhecida. Evidências: estado de db, 503 e logs. Código do erro do driver pode variar. Em um incidente não provocado, ainda seria necessário investigar por que o banco parou.

## 3. Recuperar e validar

```sh
docker compose start db
python3 aguardar.py
python3 observar.py --amostras 10 > evidencias/depois.jsonl
cat evidencias/depois.jsonl
curl -fsS localhost:18086/visitas
docker compose logs --no-color --tail=60 app > evidencias/logs-depois.txt
curl -fsS localhost:18086/metrics > evidencias/metricas-depois.txt
```

O helper tenta `/health/ready` até 30 vezes, com timeout de quatro segundos por chamada e intervalo de um segundo. Se a espera falhar, pare a sequência e investigue. Com porta alternativa, passe `--base` também ao helper. Esperado: **10 boas de 10** e `total` ainda N. O ensaio não recria app nem remove dados. A prontidão do banco não substitui a validação funcional. Registre ação preventiva, responsável e critério de verificação em [RELATO-INCIDENTE.md](RELATO-INCIDENTE.md).

## Como interpretar os números

- Sonda: chamadas seriais, não teste de carga. Tempo do cliente inclui rede e leitura; p95 por nearest-rank: ordenar e selecionar a posição `ceil(0,95 × N)`. Com 10 amostras, é o maior valor; não caracteriza comportamento de produção.
- Servidor: `duration_ms` mede recebimento até preparo da resposta, não entrega pela rede. `dependency_ms` mede espera em torno da consulta, incluindo o atraso artificial opcional; não prova tempo de execução SQL.
- `aula_http_requests_total`: respostas de `/visitas`, por método, rota e status. Inclui chamadas manuais GET/POST; exclui probes de saúde e coleta de métricas.
- Histograma `aula_http_request_duration_seconds`: GET `/visitas`, incluindo erros, em segundos. Buckets cumulativos: não somar. `+Inf` = `_count`; `_sum / _count` é média quando count > 0, não p95.
- Métricas ficam na memória e zeram ao reiniciar/recriar app. Sem coletor externo, não há série histórica persistida. Um counter de falhas que continua em 5 após recuperar não significa cinco novas falhas.
- As três sondas produzem 20 boas em 25 = 80%; descrevem este experimento com falha induzida, não disponibilidade mensal. Métricas da API podem ter outro total por incluir curls manuais.
- IDs e URLs arbitrárias não viram labels. Logs não registram query strings, tokens, payload ou DATABASE_URL. Revise qualquer evidência antes de publicar e não adicione dados reais sensíveis.

## Opcional: sucesso com lentidão

```sh
DEMO_DELAY_MS=400 docker compose up -d --no-deps --force-recreate --wait app
python3 observar.py --amostras 10
curl -fsS localhost:18086/version
DEMO_DELAY_MS=0 docker compose up -d --no-deps --force-recreate --wait app
python3 observar.py --amostras 10
```

Cada variável vale para aquele comando. A API acrescenta 400 ms ao wrapper de consulta. Espera-se status 200, mas latência maior; não é PostgreSQL realmente lento. A recriação zera métricas, então compare **novas janelas da sonda**. O banco e seus dados permanecem. Não existe limite de latência universal: a equipe define o objetivo e justifica-o.

## Encerramento

```sh
docker compose down
```

Remove containers e rede deste projeto; preserva o volume `dados`. O contador pode manter valor de execuções anteriores. Não usar remoção de volumes para tratar esta falha.

## Adaptação ao projeto final

Escolher uma operação relevante, definir contrato e janela, emitir sinais úteis, induzir uma falha controlada em ambiente local e validar recuperação. Não é obrigatório copiar esta API nem instalar todas as ferramentas citadas. Entregar evidências no repositório único da equipe até o fim do E6. Ver [roteiro da apresentação](APRESENTACAO.md) e [relato do incidente](RELATO-INCIDENTE.md).
