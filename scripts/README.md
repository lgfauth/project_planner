# scripts/

Ferramentas de verificação do repositório. Não fazem parte do planejamento — existem só para
garantir, de fora da IA, o que os guardrails pedem de dentro dela.

## `verificar-guardrails.py`

Roda no CI ([.github/workflows/guardrails.yml](../.github/workflows/guardrails.yml)) e também
na sua máquina:

```bash
python3 scripts/verificar-guardrails.py                # compara com HEAD~1
python3 scripts/verificar-guardrails.py --base main    # compara com um branch/commit
python3 scripts/verificar-guardrails.py --staged       # compara com o que está staged
```

### O que ele reprova

| Checagem | Regra | Como autorizar a exceção |
|---|---|---|
| `inputs/` somente leitura | Adicionar arquivo é livre; **modificar ou apagar reprova** | `[inputs-ok]` na mensagem do commit |
| `templates/` protegido | Qualquer alteração reprova | `[templates]` na mensagem do commit |
| `decisoes.md` append-only | A seção `## Decisões` só pode crescer; reescrever entrada anterior reprova | não há — adicione uma decisão nova que substitui a antiga |
| Estrutura de `outputs/` | Nada solto na raiz, pasta em kebab-case, todo projeto com `decisoes.md` | — |
| Adaptadores finos | Arquivo em `.claude/commands/`, `.github/prompts/` ou `.gemini/commands/` acima de 25 linhas reprova | — |

`Estado atual`, pendências e histórico de sessões **podem** ser reescritos: só o corpo das
decisões é imutável.

Avisos (não reprovam): documento fora do fluxo previsto em uma pasta de projeto, e o total de
`[A CONFIRMAR]` / `[SUPOSIÇÃO]` por projeto.

### Rodar antes de cada commit (opcional)

```bash
printf '#!/bin/sh\npython3 scripts/verificar-guardrails.py --staged\n' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

No modo `--staged` não existe mensagem de commit ainda: use `ALLOW_INPUTS=1` ou
`ALLOW_TEMPLATES=1` para autorizar uma exceção pontual.
