# Procedimento: status

Mostrar o painel de todos os projetos em `outputs/`.

> Procedimento neutro: vale para qualquer assistente de IA.
> Leia `prompts/guardrails.md` antes de executar qualquer passo.

1. Liste as pastas de `outputs/`. Para cada projeto, leia **apenas** o cabeçalho
   (**Estado atual** e últimas linhas do histórico) do seu `decisoes.md` — não é preciso abrir
   os documentos inteiros, e projetos não se misturam.
2. Monte uma tabela: projeto (slug), fase, documentos presentes (00→05), nº de decisões,
   nº de pendências abertas, última sessão, próximo passo sugerido.
3. Sinalize projetos cujo `decisoes.md` tenha decisão mais recente que a data do último documento
   gerado — são planos com documentação desatualizada.
4. Liste os arquivos de `inputs/` que não aparecem como `[FONTE: ...]` em nenhum projeto —
   material trazido e não aproveitado.
5. Seja conciso: uma tabela e, no máximo, três linhas de comentário.
   Se o usuário quiser detalhe de um projeto, sugira `/revisar <slug>`.
