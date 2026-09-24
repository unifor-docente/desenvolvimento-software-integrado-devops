# Encontro 5 — release, contenção e rollback

Demonstração local para 25/09/2026. Evolui a API de visitas do encontro 4 em uma pasta e um projeto Compose separados. **As equipes mantêm seu próprio projeto integrador**; este exemplo explica as decisões de entrega.

O objetivo é distinguir artefato, configuração e dados: uma versão defeituosa passa no healthcheck, mas falha no teste da funcionalidade. Depois contemos o defeito com uma flag, recuperamos a versão anterior e entregamos a correção. Não há deploy em nuvem, publicação em registry nem implementação de rolling/canary/blue-green. A troca de uma única instância pode interromper o atendimento brevemente.

## Preparação

Docker Engine/Desktop e plugin Compose ativos; Python 3 padrão; terminal Bash/zsh; porta local 18085 livre; acesso para baixar base e dependências. No Windows, adapte `export` e as continuações para PowerShell, usando `curl.exe`. Execute na pasta deste README. A sintaxe dos slides e daqui usa Bash/zsh.

```sh
cd 'Práticas/encontro-5-entrega'
docker version
docker compose version
python3 --version
```

O nome padrão do projeto é `unifor-encontro5`. Antes de subir, confira `docker compose ls` e `docker ps`: não reutilize recursos de outra atividade. Para ensaios simultâneos, escolha um projeto e porta exclusivos, mantendo-os na mesma sessão:

```sh
export COMPOSE_PROJECT_NAME=e5-minha-equipe
export PORTA_HOST=18086
```

Os exemplos abaixo usam a porta padrão 18085; substitua os endereços e passe a URL correta a `verificar.py` caso altere a porta. Um nome de projeto diferente usa outro volume; isso não significa que o volume anterior foi perdido.

## Arquivos e contratos

| Arquivo/recurso | Responsabilidade |
|---|---|
| `server.js` | API HTTP, consulta PostgreSQL, rotas de versão e mensagem |
| `releases/*.json` | Metadados públicos usados para produzir três artefatos distintos |
| `Dockerfile` | Instala dependências pelo lockfile e copia a release selecionada |
| `compose.yaml` | Seleciona uma imagem pronta; integra app e db, sem reconstruir na promoção |
| `verificar.py` | Smoke com asserções de prontidão, versão, mensagem e leitura de dados |
| `dados` | Volume nomeado do banco; não é recriado a cada troca da API |

`GET /health/ready` faz uma consulta simples ao banco. `GET /version` mostra a versão embutida e a flag lida na partida. `GET /mensagem` retorna o conteúdo a validar. `GET/POST /visitas` lê/incrementa o contador. O valor de `/version` ajuda a observar, mas não é uma prova criptográfica da identidade do artefato.

Credenciais `aula/aula` são públicas e fictícias, somente para o banco local da demonstração. A imagem oficial cria o estado inicial em um diretório vazio; não representa uma política de acesso de produção. Este laboratório não usa segredos reais.

## 1. Construir e identificar — antes da aula

```sh
docker build --build-arg RELEASE=v1 -t e5-api:v1 .
docker build --build-arg RELEASE=v2-ruim -t e5-api:v2-ruim .
docker build --build-arg RELEASE=v2 -t e5-api:v2 .
docker image inspect --format '{{.Id}}' e5-api:v1
docker image inspect --format '{{.Id}}' e5-api:v2-ruim
docker image inspect --format '{{.Id}}' e5-api:v2
```

Anote os três IDs. O `ARG RELEASE` seleciona um arquivo público e não contém segredo. As tags são nomes locais: não as sobrescreva durante o ensaio. O ID da imagem local não deve ser confundido com o digest de manifesto de registry. Em entrega entre hosts, prefira registrar a referência distribuída por digest e sua plataforma.

## 2. Iniciar a referência

```sh
export APP_IMAGE=e5-api:v1
export FEATURE_BANNER=false
docker compose config --quiet
docker compose up -d --no-build --wait
python3 verificar.py
curl -fsS http://localhost:18085/version
curl -fsS -X POST http://localhost:18085/visitas
curl -fsS http://localhost:18085/visitas
```

