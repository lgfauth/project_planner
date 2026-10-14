# Project Planner

Repositório para transformar ideias em planejamento de projeto conversando com a IA:
insights, proposta, features e plano de implantação por fases — tudo em Markdown versionável.

## Como funciona

```
inputs/     material que você traz      →  lido
templates/  a forma dos documentos      →  seguido
outputs/    o planejamento produzido    →  escrito
prompts/    guardrails e procedimentos  →  as regras do jogo
```

## Funciona com qualquer IA

As regras e os procedimentos vivem em `prompts/`, em Markdown neutro. `AGENTS.md` é o ponto
de entrada padrão; cada ferramenta tem só um adaptador fino, sem regra própria:

| Ferramenta | Configuração | Comandos de barra |
|---|---|---|
| Claude Code | `CLAUDE.md` | `.claude/commands/` |
| Copilot Chat | `.github/copilot-instructions.md` | `.github/prompts/` |
| Gemini CLI | `AGENTS.md` | `.gemini/commands/` |
| Codex e outros | `AGENTS.md` | peça em linguagem natural |

Sem comandos de barra, funciona igual:
*"execute o procedimento de `prompts/brainstorm.md` para o projeto `portal-do-cliente`"*.

**Ao mudar uma regra, mude em `prompts/` — nunca no adaptador.**

## Rede de segurança

Guardrail é instrução: a IA cumpre porque leu, não porque foi impedida. Fora do Claude Code
nem isso é garantido. Por isso as regras críticas também são verificadas por fora, no CI e
opcionalmente antes de cada commit:

```bash
python3 scripts/verificar-guardrails.py
```

Ele reprova alteração em `inputs/` e `templates/` sem autorização explícita, reescrita de
decisão já registrada em `decisoes.md`, documento solto em `outputs/` e adaptador que virou
cópia de regra. Detalhes em [scripts/README.md](scripts/README.md).

## Uso

```
/novo-projeto Portal do Cliente    # cria outputs/portal-do-cliente/ e o brief
/brainstorm portal-do-cliente      # entrevista de descoberta (o coração do processo)
/brainstorm portal-do-cliente riscos   # sessão curta, focada em um único bloco
/gerar-docs portal-do-cliente      # gera proposta, features, arquitetura e roadmap
/revisar portal-do-cliente         # audita lacunas, contradições e rastreabilidade
/status                            # painel de todos os projetos
```

Nada impede uma conversa livre — os comandos apenas garantem que o resultado siga
sempre a mesma estrutura e as mesmas regras.

## Princípios

1. **Conversa antes de documento.** Documento gerado cedo demais vira ficção.
2. **Lacuna declarada vale mais que texto genérico.** `[A CONFIRMAR]` é uma resposta legítima.
3. **Nada é inventado.** Números, prazos e fontes ou vêm de você, ou de `inputs/`, ou são marcados.
4. **Aqui não se implementa.** A saída é plano, não código.
5. **Cada projeto guarda sua própria memória.** `outputs/<slug>/decisoes.md` registra o que foi
   decidido e por quê, é lido antes de qualquer comando e nunca cruza com outro projeto.

Por isso a ordem dos comandos é livre: brainstorm, gerar, voltar ao brainstorm e gerar de novo
é o uso esperado — o log garante que nada seja perguntado duas vezes nem sobrescrito sem aviso.

As regras completas estão em [prompts/guardrails.md](prompts/guardrails.md).
