# Encontro 5 — roteiro de condução em quatro horas

**25/09/2026 • revisão em 23/09.** A trilha tem 55 slides; outros 5 ficam para consulta. Use os rodapés E5·NN. A capa institucional é a primeira página; os fundamentos vêm antes do primeiro checkpoint.

## Distribuição do tempo

| Minutos | Slides E5 | Condução |
|---|---|---|
| 0–10 | 01–02 | Retomar o ambiente executável do E4 e explicar o objetivo de controlar mudanças. |
| 10–35 | 03–10 | Definir vocabulário, CI/CD, identidade, ambientes e critérios; primeira verificação. |
| 35–60 | 11–18 | Separar artefato/configuração/estado; segredos, caso de exposição, IaC e GitOps; gabarito. |
| 60–90 | 19–27 | Comparar estratégias; explicar flag, rollback, schema, release notes e runbook com exemplos. |
| 90–105 | — | Intervalo de 15 minutos. |
| 105–140 | 28–37 | Demonstração preparada: referência → defeito → contenção → rollback → correção. Verificação de recuperação. |
| 140–165 | 38–48 | Segurança e IA: interpretar um achado, permissões, prompt injection, registro e gabarito. |
| 165–235 | 49–53 | 70 minutos no próprio projeto. Orientações no início; plano, ensaio quando possível e evidências. Verificação final durante a revisão das equipes. |
| 235–240 | 54–55 | Conectar os registros de entrega à observabilidade e apresentação do E6. |

Total: 240 minutos, com 15 de intervalo e 70 de prática. As respostas são explicadas dentro do tempo de cada bloco, sem criar uma segunda aula de exercícios.

## Antes da aula

Ensaiar o README e baixar as imagens. Construir as três versões antes de apresentar; o slide de build explica a preparação, não precisa consumir o tempo da demo. Conferir porta, nome do projeto e Python 3. Deixar os arquivos e templates abertos. Usar dados fictícios e os serviços exclusivos do E5.

## Como explicar os pontos centrais

**CI/CD:** “O CI testou a integração de código. Agora precisamos identificar o artefato, aplicar no destino e verificar a operação. Um verde não substitui o outro.”

**Artefato:** “A tag dá um nome. A evidência precisa apontar para o conteúdo que foi testado. Construir de novo pode mudar esse conteúdo, mesmo com o mesmo nome.”

**Configuração:** “A imagem é a mesma, mas a flag muda o caminho. Como nossa API lê a variável na partida, reaplicamos a configuração para observar a mudança.”

**Deploy e release:** “O código pode estar instalado com a função desligada. Instalar e disponibilizar são decisões separáveis.”

**Recuperação:** “Desligar a flag contém. Voltar à v1 restaura uma imagem conhecida. Promover a v2 corrigida resolve adiante. Nenhuma dessas ações apaga automaticamente efeitos no banco.”

**Saúde:** “O check diz que uma consulta básica funcionou. Não diz que a saudação está correta. Vamos comparar conteúdo esperado e observado.”

**Segurança:** “Que risco esta análise procura? O que ficou fora? O que faremos com o achado? A resposta deve incluir uma evidência, não só um nome de scanner.”

**IA:** “Uma sugestão é uma hipótese. O log pode conter uma ordem de terceiros, mas essa ordem não recebeu autoridade da equipe. Vamos controlar ações e verificar o efeito.”

## Ritmo e adaptação

O bloco de segurança é denso. Mostre as categorias e aprofunde um caso: token no log ou correção que apaga o teste. Deixe perguntas específicas de ferramentas para consulta. Preserve a execução da falha funcional, a comparação contenção/rollback e o trabalho das equipes.

Não trate os cinco checkpoints como prova individual. Ouça justificativas breves, revele o gabarito e retome uma figura se necessário. Na prática, os mesmos integrantes desenvolvem o mesmo projeto; não há nova nota individual nem mudança de pesos.

A entrega formal continua sendo o plano de release, recuperação e checklist com evidências no repositório. Se não houver ensaio executável, documente pré-requisitos e limitações; não marque como testado. Um deploy público ou assinatura de ferramenta paga não é requisito.

## Consulta

E5·56–60: ambientes protegidos no GitHub, OIDC, SBOM/proveniência/assinatura, política de canary e leitura de plano Terraform. São extensões conceituais, sem novas exigências.

## Navegação

- [Guia por slide](Guia%20ampliado%20do%20professor.md)
- [Questões e gabaritos](Índice%20de%20perguntas%20e%20respostas.md)
- [Laboratório executável](../../Práticas/encontro-5-entrega/README.md)
- [Modelo preenchido](../../Práticas/encontro-5-entrega/EXEMPLO-PREENCHIDO.md)
