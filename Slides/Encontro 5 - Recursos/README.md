# Encontro 5 — entrega, configuração, segurança e governança de IA

Reestruturado em 23/09/2026: **60 slides de conteúdo + capa institucional**, com 55 na trilha principal, 5 consultas, 11 diagramas editáveis e cinco verificações (15 situações) com gabaritos no slide seguinte.

A sequência explica os termos antes das perguntas: CI/CD, artefatos, ambientes e gates; configuração, segredos, IaC e GitOps; estratégias de deploy, flags e recuperação; demonstração; DevSecOps e governança de IA; aplicação ao projeto.

## Arquivos

- **Encontro 5 - Entrega e Governança.pptx / .pdf:** apresentação independente, com notas do professor no PowerPoint.
- **Guia ampliado do professor.md:** conceitos, exemplos, tabelas e explicações por slide.
- **Guia de Aula completo - atualizado.pdf:** apostila completa, com sumário e capítulo E5 atualizados.
- **Roteiro de condução - 4 horas.md:** tempo e sugestões de condução, com 70 minutos no projeto.
- **Índice de perguntas e respostas.md:** localiza as cinco verificações e transcreve os gabaritos.
- **conteudo_e5.py / conteudo.json:** fonte didática e conteúdo estruturado.
- **gerar_encontro5.py:** atualiza somente E5 nos slides principais, no guia PowerPoint e na apostila. Requer Python 3, python-pptx, python-docx e Pillow; PDFs são exportados separadamente. Regenerar substitui edições manuais dentro da seção E5.

A apresentação principal contém E5 nas posições **186–246**. O identificador de rodapé E5·NN corresponde à página NN + 1 do PDF independente. O guia PowerPoint é uma seleção que mantém esses identificadores.

## Laboratório e modelos

[Práticas/encontro-5-entrega](../../Práticas/encontro-5-entrega/README.md): imagens v1, v2-ruim e v2; API + banco; smoke funcional; contenção por flag; rollback e correção. Inclui templates e exemplo preenchido de release, recuperação, segurança e uso de IA.

A execução é local e usa dados fictícios. Os diagramas de rolling, blue-green e canary são conceituais, não estratégias implementadas automaticamente pelo Compose do laboratório. A prática não exige nuvem nem publicação externa.

O plano do próprio projeto alimenta os **15% de Entrega e Operação**, mantendo a rubrica oficial e a avaliação de grupo.
