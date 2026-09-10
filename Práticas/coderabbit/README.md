# Prática — revisão de código com IA usando CodeRabbit

**Encontro 2 · GitHub Flow, pull requests e qualidade · 45–60 minutos**, com as ferramentas instaladas previamente.

Você vai executar uma API de orçamento, propor um desconto em um pull request (PR), analisar a revisão da IA e comprovar a correção com testes. Ao final, a equipe terá um PR com comentários, testes de regressão e uma decisão de revisão humana.

> Toda saída de IA é hipótese até ser validada por teste, execução ou revisão humana.

## 1. Organização e pré-requisitos

- Uma conta GitHub por integrante e uma conta com permissão para instalar o CodeRabbit no repositório da equipe.
- Git, Node.js **24 ou superior** e npm instalados; editor de código e navegador.
- Acesso à internet para GitHub e CodeRabbit.
- Um fork por equipe. Um integrante conduz os comandos e outro revisa; todos participam da análise.

Confirme no terminal:

```sh
node --version
npm --version
git --version
```

Se o Git solicitar identificação ao fazer commit, configure seu nome e e-mail no clone com `git config user.name "Seu Nome"` e `git config user.email "seu-email"`. Para enviar commits, use a autenticação GitHub já configurada na máquina; quem utiliza GitHub CLI pode executar `gh auth login`. Não coloque senhas ou tokens nos arquivos.

**Links da atividade:**

