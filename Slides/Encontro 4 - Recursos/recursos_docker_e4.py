"""Recursos do Docker contextualizados na sequência didática do encontro."""
def ampliar(S, slide):
 def depois(key, *ids):
  items=[next(d for d in S if d['id']==i) for i in ids]
  for d in items:S.remove(d)
  pos=next(i for i,d in enumerate(S) if d['id']==key)+1
  S[pos:pos]=items
 slide('resources_map','Mapa dos recursos do Docker','Cada recurso resolve uma necessidade diferente da aplicação',kind='table',headers=['Necessidade','Recurso','Exemplo na aula'],widths=[.28,.32,.40],rows=[
 ['Empacotar e distribuir','Imagens, build e registry','API com Node e dependências.'],
 ['Executar e controlar','Containers e ciclo de vida','Criar, iniciar, parar e remover.'],
 ['Conectar e guardar','Redes, portas e volumes','API acessa db; contador persiste.'],
 ['Observar e restringir','Logs, inspect, stats e limites','Investigar falhas e consumo.'],
 ['Integrar componentes','Compose e healthchecks','Declarar e verificar a aplicação.']],
 note='Apresente o mapa como orientação para o restante da aula. Os recursos serão retomados quando houver um problema concreto: dados ao integrar o banco, logs ao diagnosticar, limites ao discutir consumo. Docker também oferece recursos de construção avançada e integração com ferramentas de desenvolvimento; eles estão na consulta. Não é preciso memorizar todas as opções da CLI para entender as responsabilidades. A equipe deve justificar os recursos que realmente utiliza.',takeaway='Escolha o recurso pelo problema: imagem não guarda o banco; volume não publica uma porta.')
 depois('limits','resources_map')
 slide('observe','Observar e executar comandos em uma instância','Aplicar enquanto e4-primeiro está em execução, antes de removê-lo',kind='table',headers=['Comando','O que faz / resultado esperado'],widths=[.55,.45],rows=[
 ['docker logs --tail=20 e4-primeiro','Mostra stdout/stderr; sem log no código, pode ficar vazio.'],
 ['docker exec e4-primeiro node --version','Inicia outro processo na mesma instância; imprime 22.x.'],
 ['docker inspect --format \'{{.State.Status}}\' e4-primeiro','Consulta metadados; neste momento: running.'],
 ['docker stats --no-stream e4-primeiro','Mostra uma amostra de CPU, memória e I/O.']],
 note='Execute antes da parada e remoção. exec não cria uma nova instância da imagem: inicia um comando dentro do container existente, que precisa estar ativo. inspect consulta o objeto gerenciado e funciona também para uma instância parada; selecione apenas o campo necessário. O servidor inicial não emite logs de requisições, portanto logs vazio não é falha do Docker. stats ajuda a observar consumo, mas não substitui histórico e alertas. Comandos de inspeção não corrigem o problema por si só.',takeaway='logs mostra o que foi emitido; inspect mostra configuração/estado; exec executa; stats mede consumo.',section='Primeira execução')
 depois('demo_http','observe')
 slide('image_commands','Recursos de imagem: construir, obter e identificar','Comandos de consulta depois do build de e4-api:local',kind='table',headers=['Operação','Comando / efeito'],widths=[.25,.75],rows=[
 ['Construir','docker build -t e4-api:local . → produz a imagem do projeto.'],
 ['Obter','docker pull node:22-bookworm-slim → obtém a imagem-base.'],
 ['Listar','docker image ls → mostra referências locais.'],
 ['Examinar','docker image history e4-api:local → histórico de construção.'],
 ['Dar outra tag','docker tag e4-api:local e4-api:revisao → outra referência local.']],
 note='Diferencie obter uma imagem pronta de construir a própria. Uma tag adicional não reconstrói o conteúdo nem inicia um container. O histórico ajuda a examinar etapas e metadados, mas não é um inventário completo de vulnerabilidades. A operação push publica em um registry autorizado e exige uma referência e permissão adequadas; fica explicada na consulta, sem publicação em contas reais nesta demonstração. A equipe deve saber identificar qual imagem originou a execução testada.',takeaway='build produz; pull obtém; tag referencia; push distribui; run cria uma instância.',section='Empacotamento')
 depois('build_demo','image_commands')
 slide('resource_limits','Limites de CPU e memória: controlar o consumo','Exemplo de configuração adicional do serviço app • valores ilustrativos',kind='code',code='services:\n  app:\n    # Junto dos demais campos do serviço\n    cpus: 0.50\n    mem_limit: 256m\n\n# Observar depois de aplicar a configuração:\n# docker compose stats --no-stream',cards=[
 ('CPU','0.50 limita o tempo de CPU ao equivalente a meia CPU.\nNão reserva um núcleo exclusivo.'),
 ('Memória','256m limita memória.\nUso excessivo pode levar a encerramento por OOM.')],
 note='Sem limites configurados, não presuma uma divisão automática justa por container. Os valores ilustram a sintaxe; devem ser medidos para a aplicação real. A CPU pode sofrer throttling ao atingir a quota. Para memória, swap depende de configuração adicional e do host, e não deve ser ignorada no dimensionamento. O laboratório básico não exige provocar falta de memória. Compare a configuração declarada com uma amostra de consumo e explique que uma única amostra não revela todos os picos.',takeaway='Medir → definir limite → testar carga e comportamento; copiar números não é dimensionar.',section='Integração')
 slide('restart_policy','Políticas de reinício: reagir à saída do processo','No Compose: restart: unless-stopped • escolha conforme a finalidade',kind='table',headers=['Política','Comportamento principal'],widths=[.29,.71],rows=[
 ['"no" (padrão)','Não reinicia automaticamente.'],
 ['on-failure[:N]','Reinicia após saída com erro; N pode limitar tentativas.'],
 ['always','Reinicia após saída; parada manual suspende até nova partida do daemon ou do container.'],
 ['unless-stopped','Semelhante a always; preserva a intenção de parada manual mesmo após reinício do daemon.']],
 note='A política observa o encerramento do processo. Um container unhealthy com o processo vivo não é automaticamente reiniciado por essa configuração. on-failure não equivale a inicializar automaticamente após reinício do daemon. Distinguir uma aplicação de longa duração de um job que deve terminar evita reinícios indesejados. As políticas não corrigem senha, schema ou hostname incorretos, e reiniciar repetidamente pode esconder o sintoma. O exemplo é explicativo: a API de laboratório não precisa receber uma política nova para cumprir seu objetivo.',takeaway='Restart não é healthcheck, não recupera dados perdidos e não oferece alta disponibilidade entre hosts.',section='Integração')
 depois('depends','resource_limits','restart_policy')
 slide('security','Recursos para reduzir acesso desnecessário','Configurar de acordo com o que o processo realmente precisa',cards=[
 ('Usuário e escrita','USER node no Dockerfile.\nBind mount :ro para init.sql.\nread_only pode restringir o filesystem da instância.'),
 ('Segredos e privilégios','Não colocar senhas reais na imagem.\nCompose secrets entrega arquivos aos serviços autorizados.\nA aplicação precisa lê-los.'),
 ('Aplicação ao projeto','Declarar diretórios graváveis.\nEvitar privileged sem necessidade.\nLimitar portas e redes expostas.')],
 note='Use duas medidas já presentes como ponto de partida: usuário node na API e montagem somente leitura de init.sql. read_only não transforma automaticamente todos os volumes em somente leitura, e aplicações que gravam caches ou temporários precisam de destinos adequados. Secrets no Compose local não equivale a um cofre remoto nem implica criptografia automática do arquivo de origem; controle quem acessa o host e o arquivo. Essas escolhas diminuem acessos desnecessários, mas exigem teste funcional. Não prometa segurança absoluta com uma opção.',takeaway='Permitir somente o necessário exige conhecer os arquivos, conexões e permissões da aplicação.',section='Integração')
 depois('env','security')
 slide('tmpfs','Consulta | Volume, bind mount e tmpfs','Três maneiras de montar arquivos, com finalidades diferentes',kind='table',headers=['Montagem','Quando usar','O que lembrar'],widths=[.25,.38,.37],rows=[
 ['Volume nomeado','Dados que precisam sobreviver à instância.','Precisa de backup; existe fora da camada gravável.'],
 ['Bind mount','Arquivo/diretório específico do host.','Depende de caminho e permissões do host.'],
 ['tmpfs (Linux)','Arquivos temporários durante a execução.','Não persiste após parada; pode haver swap.']],
 note='Um exemplo de sintaxe Compose é tmpfs: /tmp dentro do serviço, útil se a aplicação precisa de temporários numa instância com filesystem somente leitura. Dados de negócio não devem depender dessa montagem. tmpfs usa memória, mas páginas podem ir para swap conforme o host; não prometa que segredos jamais tocarão disco só por estarem ali. O laboratório usa volume para dados e bind mount para inicialização, por isso tmpfs é apresentado como alternativa com propósito distinto.',takeaway='Persistência, compartilhamento com o host e armazenamento temporário são requisitos diferentes.',section='Consulta',study_only=True)
 slide('network_drivers','Consulta | Diferentes modos de rede','O laboratório usa a rede bridge criada pelo Compose',kind='table',headers=['Driver','Finalidade e contexto'],widths=[.26,.74],rows=[
 ['bridge','Conecta containers no mesmo host; redes definidas pelo usuário permitem descoberta por nome.'],
 ['host','Compartilha a pilha de rede do host; comportamento e suporte dependem da plataforma.'],
 ['none','Desativa a conectividade externa da instância; mantém loopback.'],
 ['overlay','Rede entre hosts, com requisitos de Swarm; fora do laboratório.'],
 ['macvlan / ipvlan','Integração especializada com a rede física, exigindo planejamento de endereçamento.']],
 note='Não apresente drivers como uma progressão de qualidade. Bridge atende ao exemplo de dois serviços em um host. Host reduz o isolamento de rede e não exige publicação de portas da mesma forma. Overlay não é o resultado automático de executar Compose em dois notebooks. Macvlan e ipvlan atendem necessidades específicas de infraestrutura e podem ter restrições no ambiente local. No projeto, a primeira decisão é quais serviços precisam se alcançar; trocar de driver sem uma necessidade não corrige um hostname errado.',takeaway='Escolha a topologia necessária antes do driver; uma rede compartilhada não publica sozinha portas no host.',section='Consulta',study_only=True)
 slide('profiles','Consulta | Profiles: serviços opcionais no Compose','Exemplo de ferramenta administrativa que não precisa iniciar sempre',kind='code',code='services:\n  admin:\n    image: adminer:4\n    profiles: ["ferramentas"]\n    ports:\n      - "127.0.0.1:18082:8080"\n\n# Na configuração completa com app e db:\n# docker compose --profile ferramentas up -d',cards=[('Sem o profile','up inicia serviços sem profile.\nadmin fica fora desse conjunto.'),('Com ferramentas','Inclui admin no conjunto.\nO exemplo deve compartilhar a rede do db.')],
 note='O trecho ilustra um serviço adicional, não substitui o compose.yaml existente. App e db continuam sem profile para iniciar normalmente. A imagem e a porta são exemplos e precisam estar disponíveis se a equipe decidir experimentá-los; não há obrigação de baixar a ferramenta. Selecionar explicitamente um serviço na CLI também pode ativar esse serviço com profile. Profiles organizam combinações de serviços, mas não são autorização de acesso nem gestão de segredos.',takeaway='Profiles permitem escolher ferramentas ou tarefas opcionais sem duplicar toda a aplicação.',section='Consulta',study_only=True)
 slide('compose_dev','Consulta | Overrides e Watch no desenvolvimento','Adaptar o ambiente local mantendo a configuração compreensível',cards=[
 ('Overrides','Arquivos adicionais combinam configurações.\nEx.: compose.yaml + compose.dev.yaml.\nRevise o resultado com compose config.'),
 ('Watch','Regras develop.watch podem sincronizar arquivos ou reconstruir a imagem.\nO efeito depende da ação configurada.'),
 ('Limite do recurso','Sincronizar arquivo não garante recarga do processo.\nFramework e comando precisam suportar o fluxo escolhido.')],
 note='Uma execução com arquivos explícitos pode usar docker compose -f compose.yaml -f compose.dev.yaml config para revisar a combinação antes de subir. As regras de merge variam por campo; não presuma que toda lista será substituída. Watch é recurso do plugin Compose e seu suporte depende da versão instalada. Uma mudança de dependência pode exigir rebuild, enquanto uma mudança de código pode usar sync se o processo recarrega. O objetivo é encurtar o ciclo de desenvolvimento sem tornar a configuração final um mistério.',takeaway='Confira a versão do Compose e a configuração resultante; conveniência local não dispensa testar a imagem final.',section='Consulta',study_only=True)
 slide('buildkit','Consulta | BuildKit, Buildx e cache de construção','Construir com eficiência e escolher a plataforma de destino',cards=[
 ('BuildKit','Backend de construção.\nPode reutilizar resultados e usar cache mounts.\nNem todo build será executado do zero.'),
 ('Buildx','Interface para recursos de build.\nPermite escolher builders e plataformas.\nEx.: linux/amd64 ou linux/arm64.'),
 ('Exemplo e cuidado','Uma biblioteca nativa precisa ser compatível com a plataforma final.\nBuild bem-sucedido pede teste de execução.')],
 note='O cache de camadas explicado na trilha principal é o primeiro passo. Cache mounts podem reaproveitar downloads sem colocar esse cache no artefato final. Build secrets evitam fornecer credenciais por ARG ou ENV persistentes, mas ainda exigem que o comando não copie o segredo para a saída. Buildx e BuildKit oferecem capacidades de construção; não devem ser confundidos com o runtime que inicia a aplicação. Uma imagem multiplataforma exige que código, base e dependências funcionem nas plataformas publicadas.',takeaway='Otimizar a construção e controlar a plataforma complementam a reprodução; não substituem testes.',section='Consulta',study_only=True)
 slide('ecosystem','Consulta | Outros recursos do ecossistema','Conhecer o propósito sem exigir todas as ferramentas no projeto',kind='table',headers=['Recurso','Para que serve'],widths=[.30,.70],rows=[
 ['Docker Hub / registry','Distribuição de imagens, tags e controle de acesso.'],
 ['Contexts','Selecionar qual Engine a CLI controla; conferir antes de operar.'],
 ['Docker Scout','Análise de imagens e informações sobre vulnerabilidades.'],
 ['Swarm mode','Orquestração de serviços entre nós; difere do Compose local.'],
 ['Desktop Dashboard','Interface para visualizar e operar recursos do ambiente local.']],
 note='Faça uma passagem pelo mapa sem instalar componentes adicionais. Registry armazena imagens; não executa a aplicação. Context permite apontar comandos para outro Engine, portanto conhecer o destino importa. Uma análise de vulnerabilidades ajuda a priorizar correções, mas depende de dados atualizados e não comprova segurança total. Swarm introduz cluster e estado desejado de serviços, tema além da execução em um host. Algumas capacidades de produtos e planos mudam; consulte a documentação oficial antes de adotá-las.',takeaway='A entrega desta aula usa os recursos necessários ao projeto; conhecer opções não cria novas exigências.',section='Consulta',study_only=True)
