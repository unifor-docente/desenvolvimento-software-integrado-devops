# Relato de incidente — preencher com evidências reais

- Equipe, projeto, commit/versão e ambiente:
- Operação e contrato de resultado bom:
- Janela observada e fuso horário:
- Sintoma e impacto (numerador, denominador, unidade):
- Linha do tempo: início, detecção, intervenção e recuperação:
- Evidências antes/durante/depois (links, comandos e resultados):
- Hipótese inicial e hipótese alternativa:
- Teste que confirma ou refuta cada hipótese:
- Causa sustentada pelas evidências; o que segue incerto:
- Recuperação executada e validação funcional/dos dados:
- Sugestão de IA, se houve; revisão, aceitação/rejeição e teste:
- Ação preventiva, responsável, prazo e critério de conclusão:

Não substituir lacunas por resultados inventados. Diferenciar teste planejado, executado e validado.

## Exemplo didático preenchido (não é a execução da equipe)

Operação: GET /visitas no laboratório local. Resultado bom: 200 e total inteiro. Antes: 10/10 boas. Durante: 0/5 boas, 503, db parado. Causa induzida: comando deliberado `docker compose stop db`. Recuperação: `start db`, prontidão e repetição da sonda; depois 10/10 boas e contador N preservado. Evidências a anexar: três arquivos JSONL, estado do Compose e logs com IDs. Ação preventiva: equipe documenta no runbook como distinguir processo vivo de dependência indisponível, até a entrega final. Verificação da ação: outra pessoa consegue executar e interpretar o ensaio seguindo o runbook. Este exemplo não comprova disponibilidade de produção nem explica uma parada espontânea do banco.
