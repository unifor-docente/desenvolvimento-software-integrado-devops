# Validação executada — 23/09/2026

Ensaio real com projeto Compose exclusivo, imagens próprias do teste, porta temporária e dados fictícios.

Projeto: `e5-validacao-0b3d4227`. Porta local: `59581`.

- referência: PASS: prontidão, versão, mensagem e leitura de dados.
- defeito: Falha funcional esperada confirmada.
- contenção: PASS: prontidão, versão, mensagem e leitura de dados.
- rollback: PASS: prontidão, versão, mensagem e leitura de dados.
- correção: PASS: prontidão, versão, mensagem e leitura de dados.
- Contador preservado em 1 durante as trocas, sem novas gravações.
- Container do banco permaneceu o mesmo durante contenção, rollback e correção.
- IDs das três imagens permaneceram iguais durante o ensaio; não houve rebuild na recuperação.
- Projeto de teste encerrado com `down`, sem remoção do volume fictício.

## Identificadores das imagens usadas no teste

- v1: `sha256:369b74b0e5334a2d9f8412e07ebe23f9d67d2dc1f125dfccfd66e322631dfc8a`
- v2-ruim: `sha256:faf1e9fca07d3fff27a8b9dd9db8ff14663e0111288f2d1b27c503fe0289bf2b`
- v2: `sha256:9dbc959562e2d3fcdea4e6660adb87ddb2980f7550f34ca6ee3fe9a25281e57d`

Esses são IDs locais das imagens construídas para a validação, não digests de um registry nem referências a um deploy público. O aluno deve registrar os valores da própria execução.
