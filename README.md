# Desenvolvimento de Software Integrado — DevOps

Material da disciplina **PG2305-04-Z251** (Pós-Graduação, UNIFOR) — Turma 4, Z251, semestre 2026.2.

24h presenciais em 6 encontros (10, 11, 12, 24, 25 e 26/09/2026), com um projeto integrador
construído em equipe ao longo de todo o curso.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| [`Plano de Ensino/`](Plano%20de%20Ensino/) | Documento oficial homologado: ementa, objetivos, avaliação, bibliografia |
| [`Slides/`](Slides/) | Slides de aula, guia de condução e apostila de estudo do professor |
| [`Práticas/`](Práticas/) | Enunciado do Projeto Integrador entregue às equipes |
| [`Materiais de apoio/`](Materiais%20de%20apoio/) | Leituras complementares (NIST AI RMF, OWASP GenAI LLM Top 10, artigos) |

## Os três materiais de aula, e a diferença entre eles

- **`...Slides.pptx`** — projetado em sala para os alunos.
- **`...Guia de Aula.pptx`** — roteiro de condução do professor (blocos de tempo, checklists).
- **`...Guia de Aula.docx`** — apostila de estudo do professor: explicação aprofundada de cada
  tópico, exemplos comentados e vídeo-aulas recomendadas para preparo antes de cada encontro.

## Projeto Integrador

Um único projeto evolui incrementalmente a cada encontro (diagnóstico → repositório/PR → pipeline
CI → containers → release/rollback → observabilidade). Regras completas em
[`Práticas/Desenvolvimento de Software Integrado - DevOps - Projeto Integrador (Enunciado).docx`](Práticas/).

## Prática com CodeRabbit

[`Revisão de código com IA`](Práticas/coderabbit/README.md): roteiro e acesso ao [repositório da API](https://github.com/unifor-docente/devops-coderabbit-demo),
com testes automatizados e um PR didático com defeitos para revisar e corrigir.
Roteiro de 45–60 minutos para o Encontro 2.

## Professor

Arimatéia Júnior — [linkedin.com/in/arimateiajunior](https://www.linkedin.com/in/arimateiajunior)

## Encontro 4 — material ampliado

O encontro foi reorganizado em **78 slides de conteúdo + capa**, com fundamentos antes das perguntas,
12 diagramas editáveis, exemplos progressivos, notas do professor e quatro verificações com gabaritos visíveis.
A trilha explica aplicação, runtimes, containers, Docker e Compose antes de comparar VMs e integrar o projeto.
Os recursos do Docker incluem imagens, redes, armazenamento, inspeção, limites, saúde e reinício, além de nove slides de consulta.
A sequência está incorporada aos slides principais (posições 107–185) e aos guias de aula.

- [Apresentação somente do Encontro 4](Slides/Encontro%204%20-%20Recursos/Encontro%204%20-%20Containers%20e%20Compose.pptx)
- [PDF do Encontro 4](Slides/Encontro%204%20-%20Recursos/Encontro%204%20-%20Containers%20e%20Compose.pdf)
- [Guia ampliado do professor](Slides/Encontro%204%20-%20Recursos/Guia%20ampliado%20do%20professor.md)
- [Laboratório API + PostgreSQL e falhas guiadas](Práticas/encontro-4-containers/README.md)

O roteiro mantém quatro horas, incluindo intervalo e 70 minutos de prática nos projetos das equipes.

Na revisão de 22/09, as verificações passaram a suceder a base conceitual e a demonstração; cada uma tem gabarito explicado no slide seguinte.
Consulte o [índice de perguntas e respostas](Slides/Encontro%204%20-%20Recursos/Índice%20de%20perguntas%20e%20respostas.md) e o [roteiro de condução](Slides/Encontro%204%20-%20Recursos/Roteiro%20de%20condução%20-%204%20horas.md).

- [Primeiros containers: demonstração introdutória](Práticas/encontro-4-containers/PRIMEIROS-PASSOS.md)
- [Mapa dos recursos do Docker](Slides/Encontro%204%20-%20Recursos/Mapa%20dos%20recursos%20do%20Docker.md)

## Encontro 5 — entrega e governança

Capítulo reestruturado com **70 slides de conteúdo + capa**, fundamentos antes das perguntas,
15 diagramas, seis verificações com gabaritos, exemplos preenchidos e demonstração local de contenção e rollback.
E5 ocupa as posições **186–256** dos slides principais. A apostila e o guia PowerPoint também foram atualizados.

- [PowerPoint do Encontro 5](Slides/Encontro%205%20-%20Recursos/Encontro%205%20-%20Entrega%20e%20Governança.pptx)
- [PDF do Encontro 5](Slides/Encontro%205%20-%20Recursos/Encontro%205%20-%20Entrega%20e%20Governança.pdf)
- [Guia ampliado do professor](Slides/Encontro%205%20-%20Recursos/Guia%20ampliado%20do%20professor.md)
- [Roteiro de quatro horas](Slides/Encontro%205%20-%20Recursos/Roteiro%20de%20condução%20-%204%20horas.md)
- [Laboratório e modelos de release/rollback](Práticas/encontro-5-entrega/README.md)

O roteiro reserva 70 minutos ao projeto das equipes. Mantém os 15% de Entrega e Operação da rubrica oficial,
sem exigir nuvem, publicação externa ou uma ferramenta específica.


## Encontro 6 — observabilidade e projeto final

Módulo reestruturado com capa e 59 slides de conteúdo: fundamentos antes das perguntas, logs/métricas/traces, indicadores e objetivos, incidente guiado, IA aplicada e apresentação final. Inclui 15 questões com respostas comentadas, notas do professor e quatro slides de consulta. A prática compara antes/durante/depois de uma falha local e preserva os dados.

- [PowerPoint do Encontro 6](Slides/Encontro%206%20-%20Recursos/Encontro%206%20-%20Observabilidade%20e%20Projeto%20Final.pptx)
- [PDF do Encontro 6](Slides/Encontro%206%20-%20Recursos/Encontro%206%20-%20Observabilidade%20e%20Projeto%20Final.pdf)
- [Guia e roteiro do professor](Slides/Encontro%206%20-%20Recursos/README.md)
- [Laboratório de observabilidade](Práticas/encontro-6-observabilidade/README.md)
