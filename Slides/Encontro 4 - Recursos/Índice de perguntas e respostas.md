# Verificações e respostas comentadas

As quatro verificações aparecem depois da explicação e da demonstração de seus blocos. Cada uma tem três situações, seguidas de um slide com respostas explicadas. Os casos de diagnóstico também mostram sintoma, causa, correção e prova.

Use o rodapé E4·NN. A página no PDF independente corresponde ao número + 1, devido à capa.

| Questões | Gabarito | Bloco |
|---|---|---|
| E4·23 | E4·24 | Verificação | Componentes e responsabilidades |
| E4·34 | E4·35 | Verificação | Imagem e execução |
| E4·52 | E4·53 | Verificação | Rede, dados e saúde |
| E4·66 | E4·67 | Verificação final | Explicar o próprio projeto |

## Verificação | Componentes e responsabilidades

**Pergunta:** Em node server.js dentro de um container, qual é o papel de Node e qual é o papel do runtime de containers?

**Resposta explicada:** Node executa o JavaScript. O runtime de containers prepara o isolamento e inicia o processo nesse ambiente. São camadas diferentes.

**Pergunta:** Duas instâncias criadas da mesma imagem são o mesmo container?

**Resposta explicada:** Não. Compartilham a origem, mas possuem identidade, configuração e estado de instância próprios.

**Pergunta:** Compose instala um kernel e executa o JavaScript da aplicação?

**Resposta explicada:** Não. Compose declara e coordena serviços usando o Engine. O processo usa seu runtime de linguagem e o kernel do host Linux.


## Verificação | Imagem e execução

**Pergunta:** Trocar RUN npm ci por CMD npm ci mantém o mesmo comportamento?

**Resposta explicada:** Não. RUN instala durante o build; CMD executaria a instalação na partida, no lugar do comando principal esperado.

**Pergunta:** Alterar server.js depois da cópia dos manifests precisa invalidar npm ci em todo build?

**Resposta explicada:** Não necessariamente. A instalação pode usar cache se suas entradas e a base continuam válidas. O código foi copiado depois.

**Pergunta:** Se live retorna 200 e ready retorna 503 nesta execução isolada, o que já foi comprovado?

**Resposta explicada:** O processo HTTP responde. A consulta de prontidão não passou; sem o banco integrado, ainda não há prova da funcionalidade de visitas.


## Verificação | Rede, dados e saúde

**Pergunta:** A porta do host muda para 9090. A API deve passar a usar db:9090?

**Resposta explicada:** Não. 9090 é a entrada do cliente na API. A conexão interna com o banco continua db:5432.

**Pergunta:** Depois de down/up sem -v, o total permanece. Isso prova que há backup?

**Resposta explicada:** Não. Prova persistência no volume reutilizado. Backup requer uma cópia recuperável e restauração testada.

**Pergunta:** O check SELECT 1 passa, mas a tabela contador não existe. /visitas está garantido?

**Resposta explicada:** Não. A consulta básica pode passar enquanto a operação falha por schema ausente. Teste GET/POST /visitas.


## Verificação final | Explicar o próprio projeto

**Pergunta:** Ao apresentar o projeto, como distinguir imagem, container e os dois sentidos de runtime?

**Resposta explicada:** Imagem: artefato. Container: instância. Runtime da linguagem executa o código; runtime de containers prepara e inicia processos isolados.

**Pergunta:** Como provar que sua aplicação está integrada à dependência, além de mostrar o container Up?

**Resposta explicada:** Executar uma operação funcional com resultado esperado; verificar saúde e persistência conforme o contrato do projeto.

**Pergunta:** Qual evidência liga uma alteração de configuração à correção de uma falha?

**Resposta explicada:** Sintoma reproduzido, hipótese testada, mudança específica e repetição do mesmo teste com resultado corrigido.

## Atividade no projeto

O plano técnico pede decisões da própria equipe. Não há uma única stack correta: as decisões devem corresponder ao projeto e à execução. O slide “Traduzir o exemplo para a aplicação da equipe” mostra o mapeamento e “Exemplo preenchido: evidência de uma falha corrigida” oferece um modelo resolvido.
