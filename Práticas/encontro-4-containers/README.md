# Encontro 4 — Laboratório de containers e integração

Exemplo demonstrativo para a disciplina Desenvolvimento de Software Integrado — DevOps, UNIFOR, 24/09/2026. As equipes aplicam os conceitos **ao próprio projeto integrador**; esta API não substitui a aplicação escolhida.

Antes deste laboratório, use [Primeiros passos](PRIMEIROS-PASSOS.md) para observar runtime, processo, portas, inspeção e ciclo de vida sem banco de dados.

## Objetivo e preparação

Observar uma API Node.js integrada a PostgreSQL, distinguir portas internas e publicadas, comprovar persistência e investigar falhas. No roteiro de 4h, a integração ocupa 35 minutos e o diagnóstico guiado 20 minutos, combinando explicação e execução. O trabalho das equipes tem 70 minutos no roteiro de 4h.

Pré-requisitos: Docker Engine ou Docker Desktop em execução, plugin `docker compose`, porta local 8080 disponível, acesso aos registries para baixar imagens e dependências e um terminal. Os comandos abaixo usam Bash/zsh. No PowerShell, prefira `curl.exe` aos exemplos com `curl` e adapte a continuação de linha. Não é necessário instalar Node ou PostgreSQL no host.

Abra o terminal nesta pasta. Antes da aula, execute a subida e os testes para baixar as dependências; conexão e tempo de build variam. As imagens usam tags legíveis, que podem mudar: para uma turma com ambiente rigidamente controlado, registre os digests efetivamente utilizados e teste novamente após atualizações.

```sh
cd 'Práticas/encontro-4-containers'
docker version
docker compose version
docker compose config --quiet
docker compose up -d --build --wait
```

Se já estiver nesta pasta, não repita o `cd`. O nome de projeto é `unifor-encontro4`. Se existir outra cópia em execução, pare-a ou use um nome de projeto e porta próprios; projetos com o mesmo nome compartilham recursos. `--wait` aguarda os checks; se o comando falhar, investigue `ps -a` e `logs` antes de continuar.

## Arquitetura e arquivos

```text
Host / cliente                  Rede padrão do Compose
localhost:8080 ── publicação ──> app:3000 ── SQL ──> db:5432
                                Node.js              PostgreSQL 16
                                                     │
                                                     └── volume dados
```

A API escuta em `0.0.0.0:3000` **dentro do container**. A publicação `127.0.0.1:8080:3000` permite acesso apenas local no host. O banco não publica porta no host. `db` é resolvido pelo DNS da rede compartilhada; `localhost` dentro da API significa a própria API.

| Arquivo | Papel na demonstração |
|---|---|
| `Dockerfile` | Imagem Node, instalação pelo lockfile, usuário sem root e processo principal |
| `package-lock.json` | Versões e integridade das dependências npm |
| `.dockerignore` | Exclui dependências locais, histórico Git, arquivos de ambiente e logs do contexto |
| `compose.yaml` | Dois serviços, publicação de porta, conexão, health checks e volume |
| `server.js` | Rotas HTTP, consultas e tratamento de indisponibilidade |
| `init.sql` | Cria tabela e contador na primeira inicialização de um volume vazio |

As credenciais `aula/aula` são **públicas e fictícias**, somente para esta demonstração local. A imagem oficial inicializa o banco com o usuário configurado; essa conta simplificada não representa uma política de privilégios de produção. Em um projeto real, adote credenciais externas, usuário da aplicação com permissões necessárias, migrações, autenticação e backup. Não envie configurações reais nem segredos a ferramentas de IA.

## 1. Comprovar funcionamento

```sh
docker compose ps
curl -fsS http://localhost:8080/health/live
curl -fsS http://localhost:8080/health/ready
curl -fsS -X POST http://localhost:8080/visitas
curl -fsS http://localhost:8080/visitas
docker compose logs --tail=30 app db
```

Saídas esperadas (valores ilustrativos, não transcrições de uma execução específica):

```json
{"status":"alive"}
{"status":"ready"}
{"total":1}
{"total":1}
```

Se o volume já tinha dados, o total será maior. `POST /visitas` incrementa; `GET /visitas` apenas lê. A atualização é atômica no banco. `/health/ready` executa `SELECT 1`: confirma conexão e consulta básica, mas **não verifica a tabela contador nem todas as operações**. Por isso também testamos `/visitas`.

