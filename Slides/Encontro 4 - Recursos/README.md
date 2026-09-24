# Encontro 4 — fundamentos, recursos do Docker e integração

Apresentação reorganizada em 22/09/2026: **78 slides de conteúdo + capa institucional**, sendo 69 na trilha principal e 9 de consulta. As perguntas aparecem depois das explicações e demonstrações. Há quatro verificações (12 questões) com gabaritos visíveis e três casos de diagnóstico resolvidos.

- **Encontro 4 - Containers e Compose.pptx / .pdf:** apresentação independente, com diagramas editáveis e notas do professor no PowerPoint.
- **Guia ampliado do professor.md:** conteúdo, explicações, exemplos, tabelas e sugestões de fala por slide.
- **Guia de Aula completo - atualizado.pdf:** apostila completa, com o capítulo E4 e sumário atualizados.
- **Roteiro de condução - 4 horas.md:** tempos, sequência, consulta e pontos a enfatizar.
- **Índice de perguntas e respostas.md:** localização das verificações e seus gabaritos completos.
- **Mapa dos recursos do Docker.md:** recurso, finalidade, exemplo e slide correspondente.
- **conteudo.json:** conteúdo estruturado dos 78 slides.

Fontes da geração: `conteudo_e4.py` define a progressão; `recursos_docker_e4.py` integra os recursos do Docker; `gerar_encontro4.py` atualiza a seção E4 nos slides principais, no guia PowerPoint e na apostila Word. Requer Python 3, python-pptx, python-docx e Pillow. Execute apenas para regenerar: edições manuais dentro dessa seção serão substituídas. PDFs são exportados separadamente; atualize o sumário da apostila antes da exportação.

A capa conserva a identidade dos outros encontros. Os desenhos mostram processo, imagem/instância, runtimes, CLI/Engine, Compose, VM/container, cache, rede, armazenamento, saúde, diagnóstico e evolução do projeto. São formas editáveis, com rótulos que apoiam a explicação.

No conjunto principal, o encontro ocupa as posições **107–185**. Os rodapés E4·NN são a referência estável; no PDF independente a página é NN + 1.

## Demonstrações

1. [Primeiros containers: runtime, servidor, inspeção e ciclo de vida](../../Práticas/encontro-4-containers/PRIMEIROS-PASSOS.md).
2. [Laboratório integrado: API, PostgreSQL, persistência e falhas](../../Práticas/encontro-4-containers/README.md).

O exemplo apoia a aprendizagem; as equipes aplicam os conceitos ao próprio projeto integrador. O roteiro mantém quatro horas, 15 minutos de intervalo e 70 minutos de prática.
