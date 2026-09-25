# Encontro 5 — roteiro de condução em quatro horas

**25/09/2026 • revisão de CI/CD.** 65 slides na trilha principal e 5 de consulta. Rodapés E5·NN; página do PDF independente = NN + 1. A capa mantém a identidade da disciplina.

| Minutos | Slides E5 | Condução |
|---|---|---|
| 0–10 | 01–02 | Resultado: controlar a entrega ao destino; retomar o E4. |
| 10–40 | 03–13 | Vocabulário; comparar CI, Delivery e Deployment; artefato e gates; gabarito. |
| 40–60 | 14–21 | Configuração, segredos, IaC/GitOps como panoramas; gabarito. |
| 60–90 | 22–37 | Estratégias e recuperação; ler a automação, destino e aprovação; gabarito. |
| 90–105 | — | Intervalo de 15 minutos. |
| 105–140 | 38–47 | Ensaio local: referência, defeito, contenção, rollback e correção. Relacionar as ações com promover.py; gabarito. |
| 140–165 | 48–58 | Segurança e IA: aprofundar um caso, explicar responsabilidades e gabarito. |
| 165–235 | 59–63 | 70 minutos no projeto; orientação e verificação dentro da atividade. |
| 235–240 | 64–65 | Evidências e ligação com observabilidade. |

Total: 240 minutos. Os dez slides novos substituem explicações genéricas por fluxos e exemplos; não acrescentam outro laboratório obrigatório. No bloco 60–90, reserve aproximadamente 12 min para estratégias/recuperação e 18 para automação e verificação. Trate as tabelas como apoio, sem ler cada célula. Preserve a demonstração, os gabaritos e a prática das equipes.

## A mensagem que precisa ficar clara

“CI valida a mudança. Entrega contínua mantém a capacidade de implantar quando decidido; o deploy pode ser automatizado após aprovação. Implantação contínua leva as mudanças que passam nos critérios à produção sem aprovação manual por versão.”

Compare E5·05–07 apontando a intervenção humana. Em E5·31–35, siga o artefato da CI até o destino. Nome de job, pipeline verde ou environment chamado production não comprova uma aplicação implantada para usuários.

## Como explicar o exemplo de workflow

Abra `Práticas/encontro-5-entrega/workflow-cd-exemplo.yml` junto de `AUTOMACAO-CD.md`. Explique:

1. CI constrói a imagem da candidata e testa a operação num runner temporário.
2. A mesma imagem é exportada; o deploy não faz outro build.
3. `needs: ci` exige o sucesso da etapa anterior.
4. A aprovação depende da regra configurada no environment; não é criada por seu nome no YAML.
5. Um runner dedicado aplica a imagem no laboratório persistente; o temporário da CI não é esse destino.
6. O helper testa após o deploy; se falhar, tenta recuperar a referência anterior e mantém o job como falha.

O arquivo é um modelo fora da pasta de workflows ativos. Não configurar runners ou contas reais durante a exposição. Com revisor no environment, ilustra entrega com aprovação; sem revisor, automatiza a implantação naquele laboratório. Nenhuma das duas situações deve ser apresentada como produção real.

## Antes da demonstração

Ensaiar o README, construir as três imagens e conferir portas. Deixar comandos e templates abertos. A prática manual usa 18085 e `unifor-encontro5`; o helper usa 18087 e `e5-cd-local`. São destinos de laboratório distintos, com volumes próprios. Não compare os contadores como se fossem o mesmo banco.

## Como conectar o ensaio manual à automação

A sequência E5·38–47 permite explicar cada ação isoladamente. Diga: “Estou executando manualmente para vocês verem cada decisão; isso ainda não é implantação contínua.” Depois aponte em promover.py onde aplicar, verificar e recuperar foram automatizados. Se o helper já foi ensaiado, mostre seu resultado ou faça uma passagem curta; não repita duas demonstrações completas.

A versão defeituosa é promovida deliberadamente para ensinar o caso de um problema que escapou aos controles anteriores. No workflow fornecido, o smoke da CI deveria bloquear esse defeito conhecido. São cenários didáticos diferentes: gate antes da promoção e verificação no destino após a promoção. Não ensine a ignorar uma CI vermelha para reproduzir a falha.

## Trabalho das equipes

O plano deve identificar evento, imagem/artefato, executor, destino, aprovação ou política, teste pós-deploy e recuperação. Cada equipe classifica o que tem hoje: CI, ensaio manual, passos automatizados ou fluxo de entrega conectado. Não exigir implantação pública ou um runner remoto novo. O projeto continua o mesmo, com 15% de Entrega e Operação e avaliação em grupo.

Nos 70 minutos: 0–20 preparar a mudança e critérios; 20–45 ensaiar se o ambiente permitir; 45–70 registrar resultados e revisar as perguntas finais. Quando só houver plano, escrever planejado; quando houver execução, anexar evidência real.

## Consulta

E5·66–70: ambientes protegidos, OIDC, SBOM/proveniência/assinatura, política de canary e plano Terraform. Usar conforme dúvidas, fora da trilha obrigatória.