- [Repositório da aplicação](https://github.com/unifor-docente/devops-coderabbit-demo)
- [PR nº 1 do professor — demonstração](https://github.com/unifor-docente/devops-coderabbit-demo/pull/1)
- [CodeRabbit](https://app.coderabbit.ai/)

O PR do professor serve para acompanhar a demonstração. A equipe deve criar seu próprio PR no próprio fork; seu número pode ser diferente de 1. A instalação do CodeRabbit no repositório do professor não é transferida para o fork.

## 2. Criar e clonar o fork da equipe

1. Abra o repositório da aplicação e clique em **Fork**.
2. Escolha a conta de um integrante ou a organização da equipe como proprietária.
3. Mantenha o nome `devops-coderabbit-demo` e marque **Copy the main branch only**, se a opção aparecer.
4. Clique em **Create fork**.
5. No fork, abra **Code → HTTPS** e copie a URL. Use essa URL no comando abaixo, substituindo `SEU-USUARIO-OU-ORGANIZACAO`.

```sh
git clone https://github.com/SEU-USUARIO-OU-ORGANIZACAO/devops-coderabbit-demo.git
cd devops-coderabbit-demo
git remote -v
git switch main
```

Confira que `origin` aponta para a conta da equipe. Os próximos commits serão enviados para ela. Se outros integrantes forem enviar alterações, o proprietário deve conceder acesso nas configurações do repositório.

Abra a aba **Actions** do fork. Se o GitHub apresentar a opção de habilitar workflows, habilite-os para executar os testes da atividade. Consulte a [orientação oficial sobre forks](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/fork-a-repo) se precisar de ajuda.

## 3. Executar a versão inicial

Na raiz do clone da API:

```sh
cd app
npm test
npm start
```

Não é necessário executar `npm install`: esta aplicação usa apenas recursos nativos do Node.js. Os **três testes iniciais devem passar**.

Com o servidor rodando, abra no navegador:

<http://127.0.0.1:3000/orcamento?precoCentavos=1000&quantidade=2>

Resposta esperada:

```json
{"subtotalCentavos":2000,"totalCentavos":2000}
```

Isso representa duas unidades de R$ 10,00, totalizando R$ 20,00. A aplicação é uma API: o navegador mostra JSON, sem formulário visual.

Encerre o servidor com **Ctrl+C** antes de continuar. Sempre reinicie `npm start` após alterar o código; não há recarga automática.

### Entender os arquivos

| Arquivo na raiz do clone | Função |
|---|---|
| `app/src/orcamento.js` | Regra de cálculo e validação |
| `app/src/server.js` | API HTTP local na porta 3000 |
| `app/test/orcamento.test.js` | Testes iniciais da regra e da API |
| `.github/workflows/testes.yml` | Execução dos testes no GitHub Actions |
| `.coderabbit.yaml` | Instruções de revisão para o CodeRabbit |
| `demo/preparar.js` | Preparação da alteração didática e solução guiada |
| `demo/desconto.test.js.txt` | Testes de regressão que serão adicionados depois |

### Contrato da nova funcionalidade

- Preço: inteiro não negativo em centavos.
- Quantidade: inteiro entre 1 e 100. O subtotal deve caber em um inteiro seguro de JavaScript.
- Desconto: **percentual inteiro entre 0 e 100**, com padrão zero.
- O desconto incide sobre o subtotal; o total é arredondado ao centavo mais próximo, com meio centavo para cima.
- Entrada inválida deve produzir HTTP 400.
- Exemplo: subtotal de 2000 centavos com desconto de 10% resulta em **1800 centavos**.

A versão inicial ainda não implementa o desconto, embora a API já encaminhe esse parâmetro à função.

## 4. Conectar o CodeRabbit ao fork

O proprietário do fork realiza esta etapa:

1. Entre em [CodeRabbit](https://app.coderabbit.ai/) com **Login with GitHub**.
2. Selecione a conta ou organização que possui **o fork da equipe**.
3. Instale/autorize o aplicativo GitHub do CodeRabbit. Em **Only select repositories**, selecione `devops-coderabbit-demo` dessa conta.
4. Conclua **Install & Authorize** ou **Save**. Em uma organização, pode ser necessária a autorização de seu proprietário.
5. Confirme no painel que o fork aparece entre os repositórios conectados.

Se a tela inicial pedir um PR e a equipe ainda não criou nenhum, use **Skip to the app**, conclua a próxima etapa e depois solicite a revisão pelo GitHub. Instruções oficiais: [conectar CodeRabbit ao GitHub](https://docs.coderabbit.ai/platforms/github-com).

### Preciso alterar as configurações no painel?

O fork já contém `.coderabbit.yaml` na raiz, com idioma `pt-BR`, perfil `assertive`, resumo e revisão automática de PRs que não sejam rascunhos. O arquivo também orienta a análise de cálculos, validações e testes. O CodeRabbit lê a configuração da branch em revisão. [Documentação do YAML](https://docs.coderabbit.ai/getting-started/yaml-configuration).

Na tela **General**, a opção **Use Organization Settings** pode deixar campos como **Language** desabilitados. Não é necessário alterar esses campos para iniciar a prática; mantenha o YAML fornecido. Para conferir a configuração efetivamente usada, publique posteriormente no PR:

```text
@coderabbitai configuration
```

A resposta informa a configuração resolvida e suas fontes. Se houver divergência de idioma ou comportamento, use essa resposta para investigar com o professor.

**Instalar o aplicativo e configurar o YAML são etapas diferentes.** Só copiar o arquivo não concede acesso ao repositório. Esta integração não exige chave de API no workflow nem extensão de editor. Confira no painel a disponibilidade de revisão detalhada e os limites da conta antes da atividade; não é necessário contratar um plano para seguir as etapas locais.

## 5. Preparar a alteração e abrir o PR

Os comandos desta seção são executados **dentro da pasta `app`**, após encerrar o servidor:

```sh
git switch -c pratica/coderabbit-desconto
npm run demo:bug
npm test
git diff
git add src/orcamento.js
git commit -m "feat: adicionar desconto percentual ao orçamento"
git push -u origin pratica/coderabbit-desconto
```

O gerador introduz uma implementação defeituosa para análise. Os três testes continuam passando porque não verificam desconto. Observe em `git diff` qual cálculo foi adicionado.

No GitHub, abra o fork da equipe e clique em **Compare & pull request** ou **Pull requests → New pull request**. Confira antes de criar:

| Campo | Valor |
|---|---|
| Base repository | **Fork da equipe**, e não `unifor-docente/devops-coderabbit-demo` |
| Base | `main` |
| Head repository | Fork da equipe |
| Compare | `pratica/coderabbit-desconto` |

Se necessário, use **compare across forks** para selecionar os repositórios. Crie um PR normal, **sem marcar como draft**. Use o texto:

```text
Título: feat: adicionar desconto percentual ao orçamento

Implementa desconto percentual no cálculo do orçamento.

Critérios de aceite:
- Desconto inteiro de 0 a 100, padrão zero.
- 10% de desconto sobre 2000 centavos resulta em 1800 centavos.
- Arredondamento ao centavo mais próximo, com meio centavo para cima.
- Desconto inválido retorna HTTP 400.

Validação inicial: os três testes de npm test passaram.
Solicitamos revisão da regra de negócio e da cobertura de testes.

Contexto: atividade didática de revisão com IA.
Equipe: preencher os nomes dos integrantes.
```

## 6. Solicitar e interpretar a revisão

1. Na aba **Conversation** do PR da equipe, procure a resposta do CodeRabbit.
2. Se ainda não houver revisão, vá ao campo **Add a comment**, publique o comando abaixo e aguarde. O comando é escrito **no GitHub, não no terminal**.

```text
@coderabbitai review
```

Esse comando solicita revisão manual; novos pushes também podem gerar revisão incremental. [Controles oficiais de revisão](https://docs.coderabbit.ai/configuration/auto-review).

3. Leia o resumo em **Conversation** e os comentários nas linhas em **Files changed**.
4. Escolha um apontamento e responda no próprio tópico, por exemplo:

```text
@coderabbitai Explique uma entrada que reproduza esse problema e a saída esperada segundo o contrato do PR.
```

5. Registre se a equipe concorda e valide a observação pela execução ou por um teste.

**“All checks have passed” não significa necessariamente que a IA revisou o código.** Abra os detalhes dos checks: o job `testes` executa testes automatizados; a revisão do CodeRabbit deve ser verificada separadamente, pelos comentários e pelo estado da revisão. A IA pode deixar passar defeitos ou sugerir mudanças desnecessárias.

## 7. Reproduzir os defeitos

Dentro de `app`, execute `npm start` e abra:

<http://127.0.0.1:3000/orcamento?precoCentavos=1000&quantidade=2&desconto=10>

A implementação defeituosa retorna **1990 centavos (R$ 19,90)**. O contrato exige **1800 centavos (R$ 18,00)**. O cálculo está subtraindo 10 centavos em vez de aplicar 10%.

Experimente também estas entradas, mantendo preço 1000 e quantidade 2:

| Desconto | Resultado correto |
|---|---|
| `0` | Total de 2000 centavos |
| `100` | Total de zero centavos |
| `-10` | HTTP 400 |
| `101` | HTTP 400 |
| `1.5` | HTTP 400 |

Para conferir o status HTTP, use a aba **Network/Rede** das ferramentas do navegador ou, em outro terminal:

```sh
curl -i "http://127.0.0.1:3000/orcamento?precoCentavos=1000&quantidade=2&desconto=-10"
```

Compare os resultados com os apontamentos da IA. Encerre o servidor com Ctrl+C.

## 8. Adicionar testes antes de corrigir

Ainda em `app`, copie os testes de regressão:

```sh
cp ../demo/desconto.test.js.txt test/desconto.test.js
npm test
```

Alternativamente, copie pelo editor o conteúdo de `demo/desconto.test.js.txt` para `app/test/desconto.test.js`.

O resultado esperado agora é **três testes passando e três falhando**. Guarde a saída para a evidência. Leia as falhas: elas cobrem cálculo percentual, limites/arredondamento e validação do desconto.

Para registrar a etapa com falha no histórico e no GitHub Actions:

```sh
git add test/desconto.test.js
git commit -m "test: reproduzir defeitos no desconto"
git push
```

Aguarde a execução desse commit em **Actions** e registre o link do resultado com falha antes de prosseguir. A falha aqui é esperada e comprova que os testes detectam os defeitos.

## 9. Corrigir e atualizar o mesmo PR

Edite `app/src/orcamento.js` para atender ao contrato. Preserve a validação de preço, quantidade e subtotal. Valide o desconto e calcule o percentual com o arredondamento exigido.

<details>
<summary>Solução guiada — abra após discutir a correção com a equipe</summary>

Se a função ainda contém o trecho defeituoso original, execute dentro de `app`:

```sh
npm run demo:fix
```

O script aplica a solução e copia novamente os testes fornecidos. Se a equipe já alterou o trecho, ele recusará a substituição; conclua manualmente. Ele não precisa ser executado se a correção manual já estiver pronta.

A solução fornecida usa `BigInt` no cálculo intermediário para evitar perda de precisão perto do limite de inteiros seguros e converte o total de volta para número.

</details>

Execute:

```sh
npm test
```

Os **seis testes fornecidos devem passar**. Reinicie a API e repita os exemplos da seção 7: 10% deve retornar 1800 e desconto inválido deve produzir HTTP 400. Confira também preço de 101 centavos, quantidade 1 e desconto de 50%: o total esperado é 51 centavos. Encerre o servidor.

Envie a correção, ainda dentro de `app`:

```sh
git add src/orcamento.js test/desconto.test.js
git commit -m "fix: validar desconto e corrigir cálculo percentual"
git push
```

O PR existente será atualizado automaticamente; não abra outro. Acompanhe os testes do commit mais recente e a nova revisão do CodeRabbit. Se necessário, comente novamente `@coderabbitai review`.

## 10. Revisão humana e evidências

Outro integrante deve examinar o diff, os testes e as respostas do bot. Registre no PR uma conclusão usando este modelo:

```text
Equipe e integrantes:

Apontamento da IA analisado (link):
Decisão: aceito / rejeitado, porque...
Entrada utilizada para reprodução:
Resultado antes e resultado depois:
Link da execução de testes com falha:
Link da execução de testes corrigida:
Commit da correção:
Limitação ou sugestão da IA que exigiu análise humana:
Revisor humano e conclusão:
```

A evidência principal é o **link do PR da equipe**, com esse registro. Mantenha-a no repositório da equipe; se a disciplina centraliza a entrega no repositório do projeto integrador, inclua nele o link desta prática.

Checklist de conclusão:

- [ ] Fork da equipe conectado ao CodeRabbit.
- [ ] PR aberto dentro do próprio fork.
- [ ] Revisão real da IA registrada e um apontamento analisado criticamente.
- [ ] Defeito reproduzido e teste de regressão falhando antes da correção.
- [ ] Correção enviada ao mesmo PR, testes locais e CI passando.
- [ ] Nova revisão acompanhada e decisão humana registrada.

Faça merge no fork somente após esses critérios e a revisão humana. O PR do professor permanece como referência de demonstração. Se a integração externa estiver indisponível, registre o bloqueio e conclua as etapas locais; a revisão da IA fica pendente, sem inventar comentários ou atribuir à ferramenta uma análise feita pela equipe.

## Problemas comuns

| Situação | Como proceder |
|---|---|
| Repositório não aparece no CodeRabbit | Confira a conta/organização selecionada e o acesso do aplicativo ao fork; atualize a lista após salvar a autorização. |
| Não há PR para selecionar no onboarding | Use **Skip to the app**, crie o PR e solicite a revisão nele. |
| Bot não responde ao comando | Confirme que o comando foi publicado, o PR está no fork autorizado e não é draft; consulte avisos de acesso, habilitação e limites no painel. Evite enviar o mesmo comando repetidamente. |
| Campos de configuração desabilitados | Veja **Use Organization Settings**; consulte a configuração efetiva com `@coderabbitai configuration`. |
| Há checks verdes, mas nenhum comentário da IA | Confira os nomes dos checks. Testes da CI e revisão do CodeRabbit são verificações distintas. |
| Nenhum workflow executa no fork | Abra **Actions**, habilite os workflows quando solicitado e reenvie uma alteração de código/teste. |
| `npm` não encontra `package.json` | Entre na pasta `app` do clone da API. |
| Porta 3000 ocupada | Encerre a execução anterior da API com Ctrl+C antes de iniciar outra. |
| API continua exibindo o resultado antigo | Reinicie `npm start` após salvar o código. |
| `demo:bug` ou `demo:fix` recusa a alteração | O script espera uma versão específica. Confira `git diff` e a branch; não descarte o trabalho da equipe. Solicite ajuda ao professor. |
| Push negado | Confira `git remote -v`, autenticação e permissão de escrita no fork. |

## Discussão final

1. Por que os testes iniciais passavam com o desconto errado?
2. Quais problemas a IA identificou e quais a equipe encontrou por conta própria?
3. Como um teste transforma uma sugestão da IA em evidência verificável?
4. Quem assume a responsabilidade pelo merge?

Esta é uma demonstração guiada: o roteiro e os exemplos de defeito ficam visíveis no repositório, portanto não constituem um teste cego da capacidade da IA. A prática apoia a aula e não altera a escolha livre da aplicação nem os critérios de avaliação do projeto integrador.
