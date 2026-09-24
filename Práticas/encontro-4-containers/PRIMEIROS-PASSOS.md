# Primeiros containers — demonstração antes da API com banco

Objetivo: observar um runtime em execução, distinguir imagem de instância e conhecer recursos básicos do Docker. Corresponde a E4·19–24. Use Bash/zsh, Docker Engine/Desktop ativo e uma porta local 18080 livre. No PowerShell, adapte as continuações de linha e use curl.exe.

## 1. Executar um programa curto

```sh
docker version
docker run --rm node:22-bookworm-slim node --version
```

`docker version` mostra cliente e servidor quando o Engine está acessível. No segundo comando, Docker obtém a imagem se necessário, cria uma instância e executa Node. A saída é `v22.x.x` (patch conforme a imagem). O processo termina e `--rm` remove essa instância; a imagem continua disponível. Não é necessário instalar Node no host.

## 2. Executar um servidor HTTP

Confira se a porta está livre e se o nome não pertence a outra instância. Para listar nomes e portas: `docker ps -a`. Use outro nome/porta se houver conflito e mantenha essa escolha nos comandos seguintes.

```sh
docker run -d --name e4-primeiro \
  -p 127.0.0.1:18080:3000 \
  node:22-bookworm-slim node -e '
    require("node:http").createServer((req, res) => {
      res.end("Olá, turma!\n");
    }).listen(3000, "0.0.0.0");
  '
curl --retry 5 --retry-connrefused --retry-delay 1 \
  -fsS http://localhost:18080
```

Resultado esperado: `Olá, turma!`. A repetição do curl tolera o breve intervalo entre o container iniciar e o processo começar a escutar. Também é possível abrir `http://localhost:18080` no navegador.

- `-d`: o servidor permanece em segundo plano.
- `--name`: permite referenciar esta instância.
- `127.0.0.1:18080:3000`: publica apenas no host local; o cliente usa 18080 e o processo escuta 3000.
- `0.0.0.0` no código: permite que o processo receba pelas interfaces do container. Não contradiz a publicação local no host; são camadas diferentes.

## 3. Observar enquanto está executando

```sh
docker ps
docker top e4-primeiro
docker logs --tail=20 e4-primeiro
docker exec e4-primeiro node --version
docker inspect --format '{{.State.Status}}' e4-primeiro
docker stats --no-stream e4-primeiro
```

| Recurso | Resultado e explicação |
|---|---|
| ps / top | Instância ativa / processo Node que atende HTTP. |
| logs | Pode ficar vazio: o código responde ao cliente, mas não emite logs de requisições. |
| exec | Outro processo Node imprime sua versão dentro da instância já existente. |
| inspect | `running`: estado gerenciado pelo Engine. |
| stats | Amostra de CPU, memória e I/O; números dependem do ambiente e da carga. |

`exec` exige container em execução; `inspect` também permite consultar um container parado. Estes comandos têm finalidades distintas e não são correções automáticas.

## 4. Parar, retomar e remover somente a demonstração

```sh
docker stop e4-primeiro
docker ps -a
docker start e4-primeiro
curl --retry 5 --retry-connrefused --retry-delay 1 \
  -fsS http://localhost:18080
docker stop e4-primeiro
docker rm e4-primeiro
```

Após stop, o servidor deixa de atender e a instância continua existindo. Start retoma essa instância. Run criaria outra. Depois de rm, a instância deixa de existir; a imagem Node permanece. Os comandos usam apenas o nome escolhido nesta demonstração, sem limpeza global nem alteração de volumes.

## 5. Conectar ao próximo exemplo

O servidor inline não tem código versionado numa imagem própria, dependência externa ou dados persistentes. A próxima etapa usa o Dockerfile da [API de visitas](README.md), inicialmente isolada, e depois integra PostgreSQL via Compose. Assim cada recurso novo resolve uma necessidade já visível.

## Perguntas já acompanhadas de resposta

**Por que a primeira execução terminou e a segunda permaneceu ativa?** O comando `node --version` imprime e encerra; o servidor mantém o processo atendendo conexões.

**O Node do host mudou?** Não. O executável usado pertence à imagem da instância.

**A porta publicada faz o servidor existir?** Não. Ela encaminha tráfego; o processo precisa escutar no destino correto.

**Por que logs pode estar vazio com HTTP funcionando?** Docker recolhe a saída emitida pelo processo, e este exemplo não registra cada requisição em stdout/stderr.