Esperado: smoke `PASS`; versão `1.0.0`; mensagem `Bem-vindos!`. Anote o total **N** após o POST. O número depende do estado anterior do volume. Não remova dados para forçar N=1.

Se `up --wait` falhar, investigue antes de seguir:

```sh
docker compose ps -a
docker compose logs --tail=60 app db
```

## 3. Promover a candidata defeituosa — erro intencional

```sh
export APP_IMAGE=e5-api:v2-ruim
export FEATURE_BANNER=true
docker compose up -d --no-deps --no-build --wait app
curl -fsS http://localhost:18085/health/ready
curl -fsS http://localhost:18085/mensagem
python3 verificar.py http://localhost:18085 \
  2.0.0-ruim 'Bem-vindos à nova experiência!'
```

O último comando **deve terminar com erro**: `Mensagem funcional incorreta`. Não altere a expectativa para esconder o defeito. `ready` pode passar e `/mensagem` responder HTTP 200 com `Acesso negado`: o contrato funcional é que falhou. Num fluxo real, esse mesmo teste em homologação deveria barrar a promoção. Aqui a falha é provocada para estudar a recuperação num ambiente fictício.

## 4. Conter pela configuração

```sh
export FEATURE_BANNER=false
docker compose up -d --no-deps --no-build --wait app
python3 verificar.py http://localhost:18085 \
  2.0.0-ruim 'Bem-vindos!'
curl -fsS http://localhost:18085/version
```

Esperado: smoke passa no contrato antigo, mas a versão continua `2.0.0-ruim`. Isso é **contenção**, não correção do artefato nem rollback de imagem. A flag é lida na partida, então exige recriar app neste exemplo. Não há serviço de flags dinâmico.

## 5. Recuperar a imagem conhecida

```sh
export APP_IMAGE=e5-api:v1
export FEATURE_BANNER=false
docker compose up -d --no-deps --no-build --wait app
python3 verificar.py
curl -fsS http://localhost:18085/visitas
docker compose images app
```

Esperado: versão `1.0.0`, mensagem antiga e contador **N**, desde que não tenha havido outras gravações. Confirme o ID contra a referência inicial. Não ocorreu novo build nem migração de schema. O banco permanece em execução e o volume é mantido. Se o total mudar, verifique requisições concorrentes antes de concluir que houve perda.

## 6. Entregar a correção

```sh
export APP_IMAGE=e5-api:v2
export FEATURE_BANNER=true
docker compose up -d --no-deps --no-build --wait app
python3 verificar.py http://localhost:18085 \
  2.0.0 'Bem-vindos à nova experiência!'
curl -fsS http://localhost:18085/visitas
```

Esperado: mensagem nova correta, versão `2.0.0` e dados preservados. Registre o ID e os resultados. No fluxo do projeto, valide a candidata antes da promoção ao destino real. Esta demo tem apenas um ambiente local e não simula toda a infraestrutura de CI/CD.

## 7. Encerrar e registrar

```sh
docker compose down
```

Sem `-v`, o volume nomeado permanece. Não use remoção de volumes ou limpeza global como resposta ao erro de mensagem. Apenas o projeto selecionado deve ser encerrado.

Preencha [RELEASE-E-ROLLBACK.md](RELEASE-E-ROLLBACK.md), [CHECKLIST-SEGURANCA.md](CHECKLIST-SEGURANCA.md) e [REGISTRO-IA.md](REGISTRO-IA.md). O [exemplo preenchido](EXEMPLO-PREENCHIDO.md) demonstra o nível de detalhe esperado e distingue roteiro de resultado executado.

## Perguntas com explicação

- **Por que o healthcheck não acusou a mensagem errada?** Ele consulta a disponibilidade básica do banco, não o conteúdo de `/mensagem`.
- **Por que a flag não mudou sem recriação?** O servidor lê a variável ao iniciar; atualizar o shell não atualiza aquele processo.
- **Por que o rollback preservou o contador?** Somente app mudou; banco, schema e volume permaneceram. Voltar imagem não desfaz gravações de negócio.
- **O mesmo plano funcionaria após remover uma coluna?** Não necessariamente: a versão antiga pode depender dela. Planeje compatibilidade e eventual recuperação de dados.
- **Por que usamos `--no-build`?** Para selecionar um artefato já construído, em vez de gerar conteúdo novo durante a recuperação.
