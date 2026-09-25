# CI, entrega contínua e implantação contínua — exemplo do E5

## O que cada parte demonstra

| Material | O que faz | O que não comprova sozinho |
|---|---|---|
| README original | Comandos manuais de deploy, flag, rollback e correção. | Implantação contínua ou pipeline remoto. |
| promover.py | Automatiza aplicação da imagem, smoke e recuperação local quando possível. | Uma cadeia completa de CI/CD só por chamar o script. |
| workflow-cd-exemplo.yml | Conecta validação da candidata e entrega a laboratório persistente. | Implantação em produção, runner provisionado ou aprovação já configurada. |

O plano de ensino trata de **Continuous Delivery (entrega contínua)**. **Continuous Deployment (implantação contínua)** é comparada explicitamente: no caminho para produção, a promoção ocorre sem aprovação manual por versão quando os critérios automáticos passam. CI valida a integração; não prova que o destino foi atualizado.

## Ensaio local, sem GitHub nem nuvem

Pré-requisitos: Docker/Compose, Python 3, porta 18087 livre. Trabalhe apenas na cópia do laboratório. Os comandos usam um projeto diferente da demonstração manual (`e5-cd-local`); não apontam para produção.

```sh
cd Práticas/encontro-5-entrega
docker build --build-arg RELEASE=v1 -t e5-api:v1 .
docker build --build-arg RELEASE=v2-ruim -t e5-api:v2-ruim .
docker build --build-arg RELEASE=v2 -t e5-api:v2 .
python3 promover.py --imagem e5-api:v1 --versao 1.0.0 \
  --mensagem 'Bem-vindos!' --flag false
curl -fsS -X POST localhost:18087/visitas
curl -fsS localhost:18087/visitas
```

Anote o total N. A primeira entrega não tem referência anterior para rollback. A imagem deve existir localmente; o helper não reconstrói a candidata e resolve sua referência para o ID local. A imagem do banco pode precisar ser baixada na primeira subida.

Agora simule um defeito que escapou aos controles anteriores:

```sh
python3 promover.py --imagem e5-api:v2-ruim --versao 2.0.0-ruim \
  --mensagem 'Bem-vindos à nova experiência!'
```

Esperado: **código de saída 1**, resultado `falha` e recuperação da imagem/flag anteriores validada. A falha na mensagem provoca a recuperação; healthy sozinho não bastava. O deploy continua registrado como falha mesmo quando o rollback funciona. Se a recuperação também falhar, o relatório indica isso; investigar antes de seguir. Confira `/version` e `/visitas`: v1 e N preservado, sem novas gravações.

```sh
python3 promover.py --imagem e5-api:v2 --versao 2.0.0 \
  --mensagem 'Bem-vindos à nova experiência!'
curl -fsS localhost:18087/version
curl -fsS localhost:18087/visitas
```

Esperado: código zero, `promovida`, versão 2.0.0, nova mensagem correta e N preservado. O script não altera schema nem escreve no contador. Seu rollback é limitado a este laboratório com dados compatíveis; não generalizar para migrações destrutivas. A referência anterior precisa estar acessível e passar no smoke antes da promoção. O helper não é um controlador contínuo nem um sistema de monitoramento.

Encerrar somente este projeto, preservando volume:

```sh
APP_IMAGE=e5-api:v2 PORTA_HOST=18087 docker compose -p e5-cd-local down
```

## Como ler o workflow completo

O arquivo está **fora de `.github/workflows`**, portanto não ativa jobs neste repositório. É um modelo didático para leitura e adaptação. Ele requer preparação externa antes de ser executado:

1. **Job `ci`:** runner Ubuntu hospedado; constrói a release v2 do exemplo, inicia Compose temporário e executa o smoke. Falha impede exportação e impede o job dependente. É validação, não produção.
2. **Artefato:** `docker save` exporta a mesma imagem testada; o artifact guarda o tar e o ID local. Não há novo build no deploy. Num fluxo regular entre hosts, um registry com referência por digest é outra solução; ID local não é digest de manifesto de registry.
3. **Job `deploy`:** `needs: ci` estabelece a dependência. Usa um runner **Linux x64 persistente, dedicado, com label `e5-laboratorio`**, Docker/Compose, Python 3 e espaço para carregar a imagem. O host deve ser preparado pelo responsável. O banco, aplicação e volume persistem nesse host; não há `down` ao terminar o job de deploy.
4. **Environment:** configurar `e5-laboratorio` no GitHub com revisor obrigatório, se o recurso estiver disponível no plano e tipo de repositório. O YAML não cria a regra de aprovação. Sem essa regra, o deploy prossegue automaticamente após a CI.
5. **Pós-deploy:** o helper verifica imagem, versão, mensagem e leitura do banco. Em falha, tenta recuperação da referência anterior; o job recebe erro. Primeira entrega sem referência exige investigação.

O runner de deploy executa código do repositório e tem acesso ao Docker do host. Use somente repositório e branches confiáveis, com controle de acesso; não conecte esse runner a PRs não confiáveis/forks ou a um host de produção. O modelo não executa em `pull_request`. Não são necessários tokens de produção nem uma conta de nuvem para este laboratório. O token do workflow tem somente leitura de conteúdo; os artifacts são transferidos pelos mecanismos do GitHub Actions.

`localhost:18087` é o host do runner dedicado, não o computador de quem abre a interface do GitHub. A publicação fica no loopback; não disponibiliza uma URL pública. Se não houver runner adequado, use o ensaio local e leia o workflow; não marque o workflow remoto como executado.

## Comparação das duas políticas

- **Entrega com aprovação:** candidata validada → aprovação da promoção → deploy automatizado → teste no destino.
- **Implantação automática no laboratório:** candidata validada → política automática → deploy → teste, sem revisão manual por versão.
- **Continuous Deployment em produção:** exige que esse caminho automático chegue efetivamente ao ambiente de produção, com identidade, acesso, controles, observação e recuperação apropriados. Remover um revisor ou escrever `production` no YAML não cria esse ambiente.

O modelo é específico da API da disciplina e usa `RELEASE=v2` e o contrato 2.0.0. No projeto da equipe, adapte os comandos aos testes já criados no E3 e à imagem do E4. O incremento formal continua sendo plano de entrega, recuperação e segurança; não passa a exigir nuvem, produção ou runner remoto.

## Evidências para registrar

Evento/commit → resultado da CI → identidade da imagem → aprovação ou política → destino → teste após deploy → resultado da recuperação quando necessário. Distinguir planejado, executado e validado. No registro local, guardar o JSON produzido pelo helper e a leitura N antes/depois.

Fontes: [conceitos de CI/CD](https://www.redhat.com/en/topics/devops/what-is-ci-cd), [controle de deployments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments), [runners hospedados](https://docs.github.com/en/actions/concepts/runners/github-hosted-runners).
