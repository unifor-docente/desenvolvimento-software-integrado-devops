# Desenvolvimento de Software Integrado — DevOps (PG2305-04-Z251)

Este diretório reúne todo o material de uma disciplina de pós-graduação lato sensu (UNIFOR) que
o usuário leciona. Não é um repositório de código — é material didático (Word, PowerPoint, PDF).
Não há controle de versão (git) neste diretório.

## Identificação

- **Disciplina:** Desenvolvimento de Software Integrado — DevOps
- **Código:** PG2305-04-Z251 | **Turma:** 4 — Z251 | **Centro:** CCT
- **Carga horária:** 24h presenciais, em 6 encontros de 4h
- **Datas:** 10, 11, 12, 24, 25 e 26/09/2026 (semestre 2026.2)
- **Professor:** Arimatéia Júnior (arquiteto de software/soluções, +15 anos em TI — Infra, Cloud,
  DevOps, Arquitetura; certificações Microsoft, AWS, GCP, Oracle, GitHub, VMware)
- **Pré-requisito da turma:** conhecimentos básicos de dev, Git/linha de comando, APIs, redes,
  containers e noções de ambientes de execução.

## Estrutura de pastas

- **`Plano de Ensino/`** — documento oficial homologado (`plano-de-ensino-PG2305-04-Z251.docx/pdf`).
  É a **fonte de verdade** para ementa, objetivos, conteúdo por unidade, metodologia, pesos de
  avaliação (6 critérios) e bibliografia. Qualquer material novo deve ser consistente com este
  documento — os pesos de avaliação (25/25/20/15/10/5%) **não podem ser alterados** sem passar
  por homologação institucional; ajustes de como aplicá-los (ex.: mecanismo de nota individual)
  devem ser feitos como regra operacional por cima, sem reescrever os percentuais oficiais.
- **`Slides/`** — três materiais de apresentação/estudo:
  - `...Slides.pptx` — material projetado em sala para os **alunos** (94 slides, bullets curtos).
  - `...Guia de Aula.pptx` — roteiro de condução em sala para o **professor** (60 slides, blocos
    de tempo, checklists). Mais antigo que a apostila abaixo; mantido, mas parcialmente
    redundante com ela.
  - `...Guia de Aula.docx` — a **apostila de estudo do professor** (52-53 páginas). Diferente dos
    dois `.pptx` acima: não é para projetar, é para o professor estudar antes de cada encontro.
    Tem explicação aprofundada de cada conceito (além do que cabe num slide), exemplos comentados,
    trechos de código, e um índice de ~31 vídeo-aulas reais do YouTube (curadas por busca, PT-BR
    priorizado) organizadas por encontro. Estrutura: Parte 1-2 fundamentos transversais (DevOps,
    CALMS, DORA, IA no SDLC), Partes 3-8 um capítulo por encontro, Parte 9 projeto integrador,
    Parte 10 anexos/templates/comandos/bibliografia.
- **`Práticas/`** — materiais **entregáveis aos alunos** para a parte prática:
  - `...Projeto Integrador (Enunciado).docx` — regulamento oficial do projeto integrador entregue
    aos alunos no Encontro 1 (ver seção própria abaixo).
- **`Materiais de apoio/`** — PDFs de referência citados na disciplina (NIST AI RMF 1.0, OWASP
  GenAI LLM Top 10 2026, artigos de introdução a DevOps) + logos/fotos institucionais.

## Como os `.docx` foram gerados

A apostila e o enunciado do projeto foram gerados via scripts Python com `python-docx` (estilo
visual consistente: título navy `#1B2A4A`, destaques azuis `#2A5C8A`, blocos de dica com borda
esquerda, blocos de código com fundo cinza, tabelas com header navy). Os scripts viviam em um
diretório de scratchpad de sessão (efêmero) e não foram versionados neste diretório — se for
preciso regenerar ou editar esses documentos de forma extensa (não só um parágrafo pontual), a
abordagem mais confiável é recriar um script similar com `python-docx` em vez de editar o XML do
`.docx` manualmente. Para edições pequenas e localizadas, editar o `.docx` diretamente é viável.

