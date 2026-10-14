# outputs/

Documentos finais de planejamento, um diretório por projeto.

```
outputs/
└── <slug-do-projeto>/
    ├── 00-brief.md          ideia bruta
    ├── 01-discovery.md      problema, personas, riscos, sucesso
    ├── 02-proposta.md       solução, escopo, trade-offs
    ├── 03-features.md       backlog priorizado com critérios de aceite
    ├── 04-arquitetura.md    decisões técnicas (opcional)
    ├── 05-roadmap.md        fases, critérios de saída e implantação
    └── decisoes.md          log append-only: decisões, motivos e pendências
```

## `decisoes.md`

A memória do projeto entre sessões, e o primeiro arquivo lido por qualquer comando.
Cada entrada registra a decisão, o motivo e a alternativa descartada; nada é reescrito —
mudar de ideia significa adicionar uma decisão nova que substitui a anterior.

Por ser um arquivo por projeto, planejamentos em paralelo não se contaminam: o comando lê
apenas o log do slug ativo.

## Marcações usadas nos documentos

| Marcação | Significa |
|---|---|
| `[A CONFIRMAR]` | Lacuna aberta — ninguém decidiu ainda |
| `[SUPOSIÇÃO]` | Inferência da IA, precisa de validação sua |
| `[FONTE: inputs/x]` | Informação veio de um material em `inputs/` |

Rode `/revisar <slug>` para ver todas as pendências de um projeto e `/status` para o painel geral.
(Em ferramentas sem comandos de barra, peça o procedimento equivalente em `prompts/`.)
