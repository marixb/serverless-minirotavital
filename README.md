# Atividade Individual 1 – Serverless (Rota Vital)

**Aluna:** Mariana Xavier · Infraestrutura de Software · ADS · CESAR School · 2026.2
**Caminho escolhido:** A – AWS SAM CLI local (Docker + Python 3.12)
**Vídeo:** <https://drive.google.com/file/d/1BjAm2fJNRnTUjm2ZiL6IbkduBkenhgu5/view?usp=sharing> 

## Como rodar
Pré-requisitos: Docker Desktop, AWS SAM CLI, Python 3.12. No Windows, usar Git Bash.

    sam build
    sam local invoke -e events/pedido.json
    sam local start-api            # ou: sam local start-api --warm-containers LAZY
    curl -X POST http://127.0.0.1:3000/guias -H "Content-Type: application/json" \
      -d '{"requisicaoId":"R-002","hospital":"H-Caruaru"}'

## Resultados
| Experimento | Resultado |
|---|---|
| 1ª invocação (invoke) | X ms / X s |
| 2ª invocação (invoke) | X ms / X s |
| start-api sem warm (3 curls) | invocacaoNesteAmbiente = 1, 1, 1 |
| start-api com --warm-containers LAZY | 1, 2, 3 |
| demorar=true com Timeout 3 | erro: timed out after 3 seconds (502) |
| demorar=true com Timeout 10 | 201 após ~5 s |

Prints em `evidencias/`.

## Respostas
**1. Por que a primeira invocação demorou mais?**
Foi um cold start. Na fase de Init, o ambiente de execução precisa ser criado: o container sobe, o runtime Python inicia e o código fora do handler roda (imports e variáveis globais). Na segunda vez parte disso já estava pronto (imagem baixada/em cache), então foi mais rápido.

**2. O que mostrou o invocacaoNesteAmbiente?**
Sem --warm-containers ficou sempre 1, porque cada chamada criou um ambiente novo. Com LAZY foi 1, 2, 3, porque o mesmo ambiente foi reaproveitado e a variável global continuou na memória. Isso mostra que não dá pra confiar em variável global para guardar estado: ela só continua existindo se o ambiente for reaproveitado, e isso não é garantido. Estado tem que ir para um banco ou cache externo (ex.: DynamoDB).

**3. O que aconteceu com demorar = true?**
A função dormiu 5 s, passou do Timeout de 3 s e foi encerrada com erro. Com Timeout 10, funcionou. O máximo no Lambda é 15 minutos (900 s). Para trabalho mais longo: dividir em etapas com Step Functions, processar em partes com fila (SQS), ou usar container/ECS/Fargate/AWS Batch.

**4. Custo de 1 milhão de execuções (128 MB, 100 ms)**
- Requisições: 1.000.000 × 0,20 / 1.000.000 = **US$ 0,20**
- GB-s: 0,125 GB × 0,1 s × 1.000.000 = 12.500 GB-s
- Computação: 12.500 × 0,0000166667 = **US$ 0,21**
- **Total ≈ US$ 0,41** (sem contar o nível gratuito, que cobriria tudo isso)

**5. Onde faz sentido no Rota Vital?**
Faz sentido em tarefas curtas e disparadas por evento, como gerar a guia de transporte quando chega uma requisição de bolsa, mandar notificações ao hospital ou validar um pedido. Não faz sentido no que precisa de conexão contínua ou estado na memória, como o rastreamento em tempo real do transporte ou processos longos que passem de 15 min.

## Uso de IA
- **Ferramenta:** Claude (Anthropic)
- **Finalidade:** roteiro dos passos de execução no Linux, revisão da conta de custo e rascunho da estrutura do README.
- **Como validei:** executei todos os comandos, conferi as saídas (prints em `evidencias/`), refiz a conta de custo e reescrevi as respostas com minhas palavras.