# Procedimento: novo-projeto

Iniciar o planejamento de um projeto novo.

## Argumentos

O **argumento** é o nome do projeto. Se não vier, pergunte e pare.

> Procedimento neutro: vale para qualquer assistente de IA.
> Leia `prompts/guardrails.md` antes de executar qualquer passo.

Passos:

1. Derive o `slug` (kebab-case, sem acentos) a partir do nome. Se o argumento estiver vazio,
   pergunte o nome do projeto e pare.
2. Verifique se `outputs/<slug>/` já existe. Se existir, avise, leia `outputs/<slug>/decisoes.md`
   e pergunte se é para continuar o planejamento existente. **Não sobrescreva nada sem confirmação.**
3. Liste `inputs/` e diga ao usuário quais arquivos encontrou e quais parecem relacionados a este
   projeto. Não leia tudo ainda — apenas mapeie.
4. Pergunte ao usuário, em uma única mensagem, no máximo 3 coisas:
   - Qual é a ideia em uma frase?
   - Qual dor/problema motiva ela?
   - Quem é o usuário/cliente final?
5. Com as respostas, crie:
   - `outputs/<slug>/00-brief.md` a partir de `templates/00-brief.md`
   - `outputs/<slug>/decisoes.md` a partir de `templates/decisoes.md`, com o cabeçalho preenchido,
     fase `brief`, a primeira linha do histórico de sessões e as pendências já visíveis.
   Preencha apenas o que foi dito; o resto fica `[A CONFIRMAR]`.
6. Encerre declarando o slug ativo e sugerindo `/brainstorm <slug>`.
   **Não gere os demais documentos agora.**

Siga os guardrails em `prompts/guardrails.md`.
