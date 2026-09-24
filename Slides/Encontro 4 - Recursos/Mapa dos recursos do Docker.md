# Mapa dos recursos do Docker

Cada recurso aparece associado a finalidade, exemplo e explicação. Os itens E4·70–78 são consulta.

| Recurso | Finalidade | Exemplo | Slides |
|---|---|---|---|
| Imagens e construção | Empacotar aplicação e dependências. | docker build -t e4-api:local . | E4·27–33 |
| Runtime e containers | Preparar processos isolados e operar instâncias. | run, stop, start e rm | E4·10–22 |
| Inspeção e comandos | Observar logs/estado e executar uma verificação. | logs, inspect, exec e stats | E4·21 |
| Rede e portas | Conectar componentes e expor uma entrada. | app → db:5432; host:8080 → app:3000 | E4·39–40 |
| Configuração e privilégios | Entregar valores e reduzir acessos desnecessários. | environment, USER, :ro, secrets | E4·41–42 |
| Persistência | Manter dados além da instância. | volume dados e bind mount init.sql | E4·43 |
| Saúde e partida | Observar um contrato e coordenar início. | healthcheck; depends_on com service_healthy | E4·44–46 |
| CPU e memória | Restringir consumo e observar comportamento. | cpus: 0.50; mem_limit: 256m | E4·47 |
| Reinício | Reagir à saída do processo. | no, on-failure, always, unless-stopped | E4·48 |
| Compose | Declarar e operar serviços e recursos. | config; up; ps; logs; down | E4·49 |
| Registry, tags e digest | Distribuir e identificar o artefato. | pull / tag / push; referência por digest | E4·70 |
| Multi-stage e CI | Separar construção/execução e testar imagem. | Estágio de build → artefato → estágio final | E4·71–72 |
| tmpfs | Montar temporários sem persistência após parada. | tmpfs: /tmp (Linux) | E4·73 |
| Drivers de rede | Adequar conectividade à infraestrutura. | bridge, host, none, overlay, macvlan/ipvlan | E4·74 |
| Profiles | Selecionar serviços opcionais. | --profile ferramentas | E4·75 |
| Overrides e Watch | Adaptar configuração e ciclo de desenvolvimento. | -f; develop.watch; config | E4·76 |
| BuildKit / Buildx | Usar cache e construir para plataformas escolhidas. | Cache mounts e seleção de plataforma | E4·77 |
| Outras ferramentas | Conhecer possibilidades além do laboratório. | Contexts, Scout, Swarm e Dashboard | E4·78 |

O laboratório não exige todas as opções. Escolha e justifique as pertinentes à aplicação, validando seu comportamento. Os links oficiais estão no guia ampliado.
