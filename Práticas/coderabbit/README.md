# Prática — revisão de código com IA usando CodeRabbit

**Encontro 2 · GitHub Flow, pull requests, testes e revisão humana.**

**Duração estimada:** 60–90 minutos, com ferramentas e autorização preparadas. **Organização:** uma execução por equipe, alternando quem implementa e quem revisa.

Você vai criar um fork de uma API de orçamento, abrir um pull request com um defeito proposital, analisar a revisão do CodeRabbit, reproduzir o erro com testes e enviar a correção ao mesmo PR. Todas as operações de Git, GitHub, testes e API deste roteiro são feitas pelo terminal.

> Toda saída de IA é hipótese até ser validada por teste, execução ou revisão humana.

## O que deve existir ao final

- Um fork da equipe com uma branch de trabalho e um PR próprio.
- Uma revisão real do CodeRabbit e a análise crítica de pelo menos um apontamento.
- Um commit com testes que reproduzem os defeitos e outro com a correção.
- Evidências de testes falhando antes e passando depois, incluindo validação HTTP.
- Uma conclusão humana registrada no PR.

A aplicação está em [unifor-docente/devops-coderabbit-demo](https://github.com/unifor-docente/devops-coderabbit-demo). O [PR nº 1 do professor](https://github.com/unifor-docente/devops-coderabbit-demo/pull/1) é referência de demonstração; a equipe trabalha no próprio fork e seu PR pode ter outro número. Este exemplo não substitui a escolha livre da aplicação do projeto integrador.

## 1. Preparar o ambiente e o acesso

São necessários Git, **Node.js 24 ou superior**, npm, GitHub CLI (`gh`), curl, editor de código e internet. Os comandos usam **Bash ou Zsh**. No Windows, utilize WSL com essas ferramentas instaladas. Mantenha a mesma sessão de terminal: as variáveis definidas serão reutilizadas.

```sh
git --version
node --version
npm --version
gh --version
curl --version
```

Se faltar alguma ferramenta, instale-a antes de continuar. Referências: [Node.js](https://nodejs.org/en/download) e [GitHub CLI](https://cli.github.com/).

Autentique o GitHub CLI e configure o Git para usar suas credenciais:

```sh
gh auth login
gh auth status
gh auth setup-git
```

No login, escolha GitHub.com e HTTPS. O fluxo de autenticação pode exigir confirmação no navegador. Essa confirmação e a autorização inicial do aplicativo CodeRabbit são pré-requisitos de acesso, não operações de edição de código.

**CodeRabbit:** o proprietário da conta/organização deve autorizar previamente o GitHub App para o fork da equipe assim que ele for criado na próxima etapa. Faça isso com apoio do professor antes da revisão. A instalação do professor não se transfere para forks. Consulte a [documentação de autorização](https://docs.coderabbit.ai/platforms/github-com). O roteiro não instala o aplicativo por um comando nem exige chave de API no workflow.

## 2. Criar o fork e definir o repositório de destino

Um integrante será o proprietário do fork. Na conta desse integrante, execute em uma pasta de projetos, fora de outro clone:

```sh
DONO=$(gh api user --jq .login)
REPO="$DONO/devops-coderabbit-demo"
BRANCH="pratica/coderabbit-desconto"

gh repo fork unifor-docente/devops-coderabbit-demo \
  --default-branch-only --clone=false

gh repo clone "$REPO"
cd devops-coderabbit-demo
gh repo set-default "$REPO"
git switch main
git remote -v
gh repo view "$REPO" --json nameWithOwner,url
```

**Confira:** `origin` e `nameWithOwner` devem apontar para a conta da equipe, não para `unifor-docente`. Os comandos GitHub deste roteiro também usam `--repo "$REPO"` para explicitar o destino.

Se a equipe usa uma organização, defina `DONO="NOME-DA-ORGANIZACAO"` e `REPO="$DONO/devops-coderabbit-demo"` e crie o fork com `gh repo fork unifor-docente/devops-coderabbit-demo --org "$DONO" --default-branch-only --clone=false`. Depois siga a clonagem acima. Use apenas uma das alternativas.

Se o fork ou a pasta já existir, confira seu conteúdo antes de continuar; não apague trabalho anterior nem repita a criação de branch sobre uma execução já corrigida.

Configure a autoria local dos commits, substituindo os exemplos:

```sh
git config user.name "Nome do integrante"
git config user.email "email-associado-ao-github"
```

Se outro integrante vai publicar commits, o proprietário pode conceder acesso pelo terminal:

```sh
gh api --method PUT "repos/$REPO/collaborators/LOGIN-DO-INTEGRANTE" \
  -f permission=push
```

O destinatário deve aceitar o convite. Não compartilhem credenciais.

Habilite o workflow do fork, se estiver desativado:

```sh
gh workflow list --all --repo "$REPO"
gh workflow enable testes.yml --repo "$REPO"
```

Se uma política da organização bloquear Actions, peça ao responsável para liberar a execução. A equipe também deve concluir a autorização do CodeRabbit para esse fork antes da etapa 6.

## 3. Conhecer e executar a API inicial

**Convenção:** todos os comandos seguintes são executados na raiz `devops-coderabbit-demo`, salvo indicação explícita. Usamos `npm --prefix app` para não precisar alternar de pasta.

| Arquivo | Responsabilidade |
|---|---|
| `app/src/orcamento.js` | Cálculo e validação do orçamento |
| `app/src/server.js` | API HTTP em `127.0.0.1:3000` |
| `app/test/orcamento.test.js` | Três testes iniciais |
| `.github/workflows/testes.yml` | CI executando `npm test` |
| `.coderabbit.yaml` | Configuração de revisão em português |
| `demo/preparar.js` | Gerador de defeito e solução guiada |
| `demo/desconto.test.js.txt` | Três testes de regressão para copiar depois |

Execute:

```sh
npm --prefix app test
npm --prefix app start
```

Não é necessário `npm install`: a API não tem dependências externas. A primeira execução deve mostrar **3 testes passando**. O segundo comando mantém o servidor em execução.

Em **outro terminal**, faça a requisição:

```sh
curl -i "http://127.0.0.1:3000/orcamento?precoCentavos=1000&quantidade=2"
```

Resultado: HTTP 200 e `{"subtotalCentavos":2000,"totalCentavos":2000}`. São duas unidades de R$ 10,00, totalizando R$ 20,00. A API retorna JSON; não existe página com formulário.

Encerre o servidor com **Ctrl+C** no primeiro terminal e continue nele. Sempre reinicie o servidor após modificar arquivos, pois não há recarga automática.

### Contrato que orienta a revisão

| Entrada/regra | Comportamento exigido |
|---|---|
| Preço | Inteiro não negativo em centavos |
| Quantidade | Inteiro entre 1 e 100 |
| Subtotal | Preço × quantidade, dentro do limite de inteiro seguro do JavaScript |
| Desconto novo | Percentual inteiro entre 0 e 100; padrão zero |
| Arredondamento | Centavo mais próximo, com meio centavo para cima |
| Entrada inválida | HTTP 400 |
| Exemplo | 10% de desconto em 2000 centavos resulta em 1800 |

A `main` contém a versão inicial sem desconto. A API já encaminha o parâmetro, mas a funcionalidade será implementada na branch do PR.

## 4. Conferir a configuração do CodeRabbit

```sh
cat .coderabbit.yaml
```

O arquivo já configura português (`pt-BR`), perfil `assertive`, resumo, revisão automática para PRs prontos e instruções sobre validação e testes. Ele deve continuar na raiz do repositório. O CodeRabbit lê o YAML da branch revisada; copiar o arquivo não substitui a instalação do aplicativo. [Referência de configuração](https://docs.coderabbit.ai/getting-started/yaml-configuration).

A CI e o CodeRabbit são independentes: o workflow executa testes; o aplicativo analisa o PR. Confira previamente a disponibilidade de revisão detalhada e os limites da conta. Se a integração estiver indisponível, conclua a parte local e registre a revisão externa como pendente.

## 5. Criar a branch com o defeito didático

Antes de executar, `git status --short` deve estar vazio:

```sh
git status --short
git switch main
git pull --ff-only origin main
git switch -c "$BRANCH"
git branch --show-current
npm --prefix app run demo:bug
npm --prefix app test
git diff -- app/src/orcamento.js
```

**Ponto de conferência:** a branch deve ser `pratica/coderabbit-desconto`. O gerador muda a assinatura da função e subtrai `desconto` diretamente do subtotal. Os **3 testes passam**, porque ainda não exercitam o desconto.

Publique somente a alteração da aplicação:

```sh
git add app/src/orcamento.js
git commit -m "feat: adicionar desconto percentual ao orçamento"
git push -u origin "$BRANCH"
```

Nunca implemente o desconto diretamente na `main`: essa é a base para repetir a prática.

## 6. Abrir o PR pelo terminal

Crie um arquivo temporário com a descrição, preenchendo os integrantes antes de enviar:

```sh
cat > /tmp/coderabbit-pr.md <<'TEXTO'
Implementa desconto percentual no cálculo do orçamento.

Critérios de aceite:
- Desconto inteiro de 0 a 100, padrão zero.
- 10% de desconto sobre 2000 centavos resulta em 1800 centavos.
- Arredondamento ao centavo mais próximo, com meio centavo para cima.
- Entrada inválida retorna HTTP 400.

Validação inicial: os três testes existentes passam.
Solicitamos revisão da regra de negócio e da cobertura de testes.

Contexto: atividade didática de revisão com IA.
Integrantes: PREENCHER.
TEXTO
```

Edite `/tmp/coderabbit-pr.md` no seu editor e abra o PR:

```sh
gh pr create --repo "$REPO" --base main --head "$BRANCH" \
  --title "feat: adicionar desconto percentual ao orçamento" \
  --body-file /tmp/coderabbit-pr.md

PR=$(gh pr view "$BRANCH" --repo "$REPO" --json number --jq .number)
gh pr view "$PR" --repo "$REPO" \
  --json url,baseRefName,headRefName,isDraft
```

Confira `baseRefName: main`, `headRefName: pratica/coderabbit-desconto` e `isDraft: false`. O endereço deve pertencer ao fork da equipe. Guarde esse link: ele será a evidência da atividade.

## 7. Solicitar e acompanhar a revisão da IA

Consulte primeiro a conversa:

```sh
gh pr view "$PR" --repo "$REPO" --comments
```

Se a revisão ainda não começou, solicite uma vez:

```sh
gh pr comment "$PR" --repo "$REPO" --body '@coderabbitai review'
```

Acompanhe os checks e consulte os comentários novamente após alguns minutos:

```sh
gh pr checks "$PR" --repo "$REPO"
gh pr view "$PR" --repo "$REPO" --comments
```

Para acompanhar continuamente, use `gh pr checks "$PR" --repo "$REPO" --watch` e Ctrl+C para sair. Se ainda não houver checks, espere o GitHub criar a execução antes de repetir a consulta.

| Mensagem | Interpretação e ação |
|---|---|
| `Review triggered` | Pedido recebido; aguarde |
| `Currently processing` / `Review in progress` | Análise em andamento; não repita o comando a cada consulta |
| `Review finished` | Leia a revisão e os comentários nas linhas |
| `testes` passou | Os testes existentes passaram; isso não comprova cobertura suficiente |
| `Merge Risk: High` | Leia os problemas apontados e reproduza-os antes de decidir |
| `Docstring Coverage` | Aviso sobre documentação; é diferente de erro de cálculo ou cobertura de testes |

Para ler os comentários nas linhas — que podem não aparecer integralmente em `gh pr view --comments` — execute:

```sh
gh api --paginate "repos/$REPO/pulls/$PR/comments" \
  --jq '.[] | {autor: .user.login, arquivo: .path, linha: .line, texto: .body, link: .html_url}'

gh api --paginate "repos/$REPO/pulls/$PR/reviews" \
  --jq '.[] | {autor: .user.login, estado: .state, texto: .body}'

gh pr diff "$PR" --repo "$REPO"
```

Se precisar conferir as opções efetivamente usadas:

```sh
gh pr comment "$PR" --repo "$REPO" --body '@coderabbitai configuration'
```

Depois leia a resposta na conversa. Para solicitar esclarecimento sobre um apontamento:

```sh
gh pr comment "$PR" --repo "$REPO" \
  --body '@coderabbitai Explique uma entrada que reproduza o erro do desconto e a saída esperada segundo o contrato deste PR.'
```

Registre a justificativa da equipe. A IA pode omitir defeitos ou propor mudanças desnecessárias; não aplique suas sugestões sem examinar o código. Referência: [revisões automáticas e manuais](https://docs.coderabbit.ai/configuration/auto-review).

## 8. Reproduzir os defeitos na API

Inicie o servidor no primeiro terminal:

```sh
npm --prefix app start
```

No segundo terminal:

```sh
curl -i "http://127.0.0.1:3000/orcamento?precoCentavos=1000&quantidade=2&desconto=10"
curl -i "http://127.0.0.1:3000/orcamento?precoCentavos=1000&quantidade=2&desconto=-1"
curl -i "http://127.0.0.1:3000/orcamento?precoCentavos=1000&quantidade=2&desconto=101"
curl -i "http://127.0.0.1:3000/orcamento?precoCentavos=3&quantidade=1&desconto=50"
```

| Caso | Resultado correto |
|---|---|
| 10% sobre 2000 | HTTP 200, total de 1800 centavos |
| Desconto -1 ou 101 | HTTP 400 |
| 50% sobre 3 centavos | HTTP 200, total de 2 centavos |

A versão defeituosa retorna 1990 no primeiro caso e aceita descontos inválidos. Compare o resultado real com o contrato e com a revisão. Encerre o servidor com Ctrl+C.

## 9. Criar testes que falham antes da correção

Na raiz do clone, copie os testes fornecidos:

```sh
cp demo/desconto.test.js.txt app/test/desconto.test.js
npm --prefix app test
```

**Esperado:** 3 testes iniciais passando e 3 novos falhando. Esses novos testes verificam percentual, limites/arredondamento e rejeição de argumentos inválidos na função. Eles não verificam diretamente o status HTTP.

Para cobrir também a API, crie o arquivo abaixo:

```sh
cat > app/test/desconto-http.test.js <<'JAVASCRIPT'
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { criarServidor } from '../src/server.js';

test('API aplica percentual e arredondamento e rejeita descontos inválidos', async (t) => {
  const servidor = criarServidor();
  await new Promise((resolve, reject) => {
    servidor.once('error', reject);
    servidor.listen(0, '127.0.0.1', resolve);
  });
  t.after(() => new Promise(resolve => servidor.close(resolve)));
  const base = `http://127.0.0.1:${servidor.address().port}/orcamento`;

  for (const [preco, quantidade, desconto, total] of [
    [1000, 2, 10, 1800],
    [3, 1, 50, 2],
    [1000, 2, 0, 2000],
    [1000, 2, 100, 0],
  ]) {
    const resposta = await fetch(
      `${base}?precoCentavos=${preco}&quantidade=${quantidade}&desconto=${desconto}`,
    );
    assert.equal(resposta.status, 200);
    assert.equal((await resposta.json()).totalCentavos, total);
  }

  for (const desconto of ['-1', '101', '10.5', 'abc', '']) {
    const resposta = await fetch(`${base}?precoCentavos=1000&quantidade=2&desconto=${desconto}`);
    assert.equal(resposta.status, 400, `desconto=${desconto} deve ser rejeitado`);
    assert.equal(typeof (await resposta.json()).erro, 'string');
  }
});
JAVASCRIPT

npm --prefix app test
```

Agora são **7 testes: 3 passam e 4 falham** na versão defeituosa. A primeira asserção que falha interrompe seu teste; por isso, leia também os demais casos escritos, mesmo que ainda não apareçam como falhas separadas.

Registre a etapa com erro no histórico:

```sh
git add app/test/desconto.test.js app/test/desconto-http.test.js
git commit -m "test: reproduzir defeitos do desconto na função e na API"
git push origin "$BRANCH"

gh run list --repo "$REPO" --branch "$BRANCH" --limit 5
```

Identifique a execução do commit recém-enviado. Substitua `ID-DA-EXECUCAO` pelo número retornado:

```sh
gh run watch ID-DA-EXECUCAO --repo "$REPO" --exit-status
gh run view ID-DA-EXECUCAO --repo "$REPO" --log-failed
gh run view ID-DA-EXECUCAO --repo "$REPO" --json url --jq .url
```

O status de falha é esperado nesta etapa. Guarde o link antes de corrigir. Podem existir duas execuções, uma de push e outra de pull request; ambas executam a mesma suíte.

## 10. Corrigir a implementação localmente

Confira a branch e abra `app/src/orcamento.js` no editor:

```sh
git branch --show-current
git status --short
```

A branch deve ser **`pratica/coderabbit-desconto`**. Faça duas alterações:

1. Valide `desconto`: inteiro entre 0 e 100, lançando erro quando inválido.
2. Substitua apenas `const totalCentavos = subtotalCentavos - desconto;` pelo cálculo percentual com arredondamento.

**Preserve `const subtotalCentavos = precoCentavos * quantidade;`** e sua validação. Subtotal e total têm funções distintas; remover o subtotal ou usar uma variável antes de declará-la quebra a API.

<details>
<summary>Solução de referência — consulte após discutir o diagnóstico</summary>

Uma implementação completa, com a decomposição do cálculo sugerida na demonstração, é:

```js
export function calcularOrcamento(precoCentavos, quantidade, desconto = 0) {
  if (!Number.isInteger(desconto) || desconto < 0 || desconto > 100) {
    throw new Error('Desconto deve ser um inteiro entre 0 e 100.');
  }
  if (!Number.isSafeInteger(precoCentavos) || precoCentavos < 0) {
    throw new Error('Preço deve ser um inteiro não negativo em centavos.');
  }
  if (!Number.isSafeInteger(quantidade) || quantidade < 1 || quantidade > 100) {
    throw new Error('Quantidade deve ser um inteiro entre 1 e 100.');
  }
  const subtotalCentavos = precoCentavos * quantidade;
  if (!Number.isSafeInteger(subtotalCentavos)) {
    throw new Error('Subtotal excede o limite suportado.');
  }
  const fator = 100 - desconto;
  const parteInteira = Math.floor(subtotalCentavos / 100);
  const resto = subtotalCentavos % 100;
  const totalCentavos =
    parteInteira * fator + Math.floor((resto * fator + 50) / 100);
  return { subtotalCentavos, totalCentavos };
}
```

O fator representa o percentual restante. A decomposição evita multiplicar diretamente todo o subtotal por 100; somar 50 antes da divisão inteira implementa o arredondamento exigido para valores não negativos.

Como alternativa, se o código ainda estiver exatamente na versão defeituosa original, execute `npm --prefix app run demo:fix`. O script usa uma solução equivalente com `BigInt` e copia os testes fornecidos. Não execute ambas as alternativas. Se a turma já alterou o código, conclua manualmente: o script não é uma ferramenta para mesclar edições.

</details>

Valide:

```sh
npm --prefix app test
git diff --check
git diff -- app/src/orcamento.js
```

**Esperado: 7 testes passando**, incluindo o novo teste HTTP. Não basta tornar a CI verde removendo asserções ou aceitando resultados incorretos. Reinicie a API e repita os exemplos da etapa 8 para verificar também a execução manual.

Envie a correção ao mesmo PR:

```sh
git add app/src/orcamento.js
git commit -m "fix: validar desconto e corrigir cálculo percentual"
git push origin "$BRANCH"

gh pr checks "$PR" --repo "$REPO"
gh run list --repo "$REPO" --branch "$BRANCH" --limit 5
```

Acompanhe a execução do novo commit com `gh run watch`, como na etapa anterior. **Não abra outro PR**: o existente recebe os novos commits automaticamente.

## 11. Ler a nova revisão e registrar a decisão humana

```sh
gh pr view "$PR" --repo "$REPO" --comments
gh api --paginate "repos/$REPO/pulls/$PR/comments" \
  --jq '.[] | {arquivo: .path, linha: .line, texto: .body, link: .html_url}'
```

Aguarde a revisão incremental. Se ela não iniciar, solicite com `gh pr comment "$PR" --repo "$REPO" --body '@coderabbitai review'`. Comentários antigos permanecem como histórico; confira a qual commit/trecho se referem antes de concluir que o problema continua.

Outro integrante deve comparar o contrato, a alteração e os testes. Não aceite nem rejeite um comentário apenas porque ele veio de uma IA. Um aviso de documentação pode ser tratado com uma descrição clara da função, mas não substitui validar a regra de negócio.

Crie a evidência no próprio repositório:

```sh
mkdir -p evidencias
cat > evidencias/revisao-coderabbit.md <<'TEXTO'
# Evidência da prática CodeRabbit

- Equipe e integrantes:
- URL do PR:
- Link do apontamento da IA analisado:
- Decisão da equipe e justificativa:
- Entrada usada para reprodução:
- Resultado antes da correção:
- Resultado depois da correção:
- URL da execução com testes falhando:
- URL da execução com testes passando:
- Commit da correção:
- Limitação da IA ou sugestão que exigiu análise humana:
- Revisor humano e conclusão:
TEXTO
```

Preencha o arquivo no editor. Depois publique-o e registre a conclusão na conversa:

```sh
git add evidencias/revisao-coderabbit.md
git commit -m "docs: registrar evidências da revisão com IA"
git push origin "$BRANCH"
gh pr comment "$PR" --repo "$REPO" --body-file evidencias/revisao-coderabbit.md
```

O workflow filtra alterações em código/testes/configuração; um commit contendo apenas `evidencias/` pode não iniciar outra execução. Nesse caso, associe a evidência ao commit de código testado, sem afirmar que houve um novo teste.

## 12. Entrega e preservação da atividade

Entregue o **link do PR da equipe** e inclua esse link no repositório do projeto integrador, onde ficam as evidências da disciplina.

- [ ] Fork próprio e CodeRabbit autorizado para ele.
- [ ] PR da branch de trabalho para a `main` do próprio fork.
- [ ] Revisão real da IA e apontamento analisado com justificativa.
- [ ] Testes de regressão falhando antes da correção.
- [ ] Sete testes passando após a correção, incluindo HTTP.
- [ ] Execuções de CI e commit de correção identificados.
- [ ] Evidência versionada e decisão humana registrada.

**Nesta prática, deixe o PR corrigido aberto, sem merge.** Assim a `main` mantém a aplicação inicial e outra execução pode gerar os defeitos novamente. O PR do professor também serve como referência do processo. Não é preciso recolocar erros na versão corrigida nem reescrever seu histórico.

Para repetir em um fork cuja `main` continua inicial, encerre processos locais, verifique que não há mudanças pendentes e crie outra branch:

```sh
git status --short
git switch main
git pull --ff-only origin main
BRANCH="pratica/coderabbit-desconto-2"
git switch -c "$BRANCH"
npm --prefix app run demo:bug
```

Retome os testes, commit, push e criação de PR das etapas 5 e 6. Atualize a variável `PR` para o novo número. O roteiro e os defeitos são conhecidos: esta é uma demonstração guiada, não um teste cego da capacidade da IA.

## Problemas comuns e recuperação

| Situação | Como diagnosticar e continuar |
|---|---|
| `gh` usa outra conta | Execute `gh auth status`; se necessário, `gh auth switch` e confira as permissões. |
| Variáveis vazias em um novo terminal | Redefina `DONO`, `REPO` e `BRANCH`; recupere `PR` com o comando da etapa 6. |
| PR aparece no repositório do professor | Confira `REPO` e use explicitamente `--repo "$REPO"`; o destino deve ser o fork. |
| Push negado | Confira `git remote -v`, autenticação e acesso de escrita. |
| Revisão não inicia | Confirme autorização do App para o fork, PR não draft, limites e resposta ao comando; registre a pendência se depender do administrador. |
| Bot ainda processando | Aguarde e consulte novamente; não envie comandos em sequência. |
| CI verde, sem revisão | São verificações independentes. Consulte os comentários e o check CodeRabbit. |
| Nenhum workflow executa | Use `gh workflow list --all` e `gh workflow enable testes.yml`, ambos com `--repo "$REPO"`; confira políticas e caminhos alterados. |
| Testes falham | Consulte `gh run view ID --log-failed --repo "$REPO"` e reproduza com `npm --prefix app test`. |
| Porta 3000 ocupada | Encerre o servidor anterior com Ctrl+C. |
| API apresenta código antigo | Reinicie o servidor depois de salvar. |
| Gerador recusa a alteração | Confira branch e `git diff`. Ele espera a versão inicial (`demo:bug`) ou o trecho defeituoso (`demo:fix`); não descarte edições para forçá-lo. |
| Subtotal ou desconto não definido | Confira assinatura e declaração do subtotal conforme a solução de referência. |
| Push rejeitado após edição remota | Com diretório limpo, execute `git pull --rebase origin "$BRANCH"`, resolva eventuais conflitos e teste; não use force push. |

Se você perceber que editou a `main` **antes de commitar**, interrompa o fluxo e use `git switch -c resgate/alteracao` para preservar as mudanças em uma nova branch. Se já publicou o commit errado, peça apoio para criar um commit de reversão específico; não use `reset --hard` ou force push no repositório compartilhado. A correção deve ir para a branch do PR.

## Discussão final

1. Por que os testes iniciais passaram com o cálculo errado?
2. O que a IA encontrou e o que a equipe precisou descobrir?
3. Qual a diferença entre teste da função e teste da API HTTP?
4. Que evidência justifica aceitar ou rejeitar uma sugestão?
5. Por que a revisão da IA não elimina a responsabilidade humana?

Referências adicionais: [manual do GitHub CLI](https://cli.github.com/manual/), [criar forks pela CLI](https://cli.github.com/manual/gh_repo_fork) e [criar PRs pela CLI](https://cli.github.com/manual/gh_pr_create). Esta atividade não altera os critérios de avaliação do projeto integrador.
