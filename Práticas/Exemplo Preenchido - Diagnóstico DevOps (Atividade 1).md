<!--
NOTA PARA O PROFESSOR (não faz parte do exemplo — pode apagar esta caixa antes de projetar):

Cenário fictício, criado só para calibrar o nível de detalhe esperado. Não é baseado em
nenhuma empresa real. Sugestão de uso em sala: deixe os grupos tentarem sozinhos primeiro
(passos 1-3 da Atividade 1) e só mostre este exemplo no fechamento, como comparação — se
mostrar antes, os grupos tendem a copiar a estrutura em vez de pensar no próprio fluxo
(efeito de ancoragem). Bom também para mostrar o que NÃO conta como gargalo específico o
suficiente: "sistema lento" é vago; "deploy manual via FTP direto em produção, sem revisão"
é um gargalo de verdade porque já aponta pra uma causa e uma automação possível.
-->

# Diagnóstico DevOps

**Projeto/grupo:** Exemplo ilustrativo — Relatório de Vendas Interno (cenário fictício, só para referência)

## Fluxo atual

1. **Pedido/demanda** — o time de atendimento recebe o pedido "criar relatório de vendas mensal" por mensagem no WhatsApp do gestor, sem registro formal.
2. **Desenvolvimento** — um desenvolvedor pega a tarefa e mexe direto na branch `main` do repositório, sem abrir Pull Request.
3. **Teste** — o teste é manual, feito só na máquina do próprio desenvolvedor; não existe teste automatizado.
4. **Entrega** — o arquivo/script atualizado é copiado direto para o servidor de produção via FTP, geralmente numa sexta-feira à tarde.
5. **Operação** — ninguém monitora se algo quebrou; o problema só é percebido quando um usuário reclama no grupo do WhatsApp, muitas vezes já na segunda-feira seguinte.

## Gargalos

- **Gargalo 1 — Deploy manual sem pipeline nem revisão.** Qualquer erro de digitação vira incidente em produção sem ninguém perceber antes.
- **Gargalo 2 — Nenhum teste automatizado.** Bugs só aparecem depois que o cliente já viu, nunca antes do deploy.
- **Gargalo 3 — Nenhuma rastreabilidade.** Ninguém sabe o que mudou entre uma versão e outra, nem quem fez o quê.

# Priorização

**Melhoria escolhida:** Implementar um pipeline de CI simples que roda testes automatizados a cada push e bloqueia o deploy se algo quebrar, junto com um fluxo mínimo de Pull Request antes de qualquer alteração ir para produção.

**Impacto esperado:** Sair de "descobrimos o bug quando o cliente reclama" para "descobrimos o bug antes mesmo de fazer o deploy".

**Evidência de sucesso:** Pipeline rodando no repositório, com histórico mostrando pelo menos uma vez em que ele bloqueou um erro antes de chegar em produção.

**Riscos:** O time pode resistir à mudança por achar que "vai atrasar" a entrega no curto prazo; escrever os primeiros testes exige um tempo que a equipe não está acostumada a reservar.

**IA pode ajudar em:** Gerar os primeiros casos de teste a partir do código já existente, e sugerir hipóteses de correção quando o pipeline falhar.

**Validação humana necessária:** Toda sugestão de teste gerada por IA precisa ser revisada por alguém do time antes de entrar no pipeline — a IA não decide sozinha o que é um teste válido.
