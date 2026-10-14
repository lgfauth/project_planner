# Project Planner — instruções para agentes de IA

Repositório de **planejamento de projetos**. Aqui não se escreve código de produção:
a saída deste repositório são **documentos de planejamento em Markdown**.

## Estrutura

| Pasta | Papel | Quem escreve |
|---|---|---|
| `inputs/` | Material de referência trazido pelo usuário (docs, notas, pesquisas, transcrições, prints) | **Somente o usuário** |
| `templates/` | Modelos que definem a estrutura de cada documento gerado | Usuário (a IA só altera se pedido) |
| `outputs/<slug-do-projeto>/` | Documentos finais de cada projeto planejado | A IA |
| `prompts/` | Guardrails e procedimentos, em Markdown neutro | Usuário + IA |

## Fluxo de trabalho

1. **`/novo-projeto <nome>`** — cria `outputs/<slug>/` e o `00-brief.md` com a ideia bruta.
2. **`/brainstorm <slug> [tema]`** — entrevista socrática para transformar a ideia em decisões.
   Nenhum documento final é escrito antes desta etapa. Com `tema`, a sessão foca um único bloco
   (`problema`, `sucesso`, `escopo`, `restricoes`, `riscos`, `alternativas`).
3. **`/gerar-docs`** — materializa os documentos a partir dos `templates/`.
4. **`/revisar`** — checa consistência, lacunas e suposições não resolvidas.
5. **`/status`** — mostra em que ponto cada projeto está.

## Documentos gerados por projeto

| Arquivo | Responde a pergunta |
|---|---|
| `00-brief.md` | Qual é a ideia, em estado bruto? |
| `01-discovery.md` | Qual o problema real, para quem, e o que já sabemos? |
| `02-proposta.md` | Qual a solução proposta, o escopo e o que fica de fora? |
| `03-features.md` | O que exatamente será construído, priorizado e com critérios de aceite? |
| `04-arquitetura.md` | Como será construído tecnicamente? (opcional) |
| `05-roadmap.md` | Em que fases isso é entregue e implantado? |
| `decisoes.md` | O que já foi decidido, por quê, e o que ainda está aberto? |

## Memória do projeto

Cada projeto tem seu próprio `outputs/<slug>/decisoes.md` — log append-only de decisões,
pendências e sessões. **É o primeiro arquivo lido por qualquer comando** e é o que permite
intercalar brainstorms e gerações sem repetir perguntas nem perder o motivo de cada escolha.

O log é exclusivo do projeto: decisão de um planejamento nunca vale para outro, e cada sessão
trabalha com um único slug ativo, declarado no início da resposta.

## Como executar os comandos

Cada comando do fluxo é um **procedimento neutro** em `prompts/`, válido para qualquer assistente:

| Comando | Procedimento |
|---|---|
| `/novo-projeto <nome>` | `prompts/novo-projeto.md` |
| `/brainstorm <slug> [tema]` | `prompts/brainstorm.md` |
| `/gerar-docs <slug> [doc]` | `prompts/gerar-docs.md` |
| `/revisar <slug>` | `prompts/revisar.md` |
| `/status` | `prompts/status.md` |

Se a sua ferramenta não tiver comandos de barra, basta pedir em linguagem natural:
*"execute o procedimento de `prompts/brainstorm.md` para o projeto `portal-do-cliente`, tema riscos"*.

**As regras de `prompts/guardrails.md` valem sempre**, com comando ou sem comando.
Leia esse arquivo antes de escrever qualquer coisa em `outputs/`.

## Configuração por ferramenta

Os arquivos abaixo são **adaptadores finos**: apontam para `prompts/` e não contêm regra própria.
Ao mudar uma regra, mude em `prompts/` — nunca no adaptador.

| Ferramenta | Arquivos |
|---|---|
| Claude Code | `CLAUDE.md`, `.claude/commands/*.md` |
| Copilot Chat | `.github/copilot-instructions.md`, `.github/prompts/*.prompt.md` |
| Gemini CLI | `.gemini/commands/*.toml` (contexto via este `AGENTS.md`) |
| Codex e outros | este `AGENTS.md` |

