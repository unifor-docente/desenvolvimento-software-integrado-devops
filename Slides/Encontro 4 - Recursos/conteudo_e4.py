"""Sequência didática: explicar → mostrar → praticar → verificar → aplicar ao projeto."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'Práticas/encontro-4-containers'
S=[]

def slide(key,title,sub,cards=(),note='',takeaway='',kind='cards',code=None,section='Fundamentos',**extra):
 d=dict(id=key,title=title,sub=sub,cards=list(cards),note=note,takeaway=takeaway,kind=kind,code=code,section=section,role='conceito',question='',answer='',study_only=False)
 d.update(extra);S.append(d);return d

def checkpoint(key,title,questions,answers,section):
 q=slide(key,title,'Verificação do bloco • responda com os conceitos e exemplos que acabamos de estudar',[(f'{i+1}. Situação',q) for i,q in enumerate(questions)],
 'As perguntas aparecem depois das definições e demonstrações. Reserve um minuto para previsões e peça justificativas; em seguida revele o gabarito. Use as respostas para decidir se precisa retomar uma figura ou comando.',
 'Discuta primeiro. O próximo slide traz as respostas comentadas.',section=section,role='pergunta',questions=questions)
 slide(key+'_resposta','Respostas comentadas | '+title.replace('Verificação | ','').replace('Verificação final | ',''),'Gabarito explicado • relacione cada resposta ao exemplo observado',[(f'{i+1}. Resposta',a) for i,a in enumerate(answers)],
 '\n\n'.join(f'Questão {i+1}: {qq}\nResposta e explicação: {aa}' for i,(qq,aa) in enumerate(zip(questions,answers))),
 'Uma resposta completa identifica o componente envolvido e explica a evidência.',section=section,role='resposta',answers=answers,answers_for=key)

slide('percurso','Do programa ao ambiente integrado','Encontro 4 • entender os componentes antes de executar comandos',[
 ('Entender','Aplicação, processo e runtime.\nContainer, imagem e Docker.\nCompose e comparação com VMs.'),
 ('Observar','Executar um container simples.\nConstruir a imagem da API.\nIntegrar API e banco.'),
 ('Aplicar','Diagnosticar uma falha.\nContainerizar o projeto da equipe.\nGuardar evidências para a entrega final.')],
 'Apresente a aula como uma construção de conceitos. Primeiro os alunos precisam reconhecer o que está sendo executado e qual ferramenta assume cada responsabilidade. Só depois entram os comandos, a integração e as questões. O exemplo do professor será uma API de visitas; cada equipe continuará a aplicação escolhida nos encontros anteriores. Não comece pedindo que a turma explique Docker ou descubra uma configuração que ainda não foi ensinada.',
 'Resultado: outra pessoa consegue subir o projeto, testar seu funcionamento e entender sua configuração.')
slide('agenda','Roteiro das quatro horas','Exposição progressiva, demonstração e prática no projeto',[
 ('0–65 min | Base','0–10: objetivo e contexto.\n10–50: conceitos e comparação.\n50–65: primeira demonstração e verificação.'),
 ('65–165 min | Integração','65–95: imagem da API.\n95–110: intervalo.\n110–145: Compose e integração.\n145–165: diagnóstico guiado.'),
 ('165–240 min | Projeto','165–235: laboratório das equipes.\n235–240: fechamento e evidências.\nConsultas ficam disponíveis após a trilha.')],
 'O cronograma soma 240 minutos, incluindo 15 minutos de intervalo e 70 minutos de prática no projeto. Os gabaritos pertencem ao tempo de cada bloco, não são uma segunda aula. Faça uma previsão breve antes de mostrar cada resposta. Há material de consulta após o fechamento para dúvidas sobre digest, multi-stage e verificação em CI. Preserve o laboratório; se a turma avançar devagar, explique as distinções essenciais e deixe exemplos de consulta para estudo posterior.',
 'As verificações vêm depois da explicação; as equipes aplicam os conceitos ao próprio projeto.')
slide('ingredientes','Uma aplicação precisa de mais que o código','Exemplo: uma API de visitas escrita em JavaScript',[
 ('Código e bibliotecas','server.js define as rotas.\nO pacote pg permite consultar PostgreSQL.\nOs arquivos precisam estar disponíveis.'),
 ('Ambiente de execução','Node.js executa o JavaScript.\nBibliotecas do sistema dão suporte.\nO sistema operacional oferece recursos.'),
 ('Configuração e serviços','HOST e DATABASE_URL orientam a execução.\nA API precisa alcançar o banco.\nOs dados precisam de armazenamento.')],
 'Comece pelo problema conhecido: ter o arquivo server.js não significa ter uma aplicação executável. Mostre no repositório o arquivo, o package.json e a variável de conexão. Explique biblioteca como código que a aplicação utiliza, runtime como o ambiente que executa seu programa e banco como outro serviço. Nesta etapa basta reconhecer essas partes; porta, volume e rede terão explicação própria. Evite apresentar container como uma solução que automaticamente corrige código ou credenciais.',
 'A execução depende da combinação código + runtime + dependências + configuração + serviços.')
slide('processo','Programa é arquivo; processo é execução','Ao iniciar o programa, o sistema operacional cria uma atividade em execução',note=
 'Use uma analogia simples: a partitura guardada não produz som; alguém precisa executá-la. O arquivo de programa permanece no disco, enquanto o processo usa CPU, memória e descritores de arquivo. Iniciar o mesmo programa duas vezes pode criar dois processos. Quando o processo termina, o programa continua existindo como arquivo. No nosso exemplo, node server.js cria um processo Node que atende requisições. Um container não muda o fato de que, ao final, existem processos executando.',
 takeaway='Um container em execução terá um processo principal; quando esse processo termina, o container para.',kind='process')
slide('kernel','Sistema operacional: recursos para os processos','Vocabulário mínimo para entender o isolamento',[
 ('Kernel','Núcleo do sistema operacional.\nGerencia CPU, memória, arquivos e rede.\nAtende solicitações dos processos.'),
 ('Espaço de usuário','Aplicações, comandos e bibliotecas.\nNode.js e a API executam aqui.\nUsam serviços oferecidos pelo kernel.'),
 ('Exemplo concreto','A API lê um arquivo e abre uma conexão.\nO processo solicita essas operações.\nO kernel controla os recursos envolvidos.')],
 'Separe kernel de distribuição Linux: uma distribuição também reúne bibliotecas, programas e configuração. Uma imagem Debian ou Alpine pode trazer arquivos de uma distribuição sem iniciar um kernel próprio. Isso prepara a comparação com VMs, que virá depois. Não é necessário detalhar chamadas de sistema; os alunos precisam compreender que aplicações usam recursos gerenciados por uma camada comum. O escopo da aula são containers Linux.',
 'Compartilhar o kernel não significa compartilhar todos os arquivos, processos visíveis ou endereços de rede.')
slide('runtime_app','Runtime da aplicação: quem executa o programa','Runtime é o ambiente necessário para executar o código da aplicação',note=
 'Explique o termo antes de usá-lo em comandos. JavaScript no servidor pode usar Node.js, código Python depende do interpretador e de suas bibliotecas, e bytecode Java usa uma JVM. O runtime da linguagem normalmente é instalado dentro da imagem junto com a aplicação. Uma aplicação Go compilada pode distribuir um binário sem instalar uma VM de linguagem separada; isso não elimina suas necessidades de sistema. A versão do runtime influencia APIs e comportamento, por isso ela faz parte do contrato de execução.',
 takeaway='No laboratório, Node.js é o runtime da API; pg é uma biblioteca; PostgreSQL é outro serviço.',kind='table',
 headers=['Aplicação','Runtime / execução','Exemplo'],widths=[.28,.35,.37],rows=[
 ['JavaScript no servidor','Node.js','node server.js'],['Python','Interpretador Python','python app.py'],['Java','JVM','java -jar app.jar']])
slide('container','Container: processo em um ambiente isolado','Definição operacional para os exemplos desta aula',[
 ('O que é','Uma instância com processos, arquivos e configuração próprios, criada a partir de uma imagem.'),
 ('O que faz','Permite executar aplicações com dependências separadas e uma configuração de execução definida.'),
 ('Como funciona','Usa recursos do kernel para separar visibilidade e controlar acesso a recursos.\nO processo continua executando no sistema.')],
 'Diga explicitamente: container não é só uma pasta compactada, nem uma máquina virtual pequena. Na execução, o runtime prepara um ambiente a partir de uma imagem e inicia processos com isolamento configurado. A imagem fornece arquivos; a instância acrescenta configuração e estado. O container pode estar parado e continuar existindo como objeto gerenciado. Ao falar que compartilha kernel, refira-se ao host Linux em que executa, que também pode ser uma VM.',
 'Empacotar a aplicação e executá-la em um container reduz diferenças de ambiente; não elimina todas elas.')
slide('isolamento','Isolamento: o que fica separado','Mecanismos do Linux usados na execução de containers',[
 ('Visibilidade','Namespaces podem separar a visão de processos, rede e pontos de montagem.\nA API tem sua própria perspectiva de localhost.'),
 ('Recursos','Cgroups permitem contabilizar e limitar CPU e memória.\nUm limite precisa ser configurado; não presuma um valor automático.'),
 ('Arquivos e permissões','A imagem fornece arquivos-base.\nA instância recebe uma camada gravável.\nUsuário e permissões também importam.')],
 'Relacione cada mecanismo a um efeito observável, sem transformar a aula em administração avançada do kernel. A separação de rede explica por que localhost da API não é o banco. Limites de recursos explicam por que um processo pode ter memória restrita. A visão de filesystem explica por que dependências de duas imagens não precisam ser instaladas no mesmo diretório do host. O isolamento é configurável; montagens e privilégios podem ampliar o acesso. Não apresente container como uma fronteira de segurança absoluta.',
 'Isolamento, limites e persistência são escolhas configuradas; o nome “container” não define sozinho essas políticas.')
slide('image_instance','Imagem e container são objetos diferentes','Artefato de origem versus instância com estado',note=
 'A imagem é um artefato de arquivos e metadados que serve de origem. Um container é a instância criada a partir dela, com um comando, variáveis, rede e estado gravável. A mesma imagem pode criar várias instâncias. Alterar um arquivo dentro de uma delas não altera a imagem original. O nome de uma imagem pode ser uma referência mutável, assunto para a consulta sobre tags e digest. A distinção principal é artefato versus execução, sem exigir ainda que o aluno conheça registry.',
 takeaway='Um novo container recebe a imagem e a configuração escolhidas; não herda automaticamente edições de outra instância.',kind='instances')
slide('runtime_container','Runtime de containers: quem prepara o isolamento','A palavra runtime também aparece em outra camada',note=
 'Este é o ponto que costuma gerar confusão. Node executa o código JavaScript; um runtime de containers prepara e inicia processos sob regras de isolamento. Em uma arquitetura Linux típica do Docker, containerd gerencia o ciclo de vida e um runtime de baixo nível, como runc, cria o processo conforme a configuração OCI. OCI é um conjunto de especificações de interoperabilidade, não outra aplicação que os alunos precisam instalar. O desenho simplifica detalhes como shims: o objetivo é distinguir responsabilidades, não decorar todos os processos internos.',
 takeaway='Node.js e um runtime de containers não se substituem: atuam em camadas diferentes.',kind='runtimes')
slide('docker','Docker: ferramentas para trabalhar com containers','Construir imagens, distribuir artefatos e gerenciar a execução',[
 ('Docker CLI','O comando docker é o cliente.\nRecebe sua solicitação no terminal.\nEnvia operações à API do Engine.'),
 ('Docker Engine','Serviço que gerencia imagens, containers, redes e volumes.\nNo Linux, o daemon é o dockerd.'),
 ('Ecossistema','BuildKit participa da construção.\nRegistries armazenam imagens.\nDocker Desktop facilita o ambiente local.')],
 'Agora associe a tecnologia à ferramenta. Container é um conceito de execução e isolamento; Docker fornece uma experiência para construir e operar esses objetos. Digitar docker não significa que o processo da aplicação foi iniciado dentro do cliente do terminal: há uma API e um serviço atendendo às operações. O cliente pode inclusive controlar um Engine remoto. Docker Desktop reúne componentes e interface para desenvolvimento; não deve ser confundido com o formato da imagem nem com o runtime da linguagem.',
 'Docker é a ferramenta de trabalho; imagem é o artefato; container é a instância executável.')
slide('docker_flow','O caminho de um docker run','Visão simplificada do pedido até a execução',note=
 'Percorra o desenho da esquerda para a direita. A CLI pede ao Engine para criar e iniciar uma instância. Se necessário e conforme a política de obtenção, uma imagem é baixada do registry. O Engine coordena preparação de filesystem, rede e execução usando os componentes de runtime. O processo principal começa com o comando escolhido. A aplicação não roda dentro do registry. Build é outro fluxo: transforma instruções e contexto em uma imagem, não inicia automaticamente um servidor permanente.',
 takeaway='O terminal controla a execução; o registry distribui a imagem; os processos executam no host do Engine.',kind='engine')
slide('desktop','Engine e Desktop: onde o container roda','Nesta aula trabalhamos com containers Linux',[
 ('Linux com Engine','O Engine pode executar sobre o Linux do host.\nOs containers compartilham esse kernel.'),
 ('Docker Desktop','Oferece uma instalação integrada.\nContainers Linux usam um ambiente Linux virtualizado.\nNo Windows, pode usar WSL 2.'),
 ('Consequência','Não há um kernel exclusivo em cada imagem.\nArquitetura de CPU e compatibilidade da imagem ainda precisam ser consideradas.')],
 'Use o ambiente efetivo da turma como exemplo, sem prometer uma arquitetura única para todos os sistemas. Docker Desktop em macOS usa uma VM Linux; no Windows há opções de backend e esta aula assume o modo de containers Linux. Mesmo que o aluno esteja no macOS, uma imagem Debian não inicializa sozinha um kernel Debian. A VM fornece o ambiente Linux necessário. Containers Windows existem, mas suas regras de compatibilidade estão fora do laboratório.',
 'VMs e containers podem coexistir: uma VM Linux pode hospedar vários containers.')
slide('compose','Docker Compose: descrever a aplicação integrada','Um arquivo declara serviços e os recursos usados em conjunto',note=
 'Apresente Compose antes de abrir YAML. Ele organiza a configuração de uma aplicação com um ou mais serviços e usa o Docker Engine para criar e operar os recursos. No laboratório há um serviço app e um serviço db. Serviço é a definição; container é uma instância dessa definição. Compose não executa JavaScript nem instala o banco dentro da API. O arquivo também pode declarar redes, volumes, variáveis e condições de inicialização. Um comando como up aplica essa descrição; isso não substitui testes funcionais.',
 takeaway='Dockerfile descreve como construir uma imagem; compose.yaml descreve como executar e integrar os serviços.',kind='compose_model')
slide('vm_comparison','VM e container: compare a estrutura','Agora que os componentes estão definidos, observe onde cada kernel fica',note=
 'Na VM, o hypervisor apresenta hardware virtual e cada convidado tem seu sistema operacional e kernel. Nos containers Linux, processos e bibliotecas de várias aplicações compartilham o kernel do host Linux. Isso pode reduzir a necessidade de manter um sistema operacional convidado por aplicação, mas não autoriza prometer tempos fixos de startup ou superioridade universal. O desenho é simplificado; o host dos containers também pode ser uma VM, como já vimos no Desktop.',
 takeaway='VM virtualiza uma máquina; container organiza processos sob isolamento do sistema operacional.',kind='vm')
slide('vm_decision','VM e container: diferenças que orientam a escolha','Compare requisitos; evite a regra “um sempre substitui o outro”',note=
 'Explore um exemplo de cada escolha. Uma aplicação que depende de outro sistema operacional ou de um kernel específico pode exigir VM. APIs com bibliotecas e versões de linguagem diferentes podem ser empacotadas em imagens separadas, executando no mesmo ambiente Linux compatível. Na nuvem é comum usar VMs como hosts de containers. Tempo de partida depende tanto da ferramenta quanto da aplicação, do download e dos dados inicializados; não use números fixos como propriedade garantida.',
 takeaway='Containerizar um monólito não o transforma em microsserviços: arquitetura e empacotamento são decisões diferentes.',kind='table',
 headers=['Critério','Máquina virtual','Container Linux'],widths=[.24,.38,.38],rows=[
 ['Kernel','Cada VM possui seu kernel convidado.','Compartilha o kernel do host Linux.'],
 ['Conteúdo','Inclui um SO convidado a administrar.','Imagem reúne os arquivos de usuário necessários.'],
 ['Uso típico','Outro SO/kernel; separação no nível da VM.','Empacotar e executar componentes de aplicação.'],
 ['Combinação','Pode hospedar vários containers.','Pode rodar em um host físico ou virtual.']])
slide('limits','O que a containerização resolve — e seus limites','Redução de diferenças de ambiente com responsabilidades explícitas',[
 ('Padroniza','Runtime e bibliotecas escolhidos.\nArquivos presentes na imagem.\nComando e configuração declarados.'),
 ('Ainda depende','Kernel e plataforma compatíveis.\nRecursos disponíveis e rede.\nCredenciais, serviços externos e dados.'),
 ('Não fornece sozinha','Correção de bugs.\nBackup e alta disponibilidade.\nSegurança absoluta ou arquitetura de microsserviços.')],
 'Feche a base conceitual explicando o alcance real. A mesma imagem reduz variações de arquivos e dependências, mas uma senha errada continua errada. Um volume local não protege de perda de disco. Um container sem limites definidos pode consumir recursos em excesso. Compose atende bem ao escopo de um host e pode ser usado em cenários compatíveis com isso; não oferece sozinho um cluster distribuído com alta disponibilidade.',
 'A execução confiável combina artefato conhecido, configuração correta, recursos adequados e verificação.')
slide('demo_version','Primeira demonstração: um comando que termina','Observar o runtime da linguagem dentro de uma imagem pronta',[
 ('Antes de executar','Engine/Desktop ativo.\nAcesso ao registry se a imagem não estiver local.\nNode no host não é obrigatório.'),
 ('O que acontece','Docker cria a instância.\nNode imprime uma versão 22.x.\nO processo termina; --rm remove a instância.')],
 'Execute este comando primeiro, sem banco nem Dockerfile. A saída deve ser uma versão 22.x, mas o patch depende da imagem obtida pela tag. A instalação de Node no host não é substituída por esse comando. O processo principal é curto: imprime e sai. O --rm remove o container depois da saída, não a imagem baixada. Se houver falha antes da execução, distinga daemon indisponível de falha de obtenção da imagem. Esta é uma observação guiada, não uma pergunta antes da definição.',
 'O container não precisa permanecer ativo: sua duração acompanha o processo principal.',kind='code',code='docker version\ndocker run --rm node:22-bookworm-slim node --version',section='Primeira execução',role='demo')
slide('demo_http','Segunda demonstração: um servidor que permanece ativo','Exemplo isolado • terminal Bash/zsh • porta local 18080 livre',[
 ('Entenda o comando','-d: executa em segundo plano.\n--name: nome da instância.\n-p: host 18080 → container 3000.'),
 ('Resultado esperado','A chamada HTTP retorna “Olá, turma!”.\nO processo Node continua esperando novas requisições.')],
 'Antes de executar, confirme que não existe uma instância e4-primeiro de uma demonstração anterior e que a porta 18080 está livre. Se já existir uma instância sua, use o roteiro de parada e remoção adiante; não interrompa serviços de outras tarefas. O código inline usa somente a biblioteca padrão de Node. O bind 0.0.0.0 aceita tráfego na interface do container; a publicação no host fica limitada ao endereço local. A sintaxe multilinha foi preparada para Bash/zsh. Mostre a resposta no terminal ou navegador.',
 'A porta publicada é uma entrada para chegar ao processo; ela não cria um servidor por si só.',kind='code',code='docker run -d --name e4-primeiro \\\n  -p 127.0.0.1:18080:3000 \\\n  node:22-bookworm-slim node -e \'\n    require("node:http").createServer((req, res) => {\n      res.end("Olá, turma!\\n");\n    }).listen(3000, "0.0.0.0");\n  \'\ncurl --retry 5 --retry-connrefused --retry-delay 1 \\\n  -fsS http://localhost:18080',section='Primeira execução',role='demo')
slide('lifecycle','Ciclo de vida: criar, observar, parar e remover','Comandos aplicados somente ao container e4-primeiro da demonstração',note=
 'Leia cada comando junto de seu efeito. ps lista containers em execução e ps -a inclui os parados. stop solicita encerramento e start retoma a mesma instância. rm remove a instância parada; os arquivos da imagem continuam disponíveis. docker top mostra os processos da instância. Não confunda start com run: start retoma uma instância existente, run cria uma nova. Ao terminar a demonstração, pare e remova apenas e4-primeiro. Isso não deve afetar a stack do laboratório nem outros serviços do host.',
 takeaway='Imagem, instância e processo têm ciclos de vida relacionados, mas não são o mesmo objeto.',kind='table',
 headers=['Comando','O que observar'],widths=[.46,.54],rows=[
 ['docker ps / docker ps -a','Instâncias ativas / todas as instâncias.'],
 ['docker top e4-primeiro','O processo Node executando na instância.'],
 ['docker stop e4-primeiro','Servidor para; a instância continua existindo.'],
 ['docker start e4-primeiro','A mesma instância volta a executar.'],
 ['docker stop e4-primeiro\ndocker rm e4-primeiro','Encerra e remove somente a instância de demonstração.']],section='Primeira execução',role='demo')
checkpoint('check_base','Verificação | Componentes e responsabilidades',[
 'Em node server.js dentro de um container, qual é o papel de Node e qual é o papel do runtime de containers?',
 'Duas instâncias criadas da mesma imagem são o mesmo container?',
 'Compose instala um kernel e executa o JavaScript da aplicação?'],[
 'Node executa o JavaScript. O runtime de containers prepara o isolamento e inicia o processo nesse ambiente. São camadas diferentes.',
 'Não. Compartilham a origem, mas possuem identidade, configuração e estado de instância próprios.',
 'Não. Compose declara e coordena serviços usando o Engine. O processo usa seu runtime de linguagem e o kernel do host Linux.'],section='Primeira execução')

slide('api_case','Agora vamos empacotar uma aplicação real','A mesma API de visitas vai ligar os conceitos de imagem, rede e dados',[
 ('Aplicação','server.js em Node.js.\nGET /visitas lê o total.\nPOST /visitas incrementa o total.'),
 ('Dependência','PostgreSQL guarda o contador.\nA biblioteca pg envia consultas.\nDATABASE_URL informa o destino.'),
 ('Contrato de saúde','/health/live: processo responde.\n/health/ready: SELECT 1 no banco.\nA operação de visitas será testada à parte.')],
 'A demonstração anterior separou container de integração. Agora acrescente uma dependência de verdade. Mostre que o serviço do banco é outro processo, não uma biblioteca instalada dentro de Node. O comando POST executa uma atualização atômica no banco e GET lê o valor. A demonstração é fornecida para o professor; não obriga as equipes a abandonar seu projeto. As credenciais aula/aula são fictícias e servem apenas à stack local de laboratório.',
 'A aplicação de exemplo ensina o padrão; a equipe deve adaptar esse padrão à aplicação que já escolheu.',section='Empacotamento')
slide('files','Arquivos do laboratório: uma responsabilidade por arquivo','Local: Práticas/encontro-4-containers',note=
 'Abra a pasta e localize cada arquivo antes do build. O package-lock.json faz parte do exemplo; não solicite npm ci sem fornecer um lockfile. O Dockerfile e o Compose têm papéis diferentes, que ficarão claros nos passos seguintes. O init.sql inicializa o banco quando seu diretório de dados está vazio; ele não é um sistema de migrações. O README concentra os comandos completos, enquanto alguns slides dividem trechos longos para facilitar a leitura.',
 takeaway='Para reproduzir a execução, o repositório precisa trazer todos os arquivos necessários, além das instruções.',kind='table',headers=['Arquivo','Responsabilidade'],widths=[.35,.65],rows=[
 ['server.js','Comportamento HTTP e acesso ao banco.'],['package.json + lockfile','Dependências e versões resolvidas.'],['Dockerfile + .dockerignore','Construção da imagem e controle do contexto.'],['compose.yaml','Execução dos serviços e recursos compartilhados.'],['init.sql + README.md','Inicialização didática do banco e instruções verificáveis.']],section='Empacotamento')
slide('dockerfile','Dockerfile: a receita de construção da imagem','Arquivo completo da API • o código é JavaScript, sem etapa de compilação',[
 ('Durante o build','Selecionar a base.\nInstalar pacotes pelo lockfile.\nCopiar os arquivos da aplicação.'),
 ('Na execução','Definir ambiente e usuário.\nDocumentar a porta.\nIndicar o comando principal.')],
 'Apresente o Dockerfile completo e explique que o builder lê instruções para produzir uma imagem. Ele não é um script que deve instalar tudo novamente em cada partida da API. FROM node:22-bookworm-slim fornece Node e bibliotecas do espaço de usuário; não inicia uma VM Debian. As próximas lâminas detalham os dois momentos para evitar a memorização sem entendimento. A escolha de slim é adequada ao exemplo; uma imagem menor não é automaticamente compatível ou segura.',
 'Build produz a imagem. A API começa a atender somente quando um container executa o comando definido.',kind='code',code=(LAB/'Dockerfile').read_text(),section='Empacotamento')
slide('dockerfile_build','Dockerfile: o que ocorre durante o build','A ordem cria os arquivos que farão parte da imagem',note=
 'Percorra a tabela com o Dockerfile aberto ao lado. WORKDIR define o diretório das instruções seguintes. A primeira cópia coloca manifests no contexto da instalação. npm ci usa o lockfile e falha se estiver incoerente com package.json. A segunda cópia transfere somente server.js, evitando incluir arquivos locais desnecessários. O chown ajusta propriedade do arquivo copiado. Não diga que toda instrução adiciona uma camada de filesystem: instruções também podem definir metadados.',
 takeaway='O código e as dependências precisam entrar na imagem pelo build, não por edição manual de uma instância.',kind='table',headers=['Instrução','Efeito no exemplo'],widths=[.49,.51],rows=[
 ['FROM node:22-bookworm-slim','Escolhe o runtime e os arquivos-base.'],['WORKDIR /app','Define /app como diretório de trabalho.'],['COPY package.json package-lock.json ./','Coloca os manifests antes da instalação.'],['RUN npm ci --omit=dev','Instala as dependências de execução.'],['COPY --chown=node:node server.js ./','Inclui o código com propriedade definida.']],section='Empacotamento')
slide('dockerfile_run','Dockerfile: como a instância vai iniciar','Metadados que orientam a execução do processo',note=
 'ENV define um padrão não secreto que pode ser sobrescrito na execução. USER escolhe a identidade do processo; é uma redução de privilégio, não uma garantia de segurança total. EXPOSE registra uma intenção sobre a porta, mas não publica acesso no host. CMD fornece o comando padrão, sujeito a substituição na criação do container. A forma JSON inicia o comando diretamente, sem depender de um shell para interpretar a linha. O servidor é de longa duração, por isso não deve ser iniciado com RUN durante o build.',
 takeaway='RUN executa uma etapa de construção; CMD define o comando padrão para a execução do container.',kind='table',headers=['Instrução','Efeito na execução'],widths=[.46,.54],rows=[
 ['ENV NODE_ENV=production','Define um valor padrão de configuração.'],['USER node','Executa como o usuário node da imagem.'],['EXPOSE 3000','Documenta a porta; não publica no host.'],['CMD ["node", "server.js"]','Inicia o processo principal da API.']],section='Empacotamento')
slide('cache','Lockfile e cache: reproduzir sem reinstalar à toa','Instalar dependências antes de copiar o código favorece a reutilização',note=
 'O lockfile registra a resolução das dependências; ele não congela sozinho a base, a plataforma ou todos os componentes externos. Compare as duas ordens do desenho. Quando server.js muda depois de npm ci, a instalação pode ser reutilizada. Se o lockfile muda, a etapa de instalação precisa ser reavaliada. O cache pode não estar disponível numa máquina nova. Demonstre com dois builds e procure CACHED, sem prometer uma duração fixa. Diferencie reutilização de cache de atualização da imagem-base.',
 takeaway='Alteração de código não precisa reinstalar dependências quando suas entradas e o cache permanecem válidos.',kind='cache',section='Empacotamento')
slide('context','Contexto de build e .dockerignore','O ponto em docker build indica o diretório usado como contexto',[
 ('Duas fronteiras','Git filtra o versionamento.\nDocker filtra o contexto.\n.gitignore ≠ .dockerignore.'),
 ('No laboratório','node_modules local não entra.\nArquivos .env ficam fora.\nO lockfile precisa continuar disponível.')],
 'Use a pasta do laboratório como exemplo de contexto. Um arquivo ignorado pelo Git pode continuar presente no disco e ser enviado ao builder se não for excluído. A cópia seletiva de server.js ajuda a evitar inclusão acidental, mas o .dockerignore ainda expressa a intenção sobre o contexto. Não copie uma senha e depois tente apagá-la em outra etapa: camadas anteriores podem conservar informação. Valores fictícios do laboratório não devem ser confundidos com gestão de segredos em produção.',
 'Reprodução e segurança começam no conjunto de arquivos que você permite entrar na construção.',kind='code',code=(LAB/'.dockerignore').read_text(),section='Empacotamento')
slide('build_demo','Construir a API e observar sua execução isolada','Executar dentro da pasta do laboratório • usar dois terminais',[
 ('Terminal 1','Build cria e4-api:local.\nrun inicia a API em primeiro plano.\nCtrl+C encerra a demonstração.'),
 ('Terminal 2','live responde 200.\nready responde 503 sem o banco.\nIsso separa empacotamento de integração.')],
 'Use a porta 18081 livre para não conflitar com a stack Compose, que usa 8080. A aplicação do exemplo pode iniciar o processo sem conexão prévia com o banco; a consulta de prontidão falha sob demanda. Por isso live pode funcionar enquanto ready falha. A conexão da pool precisa de um PostgreSQL alcançável para as operações que o utilizam. A demonstração não prova o sistema inteiro: ela prova que a imagem inicia a API e deixa evidente a dependência ainda ausente.',
 'Uma imagem construída com sucesso ainda precisa ser executada e testada no contexto de suas dependências.',kind='code',code='docker build -t e4-api:local .\ndocker run --rm -p 127.0.0.1:18081:3000 e4-api:local\n\n# Em outro terminal:\ncurl -i http://localhost:18081/health/live\ncurl -i http://localhost:18081/health/ready',section='Empacotamento',role='demo')
checkpoint('check_build','Verificação | Imagem e execução',[
 'Trocar RUN npm ci por CMD npm ci mantém o mesmo comportamento?',
 'Alterar server.js depois da cópia dos manifests precisa invalidar npm ci em todo build?',
 'Se live retorna 200 e ready retorna 503 nesta execução isolada, o que já foi comprovado?'],[
 'Não. RUN instala durante o build; CMD executaria a instalação na partida, no lugar do comando principal esperado.',
 'Não necessariamente. A instalação pode usar cache se suas entradas e a base continuam válidas. O código foi copiado depois.',
 'O processo HTTP responde. A consulta de prontidão não passou; sem o banco integrado, ainda não há prova da funcionalidade de visitas.'],section='Empacotamento')

slide('compose_app','Compose: declarar o serviço da API','Serviço = definição • container = instância criada dessa definição',[
 ('Construção e acesso','build: . aponta para o contexto.\nports publica 8080 → 3000.\nO acesso do host fica local.'),
 ('Configuração','DATABASE_URL aponta para db.\nHOST orienta a interface de escuta.\nCredenciais aqui são fictícias.')],
 'Retome o conceito de Compose já apresentado na base. Agora leia um serviço de verdade. O arquivo completo do laboratório também contém depends_on e healthcheck; esta lâmina isola os campos de construção, acesso e configuração. build não significa que o banco será instalado dentro da API. DATABASE_URL precisa do hostname db porque a chamada sairá do container da API. Os nomes app e db são escolhas do projeto, usados como identificadores de serviços.',
 'O arquivo permite revisar e compartilhar a configuração que antes ficaria em uma longa linha de docker run.',kind='code',code='services:\n  app:\n    build: .\n    ports:\n      - "127.0.0.1:8080:3000"\n    environment:\n      DATABASE_URL: postgres://aula:aula@db:5432/aula\n      HOST: 0.0.0.0\n# Trecho: dependência e saúde aparecem adiante.',section='Integração')
slide('compose_db','Compose: banco de dados em outro serviço','Imagem pronta do PostgreSQL + estado em volume nomeado',[
 ('Configuração inicial','A imagem cria usuário e banco na primeira inicialização de dados vazios.'),
 ('Persistência','dados é um recurso separado.\nO caminho pertence ao PostgreSQL 16 deste exemplo.')],
 'O banco usa uma imagem pronta, enquanto a API tem uma imagem construída no projeto. O volume nomeado dados é montado no diretório esperado por PostgreSQL 16. Versões maiores podem mudar requisitos e demandar migração; não generalize o caminho sem verificar a imagem. A conta aula da inicialização simplifica a aula e não representa privilégios mínimos de produção. O arquivo completo monta init.sql e declara healthcheck; os próximos slides mostram essas responsabilidades.',
 'API e banco podem ser atualizados ou recriados separadamente; os dados não devem depender da camada gravável do banco.',kind='code',code='  db:\n    image: postgres:16-alpine\n    environment:\n      POSTGRES_USER: aula\n      POSTGRES_PASSWORD: aula\n      POSTGRES_DB: aula\n    volumes:\n      - dados:/var/lib/postgresql/data\nvolumes:\n  dados:',section='Integração')
slide('init','Inicializar o contador não é migrar o banco','init.sql prepara o estado inicial somente em um diretório de dados vazio',[
 ('Estado inicial','Tabela contador e linha id=1.\nO total começa em zero num volume novo.'),
 ('Depois da primeira vez','Editar init.sql não altera automaticamente o banco existente.\nMudanças posteriores exigem migração.')],
 'O arquivo completo usa um bind mount somente leitura para levar init.sql a docker-entrypoint-initdb.d. A imagem oficial executa scripts dessa pasta ao inicializar um diretório de dados vazio. Se o volume já contém o banco, não há uma nova inicialização equivalente. O mesmo raciocínio vale para variáveis de senha: alterar o YAML não troca por si só a senha persistida. Não apague dados apenas para ocultar a falta de uma migração. No projeto, documente como o schema é criado e evolui.',
 'Recriar um container e recriar o estado do banco são operações diferentes.',kind='code',code='CREATE TABLE IF NOT EXISTS contador (\n  id integer PRIMARY KEY,\n  total integer NOT NULL\n);\nINSERT INTO contador (id, total)\nVALUES (1, 0) ON CONFLICT (id) DO NOTHING;',section='Integração')
slide('network','A requisição percorre duas conexões','HTTP do cliente para a API; SQL da API para o PostgreSQL',note=
 'Trace a chamada com o dedo. O cliente no host chega a localhost:8080. O encaminhamento leva ao processo da API na porta 3000. A consulta SQL é uma nova conexão, feita pela API em direção a db:5432. db é resolvido pelo nome do serviço na rede compartilhada. Não é necessário publicar a porta do banco para que a API a alcance. Em configurações com redes distintas, a descoberta depende de ambos os serviços compartilharem uma rede apropriada.',
 takeaway='localhost pertence ao ambiente de quem faz a chamada; dentro da API ele não significa “o container do banco”.',kind='network',section='Integração')
slide('ports','Porta documentada, publicada e interface de escuta','Três decisões distintas precisam ser coerentes',[
 ('EXPOSE 3000','Metadado da imagem.\nDocumenta uma porta pretendida.\nNão cria acesso pelo host.'),
 ('8080:3000','Publicação no host.\n8080 recebe o cliente.\n3000 deve coincidir com a porta real do processo.'),
 ('HOST=0.0.0.0','A API escuta nas interfaces do container.\n127.0.0.1 restringiria a escuta ao loopback dessa instância.')],
 'Use o primeiro servidor da aula para tornar a distinção concreta. O host estava em 18080 e o processo na porta 3000; não era necessário que os números fossem iguais. No laboratório integrado usamos 8080 para o cliente. A publicação 127.0.0.1:8080:3000 restringe o acesso ao host local, enquanto HOST=0.0.0.0 permite ao processo receber pela interface do container. Essas duas configurações atuam em camadas diferentes e não se contradizem.',
 'Trocar 8080 por 9090 muda o endereço do cliente; a comunicação da API com db:5432 continua igual.',section='Integração')
slide('env','Configuração de execução fora da imagem','A mesma imagem pode receber valores distintos em cada ambiente',[
 ('environment','Entrega variáveis ao processo.\nEx.: HOST: 0.0.0.0.\nA API lê process.env.HOST.'),
 ('.env no Compose','Pode fornecer valores para interpolar ${VAR} no YAML.\nNão injeta sozinho todo o arquivo no container.'),
 ('Aplicar mudanças','Variável de execução: recriar a instância.\nCódigo/dependência: reconstruir imagem.\nrestart não aplica todo YAML alterado.')],
 'Explique com um valor não secreto: no .env, PORTA_HOST=9090; no YAML, ports pode referenciar ${PORTA_HOST}:3000. Isso configura a publicação, mas não implica que process.env.PORTA_HOST exista na API. Para entregar uma variável ao processo, declare environment ou um mecanismo apropriado como env_file. O laboratório usa credenciais fictícias para ficar autocontido; os projetos devem documentar variáveis sem versionar segredos reais. Valores embutidos no build de certos frontends estáticos exigem reconstrução, mesmo quando parecem “configuração”.',
 'Após mudar HOST no YAML: docker compose up -d --no-deps --force-recreate --wait app.',section='Integração')
slide('storage','Arquivos da instância, volume e bind mount','Escolha onde cada tipo de dado deve viver',note=
 'A camada gravável pertence à instância e desaparece quando ela é removida. Um volume nomeado é um recurso gerenciado pelo Docker, reutilizável por uma instância posterior. Um bind mount aponta para um caminho do host e depende de seu conteúdo e permissões. No laboratório, dados é volume nomeado e init.sql é um bind mount somente leitura. Stop/start conserva a mesma instância; down/up cria outra. Nenhuma dessas escolhas substitui backup e um teste de restauração.',
 takeaway='Estado de negócio deve ter persistência planejada; uma imagem nova não deve apagar o banco.',kind='storage',section='Integração')
slide('persistence_demo','Comprovar persistência com uma experiência','Anotar → recriar containers → ler novamente',[
 ('Antes','Leia e anote o total N.\nPOST deve produzir N + 1.\nGuarde o valor observado.'),
 ('Depois','down sem -v preserva o volume nomeado.\nCom o mesmo projeto, up o reutiliza.\nGET deve devolver o total preservado.')],
 'Faça a demonstração com dados fictícios. Os números dependem do estado anterior do volume, então não exija total igual a 1. A propriedade testada é a igualdade da última leitura antes da parada com a leitura após a recriação. Um nome de projeto diferente pode criar outro volume; um contador zerado nesse caso não prova que o anterior foi perdido. down -v remove volumes declarados e não é o encerramento padrão do laboratório. Perda do disco do host exige uma estratégia de backup além deste teste.',
 'Persistência além da instância não é recuperação de desastre; volume e backup resolvem problemas diferentes.',kind='code',code='curl -fsS -X POST http://localhost:8080/visitas\ncurl -fsS http://localhost:8080/visitas\ndocker compose down\ndocker compose up -d --wait\ncurl -fsS http://localhost:8080/visitas',section='Integração',role='demo',defer_demo=True)
slide('health','Estado do processo, prontidão e funcionalidade','Defina o que cada evidência realmente mede',note=
 'Um processo em execução pode estar incapaz de atender porque o banco caiu. Um healthcheck pode ser limitado: nosso SELECT 1 confirma uma consulta básica, mas não prova que a tabela contador existe. A operação GET/POST /visitas testa outro contrato. Docker registra healthy ou unhealthy conforme o comando configurado; não reinicia automaticamente apenas porque o check falhou. Políticas de restart tratam a saída do processo conforme suas regras. O diagnóstico precisa diferenciar esses fatos.',
 takeaway='Um estado verde vale somente o que a verificação executada cobre.',kind='health',section='Integração')
slide('health_config','Healthcheck: comando e parâmetros de observação','Trecho real do banco no laboratório',[
 ('Quando observar','interval: entre verificações.\ntimeout: limite por execução.\nstart_period: tolerância inicial.'),
 ('Como interpretar','retries: falhas consecutivas.\nSaída 0: sucesso do check.\npg_isready não testa a regra de negócio.')],
 'Leia as unidades e o comando sem supor familiaridade prévia. pg_isready indica o estado de aceitação de conexões, mas não comprova a credencial e todas as operações da aplicação. A API tem um check próprio no arquivo completo, usando Node para chamar /health/ready. start_period tolera falhas iniciais; um sucesso nesse período já sinaliza a inicialização bem-sucedida. Evite prometer um instante exato para unhealthy, pois duração e agendamento das verificações influenciam. O comando de saúde observa; não corrige a causa.',
 'O healthcheck da API consulta /health/ready; o teste funcional ainda precisa executar /visitas.',kind='code',code='healthcheck:\n  test: ["CMD-SHELL",\n         "pg_isready -U aula -d aula"]\n  interval: 5s\n  timeout: 3s\n  retries: 10\n  start_period: 10s',section='Integração')
slide('depends','depends_on: coordenar a partida dos serviços','Esperar um check inicial reduz a corrida de inicialização',[
 ('Partida','Compose espera o check de db passar antes de iniciar app.'),
 ('Operação','O banco ainda pode cair depois.\nA API precisa tratar falhas e timeouts.\nUm retry de escrita exige cuidado com duplicação.')],
 'Mostre a linha condition: service_healthy. Sem uma condição de saúde apropriada, ordenar a partida não garante que o banco esteja pronto para receber consultas. A espera inicial também não é um contrato de disponibilidade eterna. Na API fornecida, falhas de consulta geram 503 e novas requisições podem funcionar quando a dependência volta. Repetir automaticamente a mesma gravação é outro problema: é preciso avaliar se o efeito já ocorreu e se a operação é idempotente.',
 'Inicialização coordenada ajuda a começar; tratamento de falhas ajuda a continuar operando.',kind='code',code='services:\n  app:\n    # Demais campos definidos anteriormente\n    depends_on:\n      db:\n        condition: service_healthy',section='Integração')
slide('compose_demo','Subir a aplicação integrada e verificar a resposta','Usar o compose.yaml completo fornecido no laboratório',[
 ('Preparar','Engine ativo; porta 8080 livre.\nTerminal na pasta do laboratório.\nconfig valida a declaração.'),
 ('Observar','up cria serviços e recursos.\n--wait aguarda os checks.\nAs chamadas HTTP verificam a resposta.')],
 'Reúna os trechos mostrando o arquivo completo, sem pedir aos alunos que montem manualmente um YAML a partir das lâminas. Execute config --quiet e depois up. Se --wait falhar, consulte ps -a e logs antes de seguir; esse resultado não é uma autorização para apagar dados. O primeiro build pode exigir downloads. O README inclui alternativas para investigar porta ocupada. Depois que a stack estiver saudável, execute as rotas e a experiência de persistência apresentada na sequência.',
 'A API só está integrada quando a operação real consegue atravessar a conexão com o banco.',kind='code',code='docker compose config --quiet\ndocker compose up -d --build --wait\ndocker compose ps\ncurl -fsS http://localhost:8080/health/live\ncurl -fsS http://localhost:8080/health/ready\ncurl -fsS -X POST http://localhost:8080/visitas\ncurl -fsS http://localhost:8080/visitas',section='Integração',role='demo')
slide('evidence_read','Interpretar as saídas da demonstração','Exemplo de sequência • números ilustrativos, dependentes do estado do volume',note=
 'Use os valores da execução real, e não apenas a captura da aula. Leia o total antes da gravação e compare com o resultado do POST. Para demonstrar a persistência, use a sequência down/up sem -v e faça a nova leitura. A evidência deve descrever qual comportamento foi comprovado, não apenas que algo ficou verde. SELECT 1 bem-sucedido não prova schema, permissões de todas as tabelas nem toda a lógica de negócio. Essa distinção prepara o diagnóstico seguinte.',
 takeaway='Comandos e resultados devem ser relacionados a uma afirmação verificável sobre o projeto.',kind='table',headers=['Observação','Interpretação'],widths=[.46,.54],rows=[
 ['GET /health/live → 200','O processo HTTP respondeu.'],['GET /health/ready → 200','A consulta básica no banco funcionou.'],['GET total 7 → POST total 8 → GET total 8','A operação gravou e leu o incremento.'],['Após down/up, GET total 8','O estado foi preservado no volume reutilizado.']],section='Integração')
checkpoint('check_integration','Verificação | Rede, dados e saúde',[
 'A porta do host muda para 9090. A API deve passar a usar db:9090?',
 'Depois de down/up sem -v, o total permanece. Isso prova que há backup?',
 'O check SELECT 1 passa, mas a tabela contador não existe. /visitas está garantido?'],[
 'Não. 9090 é a entrada do cliente na API. A conexão interna com o banco continua db:5432.',
 'Não. Prova persistência no volume reutilizado. Backup requer uma cópia recuperável e restauração testada.',
 'Não. A consulta básica pode passar enquanto a operação falha por schema ausente. Teste GET/POST /visitas.'],section='Integração')

slide('diagnosis','Diagnóstico: observar antes de alterar','Uma sequência de verificação para localizar a falha',note=
 'Comece identificando se o problema ocorreu no build ou na execução. No build, confira o contexto, os arquivos e a etapa que falhou. Na execução, inclua containers parados na inspeção, leia logs e só então relacione configuração, rede e dependências. Uma mensagem de conexão recusada sugere que não houve serviço aceitando naquele destino; não prova sozinha por que isso ocorreu. Mudar várias coisas simultaneamente impede saber qual hipótese estava correta.',
 takeaway='Sintoma → hipótese → teste → correção mínima → nova validação → registro.',kind='trouble',section='Diagnóstico')
slide('diagnosis_tools','Comandos com uma pergunta técnica definida','Cada comando produz uma evidência diferente',note=
 'Explique por que exec não é o primeiro recurso se a instância encerrou: ele precisa de um container ativo. Primeiro veja ps -a e logs. O comando node que imprime HOST é um exemplo seguro porque inspeciona apenas um valor não secreto. Evite imprimir toda a configuração ou environment em um ambiente real. Em imagens mínimas, curl e shell podem não existir; no laboratório há Node, então é possível usar suas bibliotecas para verificações específicas.',
 takeaway='Não memorize uma lista de comandos sem entender qual hipótese cada um testa.',kind='table',headers=['Comando','O que ele ajuda a responder'],widths=[.59,.41],rows=[
 ['docker compose ps -a','A instância iniciou ou encerrou?'],['docker compose logs --tail=60 app','Qual erro a aplicação emitiu?'],['docker compose exec db pg_isready -U aula -d aula','O banco aceita conexões?'],['docker compose exec app node -p "process.env.HOST"','Qual bind a API recebeu?'],['docker compose config --quiet','A declaração é válida para o Compose?']],section='Diagnóstico')
slide('case_localhost','Caso resolvido: banco saudável, API retorna 503','Falha provocada: hostname localhost na conexão da API',[
 ('Sintoma e evidência','db está healthy.\nready retorna 503.\nLog da API: conexão recusada.\nURL aponta para localhost:5432.'),
 ('Causa explicada','A conexão sai da API.\nlocalhost aponta para ela mesma.\nO banco está no serviço db da rede compartilhada.'),
 ('Correção e prova','Trocar localhost por db.\nRecriar app com a nova configuração.\nRepetir ready e GET/POST /visitas.')],
 'Use apenas a cópia de laboratório para provocar a falha. Altere uma coisa: o hostname da URL. Recrie app sem --wait, pois estamos esperando uma falha de prontidão, e recolha logs e resposta HTTP. Confirme que db continua disponível. A correção é restaurar db na URL e recriar a instância, mantendo volume e banco. O README tem os comandos completos de provocação, inspeção e recuperação. Publicar 5432 no host não corrige o significado de localhost dentro da API.',
 'A evidência antes/depois deve confirmar a causa; apagar o volume não testa esta hipótese.',section='Diagnóstico')
slide('case_bind','Caso resolvido: check verde, acesso externo falha','Falha provocada: HOST=127.0.0.1 dentro do container',[
 ('Sintoma e evidência','Chamada interna em localhost:3000 funciona.\nCliente no host:8080 falha.\nO healthcheck interno pode ficar verde.'),
 ('Causa explicada','A API escuta apenas no loopback da instância.\nO tráfego publicado chega pela interface de rede do container.'),
 ('Correção e prova','Restaurar HOST=0.0.0.0.\nRecriar app.\nComparar novamente a mesma rota de dentro e de fora.')],
 'Este caso mostra por que definir de onde o teste parte é essencial. O healthcheck da aplicação usa o loopback interno, que continua acessível com o bind errado para tráfego externo. Antes de corrigir, demonstre os dois pontos de observação. Em seguida mude apenas HOST, recrie e repita as chamadas. O arquivo da imagem EXPOSE não altera a interface real de escuta do processo. O mapeamento no Compose precisa continuar apontando para a porta correta.',
 'Um teste interno bem-sucedido não garante o caminho percorrido pelo cliente externo.',section='Diagnóstico')
slide('case_dependency','Caso resolvido: dependência cai durante o uso','Parar apenas o banco diferencia processo vivo de funcionalidade disponível',[
 ('Provocar e observar','docker compose stop db\nlive continua 200.\nready e /visitas retornam 503.'),
 ('Explicação','A API segue em execução.\nA operação precisa de consulta SQL.\ndepends_on já cumpriu seu papel na partida.'),
 ('Recuperar e provar','docker compose start db\nAguardar o banco aceitar conexões.\nready volta a 200; o total permanece.')],
 'Esta é a demonstração de falha mais rápida, sem edição do YAML. O código da API trata erros de consulta e da pool para permitir novas requisições após o banco voltar. Isso foi validado no laboratório anterior e deve ser ensaiado no ambiente da aula. Não generalize a recuperação para toda aplicação: algumas precisam de tratamento adicional. Discuta por que reiniciar tudo pode ser desnecessário e também esconder evidências úteis.',
 'Recuperar a dependência e testar novas requisições pode bastar; a decisão deve seguir a evidência.',section='Diagnóstico',role='demo')
slide('ai','IA no diagnóstico: hipótese com teste verificável','Exemplo de pedido depois de coletar o sintoma e a configuração relevante',[
 ('Contexto fornecido','API retorna 503 em ready.\ndb aparece healthy.\nURL usa localhost:5432.\nSem senhas nem dados reais.'),
 ('Pedido à IA','“Liste hipóteses priorizadas.\nPara cada uma, dê um teste não destrutivo e o resultado que a descartaria.”'),
 ('Validação humana','Conferir a relação causa/ação.\nExecutar a verificação.\nRejeitar down -v para um erro de hostname.\nRegistrar correção e resultado.')],
 'A IA entra após os alunos entenderem o sistema que estão diagnosticando. Ela pode organizar hipóteses e explicar mensagens, mas a hipótese só é útil se puder ser confrontada com uma evidência. Mostre uma recomendação sem relação causal, como apagar um volume para corrigir uma porta, e explique por que ela é rejeitada. Não exponha dumps de environment ou inspect contendo segredos. Um registro crítico inclui sugestões rejeitadas, não apenas as que funcionaram.',
 'Toda saída de IA é hipótese até ser validada por teste, execução ou revisão humana.',section='Diagnóstico')

slide('project_bridge','Como este encontro entra no projeto integrador','O mesmo projeto evolui do código validado ao ambiente executável',note=
 'Agora faça a ligação com os encontros anteriores. A equipe já escolheu uma aplicação, organizou colaboração e criou CI. O incremento de hoje não substitui nada disso: acrescenta um contrato de execução da aplicação e suas dependências. No próximo encontro, a imagem verificável será candidata a uma entrega controlada, com configuração e rollback. No encontro final, logs e evidências vão sustentar a demonstração. Não há um segundo projeto separado nem obrigação de adotar a API de visitas.',
 takeaway='E4 alimenta os 20% de Containers/Compose já previstos na rubrica; os demais pesos permanecem os oficiais.',kind='project',section='Projeto')
slide('project_mapping','Traduzir o exemplo para a aplicação da equipe','A linguagem pode mudar; as responsabilidades continuam',note=
 'Peça que a equipe identifique equivalentes no próprio repositório. Uma aplicação Java pode executar um jar, Python um módulo ou servidor WSGI/ASGI, e Node um arquivo ou script definido. Não copie npm ci para outra stack. Dependência pode ser PostgreSQL, outro banco ou um serviço auxiliar pertinente. Se uma aplicação não precisa de banco, não acrescente um sem justificativa só para imitar o exemplo; explique sua integração e os recursos de estado reais. A evidência deve avaliar a aplicação escolhida, não uma demonstração paralela.',
 takeaway='Antes de escrever o Dockerfile, anote comando, runtime, dependências, configuração e estado do próprio projeto.',kind='table',headers=['No exemplo da aula','No projeto da equipe'],widths=[.43,.57],rows=[
 ['Node + server.js','Runtime e comando reais da aplicação.'],['pg + lockfile npm','Dependências controladas da stack escolhida.'],['app → db','Componentes que de fato precisam conversar.'],['dados + init.sql','Persistência e inicialização/migração pertinentes.'],['live, ready e /visitas','Check de saúde e operação funcional do projeto.']],section='Projeto')
slide('project_plan','Plano técnico: decisões antes de executar','Preencher no README da própria equipe',[
 ('Imagem','Qual comando inicia a aplicação?\nQual runtime e versão ela usa?\nQuais arquivos precisam entrar?'),
 ('Integração','Quais serviços existem?\nQuem chama quem e por qual porta?\nQuais variáveis são obrigatórias?'),
 ('Dados e validação','Onde o estado deve persistir?\nO que o check de saúde mede?\nQual operação comprova funcionamento?')],
 'Estas perguntas são uma atividade de aplicação, depois da explicação e da demonstração. Oriente a equipe a registrar respostas objetivas, não frases como “usar Docker para padronizar”. Um bom registro diz, por exemplo: API escuta 3000, cliente usa 8080, banco é acessado pelo nome db e dados vivem em um volume. A escolha de mecanismos de configuração e schema deve acompanhar a stack real. A próxima lâmina distribui o trabalho em checkpoints.',
 'As decisões do README devem corresponder aos arquivos versionados e à execução que será demonstrada.',section='Projeto',role='atividade')
slide('project_lab','Laboratório: aplicar ao projeto da equipe','70 minutos reservados para implementação e evidências',[
 ('0–20 min | Empacotar','Dockerfile e .dockerignore.\nDependências controladas.\nImagem inicia com comando claro.'),
 ('20–45 min | Integrar','Compose com serviços pertinentes.\nConfiguração, rede, dados e saúde.\nExecutar uma operação funcional.'),
 ('45–70 min | Validar','Provocar e corrigir uma falha.\nConferir README a partir de clone limpo.\nRegistrar comandos, resultados e decisões.')],
 'Circule pela turma verificando comportamento em vez de apenas arquivos presentes. Uma pessoa pode operar, outra acompanhar logs, outra registrar a evidência e outras revisar o comando e o critério de sucesso; troquem funções. Mantenha o acompanhamento e a entrega de grupo conforme o regulamento existente. Se o tempo estiver curto, preserve o teste funcional e o registro de uma falha compreendida. O laboratório da API de visitas continua como referência, não como substituto do projeto.',
 'A equipe deve conseguir explicar o que cada serviço faz e reproduzir sua própria execução.',section='Projeto',role='atividade')
slide('acceptance','Critérios de aceite: o que deve ficar demonstrado','Evidências no repositório • critério Containers/Compose: 20%',[
 ('Reprodução','Dockerfile, Compose e arquivos necessários.\nREADME com setup, subida, teste e parada.\nNenhum arquivo local oculto indispensável.'),
 ('Comportamento','Aplicação inicia.\nOperação alcança a dependência.\nEstado persiste quando necessário.\nCheck tem um contrato explicado.'),
 ('Raciocínio','Falha reproduzida e causa confirmada.\nCorreção validada por execução.\nRegistro crítico de IA, se utilizada.\nEscolhas justificadas.')],
 'Não altere os pesos homologados nem introduza uma nota individual. Este conjunto de evidências contribui para o critério já estabelecido. Clone limpo significa que os arquivos necessários estão disponíveis pelo repositório e pelas instruções, não que dados reais devam ser apagados. Peça que alguém siga o README sem ajuda oral para revelar etapas implícitas. Um print do Docker aberto não prova integração funcional ou diagnóstico.',
 'Arquivo presente é parte da evidência; resultado reproduzível e explicação da decisão completam a entrega.',section='Projeto')
slide('filled_evidence','Exemplo preenchido: evidência de uma falha corrigida','Modelo ilustrativo para adaptar aos comandos e resultados reais da equipe',note=
 'Mostre um registro curto mas causal. O importante é que o aluno possa relacionar a hipótese à evidência e à mudança específica. Não apresente os dados desta tabela como execução da equipe; são um modelo didático. Se a equipe usou IA, registre qual hipótese ela sugeriu e como foi aceita ou descartada. A validação final deve testar tanto a prontidão quanto uma operação funcional, porque os contratos são diferentes.',
 takeaway='Substitua os valores do exemplo pela execução real e mantenha toda evidência no repositório.',kind='table',headers=['Campo','Exemplo preenchido'],widths=[.24,.76],rows=[
 ['Sintoma','GET /health/ready devolvia HTTP 503.'],['Hipótese e teste','URL usava localhost; db estava saudável. Conferimos destino e logs.'],['Causa','A API procurava o banco em sua própria instância.'],['Correção','Hostname mudou para db; somente app foi recriado.'],['Validação','ready retornou 200; POST incrementou N para N+1 e GET confirmou.']],section='Projeto')
checkpoint('check_final','Verificação final | Explicar o próprio projeto',[
 'Ao apresentar o projeto, como distinguir imagem, container e os dois sentidos de runtime?',
 'Como provar que sua aplicação está integrada à dependência, além de mostrar o container Up?',
 'Qual evidência liga uma alteração de configuração à correção de uma falha?'],[
 'Imagem: artefato. Container: instância. Runtime da linguagem executa o código; runtime de containers prepara e inicia processos isolados.',
 'Executar uma operação funcional com resultado esperado; verificar saúde e persistência conforme o contrato do projeto.',
 'Sintoma reproduzido, hipótese testada, mudança específica e repetição do mesmo teste com resultado corrigido.'],section='Projeto')
slide('next','Do ambiente executável à entrega controlada','Conexão com o Encontro 5 e a apresentação final',[
 ('Levar pronto','Projeto executável por comando documentado.\nIntegração demonstrada.\nFalha corrigida e registrada.'),
 ('Preparar a entrega','Identificar a imagem validada.\nSeparar configuração de ambiente.\nDefinir promoção e rollback.'),
 ('Apresentação final','Explicar o fluxo código → CI → imagem → execução.\nMostrar evidências reais.\nDefender as escolhas adotadas.')],
 'Feche o encontro retomando a sequência lógica, sem abrir um novo laboratório. A equipe agora tem uma forma de executar a aplicação e pode começar a discutir entregar um artefato conhecido. O build de imagem no CI é uma evolução útil, mas não substitui os testes anteriores. Um pipeline que apenas constrói a imagem não prova que ela consegue iniciar e atender no ambiente de destino. O encontro seguinte discutirá controlar essa passagem com critérios explícitos.',
 'Containerização tem valor quando melhora a reprodução, a integração e a entrega do projeto.',section='Projeto')
slide('references','Referências e consulta depois da aula','Documentação oficial e material do próprio laboratório',[
 ('Conceitos','Docker: visão geral e containers.\nEngine e Compose.\ncontainerd e runc: responsabilidades.'),
 ('Prática','Dockerfile, cache e .dockerignore.\nRedes, volumes e health checks.\nImagem oficial PostgreSQL.'),
 ('Material disponível','Notas do apresentador.\nGuia completo por slide.\nREADME e exemplos executáveis.\nGabaritos das verificações.')],
 'As referências oficiais estão com links completos no guia e na apostila. Os diagramas são esquemas didáticos editáveis, não capturas de uma arquitetura obrigatória em todas as instalações. Consulte as versões efetivamente utilizadas quando houver diferença de comando ou implementação. As próximas lâminas são de consulta para aprofundamento, não uma extensão obrigatória da aula de quatro horas.',
 'Fim da trilha principal. Os próximos slides são material de consulta, sem nova entrega obrigatória.',section='Referências')
slide('digest','Consulta | Registry, tag e digest','Identificar o artefato que será promovido',[
 ('Registry','Armazena e distribui imagens.\npush publica; pull obtém.\nNão executa a aplicação.'),
 ('Tag','Nome legível de uma referência.\nPode mudar de alvo.\nlatest não significa conteúdo imutável.'),
 ('Digest','Identifica conteúdo.\nPermite registrar o artefato validado.\nEm imagens multiplataforma, registre também a plataforma.')],
 'Use node:22-bookworm-slim como exemplo: uma atualização do publicador pode mudar o conteúdo por trás da tag. O lockfile npm não fixa a imagem-base. Fixar digest ajuda a controlar atualização, mas exige política para receber correções. Não faça push para contas reais nesta aula. A distinção é relevante quando o mesmo artefato testado deve ser promovido, assunto do próximo encontro.',
 'Mesma tag não prova igualdade de conteúdo entre máquinas ou momentos diferentes.',section='Consulta',study_only=True)
slide('multistage','Consulta | Multi-stage e separação de responsabilidades','Exemplo conceitual de aplicação TypeScript • não é necessário na API do laboratório',[
 ('Estágio de build','Instala dependências de desenvolvimento.\nExecuta o compilador.\nGera o diretório dist/.'),
 ('Estágio de execução','Recebe dist/ e dependências de produção.\nExecuta com Node.\nNão precisa do compilador só para iniciar.'),
 ('Decisão','Inclua somente o necessário para executar.\nVerifique bibliotecas nativas e plataforma.\nNão presuma ganho de segurança só pelo número de estágios.')],
 'A API da aula é JavaScript sem compilação; um Dockerfile simples atende ao objetivo. Num projeto TypeScript, separar a construção permite excluir ferramentas usadas apenas para compilar. Em Java ou Go a forma do artefato será diferente. Isso não autoriza copiar um binário entre bases incompatíveis sem revisar suas bibliotecas. O aluno deve reconhecer quando o padrão é útil, sem ser obrigado a adicioná-lo ao projeto se ele não resolve um problema concreto.',
 'Multi-stage é uma escolha de empacotamento; use quando houver uma separação útil entre construir e executar.',section='Consulta',study_only=True)
slide('ci','Consulta | Verificar a imagem no CI','Evolução do pipeline já criado no Encontro 3',[
 ('Validar o código','Instalação controlada.\nTestes da aplicação.\nBuild quando a stack exige.'),
 ('Validar a execução','Construir a imagem.\nSubir dependências de teste.\nExecutar uma operação integrada.'),
 ('Registrar e encerrar','Identificar o artefato testado.\nGuardar logs pertinentes.\nEncerrar apenas os recursos do job, inclusive em falha.')],
 'Esta lâmina conecta o laboratório ao pipeline sem impor mais uma entrega no encontro. Um teste de integração em CI precisa de asserções e de tratamento da limpeza em falha; listar compose up seguido de down não garante por si só esse comportamento em qualquer executor. Dê preferência a um projeto Compose exclusivo por job para evitar colisões. Não use prune global ou remoção de volumes reais como rotina de limpeza. A publicação de artefato deve seguir as permissões e políticas do projeto.',
 'CI verde só comprova o que foi testado; executar a imagem amplia a evidência sobre o artefato.',section='Consulta',study_only=True)

# A experiência de persistência exige a stack já iniciada e validada.
experiment=next(d for d in S if d['id']=='persistence_demo')
S.remove(experiment)
S.insert(next(i for i,d in enumerate(S) if d['id']=='check_integration'),experiment)

from recursos_docker_e4 import ampliar
ampliar(S, slide)

for i,d in enumerate(S,1):
 d['source_id']=i
 d['question']= '\n'.join(d.get('questions',[]))
 d['answer']= '\n'.join(d.get('answers',[]))

REFS=[
 ('Visão geral do Docker','https://docs.docker.com/get-started/docker-overview/'),
 ('Containers e comparação com VMs','https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/'),
 ('Docker Engine','https://docs.docker.com/engine/'),
 ('Como Compose funciona','https://docs.docker.com/compose/intro/compose-application-model/'),
 ('containerd','https://containerd.io/'),
 ('runc e OCI','https://github.com/opencontainers/runc'),
 ('Dockerfile','https://docs.docker.com/reference/dockerfile/'),
 ('Cache','https://docs.docker.com/build/cache/invalidation/'),
 ('Boas práticas','https://docs.docker.com/build/building/best-practices/'),
 ('Rede','https://docs.docker.com/compose/how-tos/networking/'),
 ('Ordem de inicialização','https://docs.docker.com/compose/how-tos/startup-order/'),
 ('Volumes','https://docs.docker.com/engine/storage/volumes/'),
 ('Serviços e saúde','https://docs.docker.com/reference/compose-file/services/'),
 ('Variáveis de ambiente','https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/'),
 ('PostgreSQL oficial','https://hub.docker.com/_/postgres')]

REFS += [
 ('Limites de recursos','https://docs.docker.com/engine/containers/resource_constraints/'),
 ('Políticas de reinício','https://docs.docker.com/engine/containers/start-containers-automatically/'),
 ('Drivers de rede','https://docs.docker.com/engine/network/drivers/'),
 ('tmpfs','https://docs.docker.com/engine/storage/tmpfs/'),
 ('Profiles','https://docs.docker.com/compose/how-tos/profiles/'),
 ('Watch','https://docs.docker.com/compose/how-tos/file-watch/'),
 ('Combinar arquivos','https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/'),
 ('Secrets no Compose','https://docs.docker.com/compose/how-tos/use-secrets/'),
 ('BuildKit','https://docs.docker.com/build/buildkit/'),
 ('Buildx','https://docs.docker.com/build/concepts/overview/'),
 ('Contexts','https://docs.docker.com/engine/manage-resources/contexts/'),
 ('Scout','https://docs.docker.com/scout/'),
 ('Swarm','https://docs.docker.com/engine/swarm/'),
 ('Docker Desktop','https://docs.docker.com/desktop/')]