Pergunte: “O que foi comprovado por cada comando?” `config` valida a declaração; `ps` informa estado; HTTP demonstra a resposta; POST seguido de GET demonstra escrita e leitura integradas.

## 2. Provar persistência

Anote o total antes de parar:

```sh
curl -fsS -X POST http://localhost:8080/visitas
curl -fsS http://localhost:8080/visitas
docker compose down
docker compose up -d --wait
curl -fsS http://localhost:8080/visitas
```

**Esperado:** o mesmo total da última leitura. Os containers foram recriados, mas o volume nomeado permaneceu. `stop/start` mantém o mesmo container; `down/up` o substitui. Volume não substitui backup.

O script `init.sql` só inicializa um diretório de dados vazio. Alterar esse arquivo ou `POSTGRES_PASSWORD` não modifica automaticamente um banco existente. Não apague volumes para “corrigir” mudanças de schema ou senha sem compreender e preservar os dados.

## 3. Observar cache de build

```sh
docker compose build app
docker compose build app
```

Observe as etapas marcadas `CACHED`. Edite apenas uma mensagem de log em `server.js`, refaça o build e observe a reutilização da instalação de dependências. Reverta a alteração pelo editor e reconstrua. O Dockerfile copia os manifests antes do código, evitando reinstalação quando apenas o código mudou. Alterar o lockfile pode invalidar a etapa de instalação. Build cria imagem; para executar a nova imagem, use `docker compose up -d --build --wait`.

Não confunda cache com atualização: `--no-cache` desativa reutilização de etapas; `--pull` consulta a base. Tags podem mudar, e o lockfile não fixa sozinho todos os componentes do ambiente.

## 4. Falha guiada A — localhost incorreto

Guarde a configuração correta antes de editar. Altere **somente** o hostname em `DATABASE_URL`, de `db` para `localhost` no serviço `app`. Mantenha o banco intacto.

```sh
docker compose up -d --no-deps --force-recreate app
curl -sS -i http://localhost:8080/health/ready
docker compose ps -a
docker compose logs --tail=30 app
docker compose exec db pg_isready -U aula -d aula
docker compose exec app node -e 'require("node:dns").lookup("db", (e,a)=>{console.log(e?e.code:a);process.exit(e?1:0)})'
```

O endpoint deverá retornar 503; os logs podem mostrar `ECONNREFUSED`. O banco pode estar saudável ao mesmo tempo. O DNS de `db` deve resolver para um endereço interno variável. **Causa:** a API procurou o banco em seu próprio loopback.

Corrija o hostname de volta para `db` e aplique:

```sh
docker compose up -d --no-deps --force-recreate --wait app
curl -fsS http://localhost:8080/health/ready
curl -fsS -X POST http://localhost:8080/visitas
curl -fsS http://localhost:8080/visitas
```

Não publicamos a porta do banco nem apagamos dados, pois essas ações não corrigem a causa identificada.

## 5. Falha guiada B — bind no loopback

Altere `HOST` do serviço `app` para `127.0.0.1` e recrie:

```sh
docker compose up -d --no-deps --force-recreate app
docker compose exec app node -e 'fetch("http://127.0.0.1:3000/health/live").then(async r=>console.log(r.status,await r.text()))'
curl --max-time 5 -sS -i http://localhost:8080/health/live
docker compose ps
```

**Esperado:** chamada interna funciona; chamada do host falha. Aguarde o processo iniciar se a primeira chamada interna for precoce. O healthcheck pode ficar verde, porque também acessa localhost **dentro** do container. A falha está na interface de escuta do processo, não no metadado `EXPOSE`.

Restaure `HOST: 0.0.0.0` e valide:

```sh
docker compose up -d --no-deps --force-recreate --wait app
curl -fsS http://localhost:8080/health/live
curl -fsS http://localhost:8080/health/ready
```

## 6. Falha guiada C — dependência indisponível

```sh
docker compose stop db
curl -sS -i http://localhost:8080/health/live
curl -sS -i http://localhost:8080/health/ready
curl -sS -i http://localhost:8080/visitas
docker compose logs --tail=30 app
```

**Esperado:** `live` responde 200; `ready` e `/visitas` respondem 503. O processo está vivo, porém a funcionalidade depende do banco. `depends_on: service_healthy` ajudou na partida; não garante disponibilidade contínua.

```sh
docker compose start db
docker compose exec db pg_isready -U aula -d aula
curl -fsS http://localhost:8080/health/ready
curl -fsS http://localhost:8080/visitas
```

