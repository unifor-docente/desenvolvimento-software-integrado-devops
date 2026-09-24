# Validação do laboratório

Executada em 21/09/2026 com Docker Engine 29.8.1 e Compose v5.5.1.
Porta temporária 18084, pois 8080 já estava ocupada no host. Arquivo original preservado.

- OK: live/ready 200; POST incrementa e GET confirma banco.
- OK: dados persistem após down/up sem remoção do volume.
- OK: hostname localhost incorreto produz 503 e ECONNREFUSED.
- OK: bind 127.0.0.1 mantém teste interno 200 e impede acesso pelo host.
- OK: banco parado mantém live 200, ready e visitas 503.
- OK: banco recuperado; API e dados recuperam sem reiniciar app.

Recursos criados para a validação foram encerrados e seu volume fictício preservado.

## Novas demonstrações introdutórias — 22/09/2026

Execução em container temporário exclusivo, com porta local atribuída pelo Docker.

- OK: Node `v22.23.2` executado pela imagem `node:22-bookworm-slim`.
- OK: servidor HTTP respondeu `Olá, turma!`.
- OK: `exec` confirmou versão e `inspect` confirmou `running`.
- OK: `logs` vazio coerente com o exemplo sem emissão de logs.
- OK: `stats --no-stream` apresentou consumo; limites de 0,5 CPU e 256 MiB confirmados na configuração.
- OK: stop/start preservou a instância e o servidor voltou a responder.

Somente o container criado para este teste foi parado e removido; nenhum volume foi removido. A imagem usada nesta execução apresentou o digest `sha256:48e4b67d85f87bd551df43704e24d252f56cc5f8e9718841aace50f19948f0f9`.
