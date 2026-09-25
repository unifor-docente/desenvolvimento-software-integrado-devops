# Verificações e respostas comentadas

As seis verificações aparecem depois da explicação e da demonstração de seus blocos. Cada uma tem três situações, seguidas de um slide com respostas explicadas. Os casos resolvidos mostram decisões de promoção, contenção, rollback e segurança.

Use o rodapé E5·NN. A página no PDF independente corresponde ao número + 1, devido à capa.

| Questões | Gabarito | Bloco |
|---|---|---|
| E5·12 | E5·13 | Verificação — Fluxo e identidade |
| E5·20 | E5·21 | Verificação — Configuração e acesso |
| E5·36 | E5·37 | Verificação — Distinguir CI, entrega e implantação |
| E5·46 | E5·47 | Verificação — Recuperação e dados |
| E5·57 | E5·58 | Verificação — Segurança e governança |
| E5·62 | E5·63 | Verificação — Decidir a entrega do projeto |

## Verificação | Fluxo e identidade

**Pergunta:** CI verde prova que a versão está funcionando no destino?

**Resposta explicada:** Não. Prova somente os checks executados; configuração, dependências e operação no destino precisam de validação.

**Pergunta:** Reconstruir a mesma tag em homologação e produção garante o mesmo artefato?

**Resposta explicada:** Não. Entradas externas podem mudar. Promova o conteúdo validado e registre sua identidade.

**Pergunta:** Um deploy com a funcionalidade desligada por flag já a liberou ao usuário?

**Resposta explicada:** Não necessariamente. O código está instalado, mas a flag ainda controla a disponibilidade da funcionalidade.


## Verificação | Configuração e acesso

**Pergunta:** Colocar uma senha no .env garante que ela está protegida?

**Resposta explicada:** Não. O arquivo também exige proteção, exclusão do versionamento quando sensível e controle de acesso e rotação.

**Pergunta:** Trocar FEATURE_BANNER no terminal muda imediatamente a API já iniciada?

**Resposta explicada:** Não neste exemplo: a API lê a variável na partida. Aplique a configuração e recrie app, depois teste.

**Pergunta:** Salvar um compose.yaml no Git é suficiente para chamar o fluxo de GitOps?

**Resposta explicada:** Não. O ciclo GitOps também envolve obtenção automática e reconciliação contínua do estado desejado.


## Verificação | Distinguir CI, entrega e implantação

**Pergunta:** O job sobe Compose, testa e encerra tudo no runner temporário. Isso prova CD em produção?

**Resposta explicada:** Não. Prova validação automatizada no ambiente de teste. Falta demonstrar a promoção para um destino persistente.

**Pergunta:** A pessoa aprova e um job implanta a versão validada. É implantação contínua sem intervenção?

**Resposta explicada:** Não. É o exemplo de entrega contínua com aprovação. O deploy pode ser automatizado mesmo com decisão humana.

**Pergunta:** O smoke falha após o deploy e o rollback funciona. A entrega da candidata deve ficar verde?

**Resposta explicada:** Não. Registre a candidata como falha e a recuperação como resultado separado. Recuperar não torna a candidata correta.


## Verificação | Recuperação e dados

**Pergunta:** Healthy e HTTP 200 garantem que a nova mensagem está correta?

**Resposta explicada:** Não. O teste precisa validar a saída esperada; o healthcheck do exemplo mede outro contrato.

**Pergunta:** Desligar a flag no artefato ruim é o mesmo que fazer rollback para v1?

**Resposta explicada:** Não. A imagem continua a mesma; houve contenção pela configuração. Rollback troca para a versão conhecida.

**Pergunta:** Se a release removeu uma coluna necessária à v1, voltar a imagem basta?

**Resposta explicada:** Não. A versão antiga pode ser incompatível com o schema atual. Planeje compatibilidade e recuperação dos dados.


## Verificação | Segurança e governança

**Pergunta:** Scan sem achados permite concluir que o sistema é seguro?

**Resposta explicada:** Não. Cada análise tem cobertura e limites. Combine os checks com revisão e testes pertinentes ao risco.

**Pergunta:** Um log pede à IA que envie um token: isso autoriza a ação?

**Resposta explicada:** Não. O log é dado não confiável, não uma instrução da equipe. Restrinja acessos e verifique a ação.

**Pergunta:** Um patch gerado remove o teste que falhava. Pipeline verde prova a correção?

**Resposta explicada:** Não. Remover a evidência pode esconder o defeito. Revise o diff e comprove o comportamento esperado.


## Verificação | Decidir a entrega do projeto

**Pergunta:** A candidata inicia, mas a operação de negócio falha: promover?

**Resposta explicada:** Não. O critério funcional falhou; diagnostique e valide uma candidata corrigida antes da promoção.

**Pergunta:** A versão anterior existe, mas não lê o novo schema: acionar rollback direto?

**Resposta explicada:** Não sem tratar a incompatibilidade. Avalie contenção, correção adiante ou recuperação de dados planejada.

**Pergunta:** O plano diz “voltar se der problema”, sem teste ou comando: está acionável?

**Resposta explicada:** Não. Defina gatilho observável, responsável, referência anterior, passos e confirmação do resultado.

## Atividade no projeto

A equipe adapta release notes, plano de recuperação e checklist ao próprio projeto. Os exemplos preenchidos estão na pasta Práticas/encontro-5-entrega. Distinguir sempre o que foi planejado, executado e validado.