Se o banco ainda estiver iniciando, aguarde e repita as verificações. O total deve continuar preservado. A aplicação trata falhas de consulta e de conexões ociosas, permitindo novas requisições após a recuperação. Isso não implementa retry ilimitado nem resolve idempotência de operações de escrita.

## Matriz de diagnóstico para usar em sala

| Sintoma | Hipótese | Verificação | Correção provável |
|---|---|---|---|
| Build falha no COPY | Lockfile ou arquivo fora do contexto | Mensagem do build; arquivos e `.dockerignore` | Corrigir contexto/arquivo |
| `npm ci` falha | Manifests e lock divergentes, download indisponível | Log da etapa; comparar manifests | Atualizar lock de forma controlada ou resolver acesso |
| Porta já alocada | Outro serviço usa 8080 | Erro de publicação; identificar serviço local | Liberar a porta ou alterar somente a porta do host |
| API recebe conexão recusada do DB | Host/porta incorretos ou banco parado | Logs, `pg_isready`, hostname configurado | Corrigir endereço ou recuperar dependência |
| Acesso interno OK e externo falha | Bind no loopback ou porta interna errada | Chamada dentro/fora e mapeamento | Corrigir bind/mapeamento |
| `relation ... does not exist` | Schema não inicializado/migração ausente | Erro SQL; conferir tabelas e inicialização | Aplicar migração apropriada; não apagar dados às cegas |
| API unhealthy, processo Up | Check está falhando | Executar o check e ler logs | Corrigir a causa; saúde não é sinônimo de processo vivo |
| Senha nova não funciona | Volume foi inicializado com credencial anterior | Histórico de inicialização/configuração | Alterar credencial do banco com procedimento apropriado |

## IA: prompt e registro

> Contexto: API Node.js retorna 503 em /health/ready; db está healthy. A URL usa localhost:5432. Seguem trechos sanitizados de configuração e logs. Liste três hipóteses priorizadas. Para cada uma, indique uma verificação não destrutiva, o resultado esperado e o que descartaria a hipótese. Proponha uma mudança por vez. Não apague volumes.

**Toda saída de IA é hipótese até ser validada por teste, execução ou revisão humana.** Não cole arquivos `.env`, dumps de `inspect` ou logs com segredos. Confira sugestões contra os arquivos, documentação e comportamento observado.

Use este registro no repositório da equipe:

```text
Sintoma e comando que reproduz:
Hipótese inicial:
Evidência que confirmou/descartou:
Causa identificada:
Mudança aplicada:
Comando e resultado após correção:
Prevenção/documentação:
IA (se usada): contexto sanitizado, sugestão aceita/rejeitada e validação:
```

## Atividade do projeto e critérios de aceite

1. **0–20 min:** empacotar a aplicação, controlar contexto e documentar variáveis.
2. **20–45 min:** integrar dependência no Compose, demonstrar rede, saúde e persistência pertinente ao projeto.
3. **45–70 min:** diagnosticar uma falha, registrar correção e testar instruções a partir de clone limpo.

Entregar no repositório: Dockerfile, `.dockerignore`, Compose, dependências controladas, README com setup/subida/teste/parada, evidência de integração e diagnóstico de uma falha. A escolha de linguagem continua livre. O incremento alimenta os **20% de Containers/Compose** já previstos; não altera os pesos da disciplina.

## Encerramento

Encerramento normal, preservando os dados:

```sh
docker compose down
```

**Somente para descartar os dados fictícios deste laboratório**, após conferir o projeto e aceitar perder seu contador:

```sh
docker compose down -v
```

Não use comandos globais de remoção/prune na máquina da turma.

## Referências oficiais

Consultadas em 21/09/2026:

- [Conceito de container](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
- [Dockerfile](https://docs.docker.com/reference/dockerfile/)
- [Cache de build](https://docs.docker.com/build/cache/invalidation/)
- [Boas práticas de build](https://docs.docker.com/build/building/best-practices/)
- [Rede no Compose](https://docs.docker.com/compose/how-tos/networking/)
- [Ordem de inicialização e saúde](https://docs.docker.com/compose/how-tos/startup-order/)
- [Volumes](https://docs.docker.com/engine/storage/volumes/)
- [Serviços e healthcheck](https://docs.docker.com/reference/compose-file/services/)
- [Imagem oficial PostgreSQL e inicialização](https://hub.docker.com/_/postgres)