## Estrutura da disciplina (6 encontros)

| Encontro | Data | Foco |
|---|---|---|
| E1 | 10/09 | Cultura DevOps, IA no SDLC, diagnóstico inicial |
| E2 | 11/09 | Git, colaboração, PR, qualidade, IA assistida |
| E3 | 12/09 | CI, testes automatizados, IA para automação |
| E4 | 24/09 | Containers, Docker Compose, troubleshooting |
| E5 | 25/09 | CD, configuração, segurança, governança de IA |
| E6 | 26/09 | Observabilidade, IA aplicada, projeto final |

Um único **projeto integrador**, feito em equipe, evolui incrementalmente ao longo dos 6
encontros — não existe "trabalho final" separado.

## Avaliação (definida no Plano de Ensino — pesos fixos)

| Peso | Critério |
|---|---|
| 25% | Projeto funcional |
| 25% | Pipeline CI |
| 20% | Containers/Compose |
| 15% | Entrega e operação |
| 10% | Diagnóstico DevOps |
| 5% | Apresentação final |

**Decisão operacional (definida com o usuário, não está no Plano de Ensino):** a nota desses 6
critérios é **inteiramente de grupo** — todos os integrantes de uma equipe recebem a mesma nota.
Não existe arguição oral individual nem mecanismo formal de nota individual embutido na rubrica.
A diferenciação entre alunos de uma mesma equipe fica a critério da observação direta do
professor ao longo dos encontros (avaliação diária informal) e da apresentação final assistida
por ele no Encontro 6 — não é algo a formalizar em documento, é julgamento do professor.

Rubrica de correção usada (mesma escala para os 6 critérios, aplicada no Encontro 6 sobre o
estado final do repositório): Ótimo 9-10, Bom 7-8, Regular 5-6, Insuficiente 0-4.

## Projeto Integrador — regras fechadas

- **Equipes:** formação livre pelos alunos, 4 a 5 integrantes, decidido nos primeiros minutos do
  Encontro 1. Grupos fora dessa faixa se reorganizam na hora.
- **Aplicação:** escolha livre da equipe (não há catálogo de apps prontas do professor). Critérios:
  pequena mas realista, com build/teste/execução local, idealmente API + banco/dependência
  externa. Precisa estar fechada até o fim do Encontro 1.
- **Entregável por encontro** (tabela completa está na Parte 9.3 da apostila e na seção 3 do
  Enunciado): cada encontro tem um critério de aceite objetivo que alimenta um dos 6 pesos acima
  — ex. E3 alimenta os 25% de Pipeline CI, E4 alimenta os 20% de Containers/Compose, etc.
- **Submissão:** um único link de repositório por equipe, toda evidência mora nele (nada se
  avalia fora do repositório), prazo até o fim do Encontro 6.

## Convenções de conteúdo já estabelecidas

- Tom didático em português (pt-BR), alinhado ao Plano de Ensino.
- Regra de IA citada em vários materiais: "toda saída de IA é hipótese até ser validada por
  teste, execução ou revisão humana" — repetir essa frase é intencional, é o mantra da disciplina.
- Vídeos do YouTube recomendados nunca são inventados — sempre buscados e confirmados via busca
  antes de citar, priorizando PT-BR com fallback em inglês para tópicos mais avançados
  (DORA, SRE, OWASP LLM Top 10, NIST AI RMF).
- GitHub Flow é o modelo de branching adotado na disciplina (não GitFlow nem trunk-based) —
  justificado pelo tamanho pequeno das equipes e tempo curto de curso.

## Em aberto / não decidido ainda

- Regras de formação de equipe e escolha de aplicação valem para a matrícula real da turma
  (entre 20 e 30 alunos estimados) — pode precisar ajuste fino quando o número exato de alunos
  matriculados for confirmado.
- O Guia de Aula em `.pptx` (roteiro de condução) não foi atualizado/removido — decidir depois se
  ele deve continuar existindo ao lado da apostila `.docx` ou ser descontinuado.
