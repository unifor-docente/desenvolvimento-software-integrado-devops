# Exemplo preenchido — release da API de visitas

**Modelo didático**, para adaptar. Os resultados abaixo são os critérios esperados; o registro da execução do professor está em VALIDACAO.md. No projeto da equipe, substituir referências por valores reais e indicar o estado de cada teste.

## Release 2.0.0

**Objetivo:** disponibilizar nova saudação sem mudar o contador ou o schema.

**Artefato:** imagem local `e5-api:v2`. Registrar seu ID com `docker image inspect --format '{{.Id}}' e5-api:v2`. Registrar também o commit real do repositório. Não preencher identificadores fictícios como se fossem provas.

**Configuração:** `APP_IMAGE=e5-api:v2`, `FEATURE_BANNER=true`. Credenciais fictícias permanecem iguais. **Destino:** ensaio local, projeto `unifor-encontro5`, porta 18085. **Estratégia:** recriação da única API; pequena interrupção possível. Banco permanece ativo.

**Critério de promoção:** imagem identificada; smoke da candidata validado em ambiente de teste; `GET /mensagem` deve ser `Bem-vindos à nova experiência!`; `GET /version` deve indicar `2.0.0`; readiness e leitura de visitas devem passar. Avaliação de segurança registrada, sem exceção implícita.

**Mudança e risco:** ativação da mensagem nova. Falha no conteúdo pode ocorrer mesmo com HTTP 200. Mitigação inicial: flag false; alternativa: imagem anterior compatível. Não há migração de schema neste ensaio.

## Recuperação acionável

**Gatilho:** o smoke encontra mensagem diferente da esperada depois da promoção. **Decisão:** responsável pelo release da equipe interrompe a progressão e registra versão, sintoma e teste. **Evidência a preservar:** saída de `/version`, `/mensagem`, estado de app e total do contador; sem divulgar configuração sensível.

**Contenção:** manter a imagem e mudar `FEATURE_BANNER=false`, reaplicar app e verificar o contrato antigo. O recurso novo fica suspenso; a correção continua pendente.

**Rollback:** no diretório do laboratório e no mesmo contexto de projeto:

```sh
export APP_IMAGE=e5-api:v1
export FEATURE_BANNER=false
docker compose up -d --no-deps --no-build --wait app
python3 verificar.py
curl -fsS http://localhost:18085/visitas
```

**Confirmação:** versão 1.0.0; mensagem antiga; readiness e leitura do banco; contador igual ao observado antes, na ausência de novas gravações. Comparar ID da imagem com o registro inicial.

**Se não recuperar:** interromper novas promoções, guardar logs pertinentes, conferir destino e imagem disponível, diagnosticar configuração e dependência. Não remover o volume. Se houver incompatibilidade de schema no projeto real, a equipe deve planejar outro caminho antes da entrega.

**Comunicação no projeto:** registrar impacto, recurso suspenso, responsável, ação e resultado no repositório, pelo canal adotado pela equipe. O laboratório não envia mensagens externas automaticamente.

## Segurança e IA

A conta local é fictícia; não copiar esse padrão para produção. Nenhum segredo real vai para prompts. Se IA sugerir apagar o volume para corrigir a saudação, rejeitar: não há relação causal. O controle efetivo é validar conteúdo, versão e dados após a ação.

**Pendência ilustrativa:** tornar a flag dinâmica pode ser uma evolução, mas não é requisito. **Ensaio:** preencher data, operador e evidências reais; não confundir este texto com log de execução.
