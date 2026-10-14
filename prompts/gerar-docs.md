# Procedimento: gerar-docs

Gerar ou atualizar os documentos de planejamento a partir dos templates.

## Argumentos

O **primeiro argumento** é o `slug`; o **segundo** (opcional) é o documento
(`proposta`, `features`, `arquitetura`, `roadmap` ou `todos`; padrão `todos`).

> Procedimento neutro: vale para qualquer assistente de IA.
> Leia `prompts/guardrails.md` antes de executar qualquer passo.

## Antes de escrever (obrigatório)

1. Leia `outputs/<slug>/decisoes.md` **primeiro**: as decisões vigentes mandam no conteúdo.
   Decisão marcada como `substituída` não entra no documento.
2. Leia os documentos já existentes em `outputs/<slug>/` e **preserve as decisões neles registradas**.
   Não leia pasta de outro projeto.
3. **Pré-condição:** `01-discovery.md` deve existir e não pode estar dominado por `[A CONFIRMAR]`
   nas seções de problema, usuário e sucesso. Se estiver, pare e chame `/brainstorm <slug>`.
4. Se alguma decisão do log for posterior à data de um documento já gerado, avise que ele está
   desatualizado antes de regravá-lo.

## Geração

- Padrão: `todos` — exceto `04-arquitetura.md`, gerado só quando houver decisão técnica real
  registrada no log ou quando for pedido explicitamente.
- Um documento por vez: siga o template correspondente em `templates/`, mostre um resumo do que
  decidiu e só então passe ao próximo.
- Marque lacunas com `[A CONFIRMAR]` e inferências com `[SUPOSIÇÃO]`. Não invente dados.
- No cabeçalho de cada documento gerado, atualize `data` e `versao`, e registre em
  `Origem: decisões D0xx–D0yy` quais decisões sustentam aquela versão.

## Depois

1. Registre em `decisoes.md` (histórico de sessões) o que foi gerado e com base em quais decisões.
   Se durante a geração surgirem escolhas novas, registre-as como decisões próprias.
2. Rode a checagem de `/revisar <slug>` e informe as pendências.

Siga os guardrails em `prompts/guardrails.md`.
