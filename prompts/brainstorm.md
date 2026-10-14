# Procedimento: brainstorm

Conduzir a entrevista de descoberta que transforma a ideia em decisões.

## Argumentos

O **primeiro argumento** é o `slug` do projeto; o **segundo** (opcional) é o tema da sessão.
Se o slug não vier, liste `outputs/` e pergunte qual projeto — não presuma.

> Procedimento neutro: vale para qualquer assistente de IA.
> Leia `prompts/guardrails.md` antes de executar qualquer passo.

## Antes de qualquer pergunta (obrigatório)

1. Leia `outputs/<slug>/decisoes.md` **primeiro**. Ele diz o que já foi decidido, quais blocos
   já foram cobertos e o que está pendente. **Nunca repita uma pergunta já respondida no log.**
2. Leia os demais documentos existentes em `outputs/<slug>/`. Não leia pasta de outro projeto.
3. Leia os arquivos de `inputs/` relevantes a este projeto, citando-os como `[FONTE: ...]`.
4. Abra a sessão com: slug ativo, o que já está decidido (3–5 linhas), o que está pendente,
   e o que esta sessão vai cobrir. Peça correção antes de seguir.

## A entrevista

**Com tema informado:** trabalhe só aquele bloco, a fundo. Sessão curta e focada vale mais
que uma varredura rasa dos seis.

**Sem tema:** proponha o próximo bloco ainda não coberto segundo o log, e confirme com o usuário.

Blocos:

1. **problema** — quem sofre, com que frequência, qual o custo de não resolver, como resolvem hoje.
2. **sucesso** — como saberemos que deu certo; que métrica muda; qual o número mínimo aceitável.
3. **escopo** — o que é essencial na v1 e o que é explicitamente adiado.
4. **restricoes** — orçamento, prazo, time, stack obrigatória, exigências legais/LGPD.
5. **riscos** — o que pode matar o projeto; qual a premissa mais frágil.
6. **alternativas** — a solução mais burra que resolveria 80%; comprar vs. construir.

Regras da entrevista:
- Máximo 3 perguntas por mensagem.
- Resposta vaga → ofereça 2–3 opções concretas com trade-offs, não repita a pergunta.
- Desafie: aponte quando algo parecer caro, arriscado ou desnecessário para a v1.
- **Registre cada decisão em `decisoes.md` assim que ela for tomada** (append, com motivo e
  alternativa descartada). Não acumule para o fim da sessão.
- Se uma decisão nova contradisser uma anterior, crie a nova entrada e marque a antiga como
  `substituída por D0xx`, avisando quais documentos ficam desatualizados.

## Fechamento

1. Atualize `outputs/<slug>/01-discovery.md` (base: `templates/01-discovery.md`) com o que foi
   decidido, marcando `[SUPOSIÇÃO]` e `[A CONFIRMAR]` onde couber.
2. Atualize em `decisoes.md`: **Estado atual**, tabela de **pendências** e **histórico de sessões**.
3. Liste as pendências que ainda bloqueiam a proposta e sugira o próximo comando
   (outro `/brainstorm <slug> <tema>` ou `/gerar-docs <slug>`).

Siga os guardrails em `prompts/guardrails.md`.
