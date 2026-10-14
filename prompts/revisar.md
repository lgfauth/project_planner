# Procedimento: revisar

Auditar os documentos de um projeto em busca de lacunas e contradições.

## Argumentos

O **argumento** é o `slug`. Se não vier, pergunte qual projeto.

> Procedimento neutro: vale para qualquer assistente de IA.
> Leia `prompts/guardrails.md` antes de executar qualquer passo.

Leia `outputs/<slug>/decisoes.md` primeiro e depois todos os `.md` de `outputs/<slug>/`.
Não leia outros projetos. Produza um relatório com:

1. **Cobertura** — documentos presentes/ausentes, seções do template vazias, blocos de brainstorm
   ainda não cobertos segundo o log.
2. **Lacunas** — todos os `[A CONFIRMAR]` e `[SUPOSIÇÃO]` mais as pendências do log, agrupados
   e ordenados por impacto na decisão.
3. **Aderência ao log** — todo documento reflete as decisões vigentes? Alguma decisão
   `substituída` ainda aparece como válida em algum texto? Alguma decisão do log não chegou
   a documento nenhum?
4. **Contradições** — divergências entre documentos (feature da v1 ausente da fase 1 do roadmap,
   métrica de sucesso que nenhuma feature move, escopo que contradiz uma restrição declarada).
5. **Rastreabilidade** — toda feature de `03-features.md` liga a um problema de `01-discovery.md`
   e aparece em alguma fase de `05-roadmap.md`. Liste as órfãs.
6. **Realismo** — onde o plano parece otimista demais frente às restrições declaradas.

Apenas **relate**: não corrija arquivos nem escreva no log neste comando.
Ao final, pergunte o que o usuário quer ajustar.

Siga os guardrails em `prompts/guardrails.md`.
