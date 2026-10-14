#!/usr/bin/env python3
"""Verifica os guardrails do Project Planner contra o diff de um intervalo de commits.

Uso:
    python3 scripts/verificar-guardrails.py                 # compara com HEAD~1
    python3 scripts/verificar-guardrails.py --base <sha>    # compara com um commit
    python3 scripts/verificar-guardrails.py --staged        # compara HEAD com o que está staged

Sai com codigo 1 se algum guardrail for violado.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

DOCS_CONHECIDOS = {
    "00-brief.md", "01-discovery.md", "02-proposta.md", "03-features.md",
    "04-arquitetura.md", "05-roadmap.md", "decisoes.md",
}
ADAPTADORES = (".claude/commands", ".github/prompts", ".gemini/commands")
LIMITE_ADAPTADOR = 25

erros: list[str] = []
avisos: list[str] = []


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0:
        return ""
    return r.stdout


def resolver_base(base_arg: str | None, staged: bool) -> str | None:
    if staged:
        return "HEAD"
    for cand in (base_arg, os.environ.get("BASE_SHA")):
        if cand and not set(cand) <= {"0"} and git("rev-parse", "--verify", f"{cand}^{{commit}}"):
            return cand
    return "HEAD~1" if git("rev-parse", "--verify", "HEAD~1^{commit}") else None


def arquivos_alterados(base: str, staged: bool) -> list[tuple[str, str]]:
    args = ["diff", "--name-status", "--no-renames"]
    args += ["--cached", base] if staged else [base, "HEAD"]
    saida = git(*args)
    itens = []
    for linha in saida.splitlines():
        partes = linha.split("\t")
        if len(partes) >= 2:
            itens.append((partes[0][0], partes[-1]))
    return itens


def mensagens(base: str, staged: bool) -> str:
    if staged:
        return os.environ.get("COMMIT_MSG", "")
    return git("log", "--format=%B", f"{base}..HEAD")


def secao_decisoes(texto: str) -> str:
    m = re.search(r"^## Decis(?:õ|o)es\s*$(.*?)(?=^## |\Z)", texto, re.S | re.M)
    return m.group(1).rstrip() if m else ""


# ---------------------------------------------------------------- checagens

def checar_inputs(mudancas, msg):
    permitido = "[inputs-ok]" in msg or os.environ.get("ALLOW_INPUTS") == "1"
    for status, caminho in mudancas:
        if not caminho.startswith("inputs/"):
            continue
        if status == "A":
            continue  # trazer material novo é o uso esperado de inputs/
        if permitido:
            avisos.append(f"inputs/ alterado com autorização explícita: {caminho} ({status})")
        else:
            erros.append(
                f"`{caminho}` foi {'removido' if status == 'D' else 'modificado'}. "
                "inputs/ é somente leitura para a IA; só adição de arquivo é livre. "
                "Se a mudança é sua, inclua [inputs-ok] na mensagem do commit."
            )


def checar_templates(mudancas, msg):
    permitido = "[templates]" in msg or os.environ.get("ALLOW_TEMPLATES") == "1"
    alterados = [c for s, c in mudancas if c.startswith("templates/")]
    if alterados and not permitido:
        erros.append(
            "templates/ alterado sem autorização: " + ", ".join(f"`{c}`" for c in alterados) +
            ". Template só muda a pedido seu — inclua [templates] na mensagem do commit."
        )


def checar_decisoes_append_only(mudancas, base, staged):
    for status, caminho in mudancas:
        if status != "M" or not re.fullmatch(r"outputs/[^/]+/decisoes\.md", caminho):
            continue
        antigo = git("show", f"{base}:{caminho}")
        novo = Path(caminho).read_text(encoding="utf-8") if Path(caminho).exists() else ""
        if not antigo:
            continue
        sa, sn = secao_decisoes(antigo), secao_decisoes(novo)
        if sa and not sn.startswith(sa):
            erros.append(
                f"`{caminho}`: a seção `## Decisões` não é append-only — entradas anteriores "
                "foram alteradas ou removidas. Para mudar de ideia, adicione uma decisão nova "
                "e marque a antiga como substituída."
            )


def checar_estrutura():
    raiz = Path("outputs")
    if not raiz.is_dir():
        return
    for solto in raiz.glob("*.md"):
        if solto.name != "README.md":
            erros.append(f"`{solto}` está solto em outputs/. Todo documento vive em outputs/<slug>/.")
    for proj in sorted(p for p in raiz.iterdir() if p.is_dir()):
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", proj.name):
            erros.append(f"`{proj}`: nome de pasta não é um slug válido (kebab-case, sem acentos).")
        if not (proj / "decisoes.md").exists():
            erros.append(f"`{proj}` não tem decisoes.md — todo projeto precisa do seu log de decisões.")
        for doc in proj.glob("*.md"):
            if doc.name not in DOCS_CONHECIDOS:
                avisos.append(f"`{doc}` não é um documento previsto no fluxo.")


def checar_adaptadores():
    for prefixo in ADAPTADORES:
        pasta = Path(prefixo)
        if not pasta.is_dir():
            continue
        for arq in sorted(pasta.iterdir()):
            if not arq.is_file():
                continue
            n = len(arq.read_text(encoding="utf-8").splitlines())
            if n > LIMITE_ADAPTADOR:
                erros.append(
                    f"`{arq}` tem {n} linhas (limite {LIMITE_ADAPTADOR}). Adaptador aponta para "
                    "prompts/, não contém regra: regra duplicada sai de sincronia."
                )


def resumo_pendencias():
    raiz = Path("outputs")
    if not raiz.is_dir():
        return
    linhas = []
    for proj in sorted(p for p in raiz.iterdir() if p.is_dir()):
        texto = "".join(d.read_text(encoding="utf-8") for d in proj.glob("*.md"))
        a, s = texto.count("[A CONFIRMAR]"), texto.count("[SUPOSIÇÃO]")
        if a or s:
            linhas.append(f"  {proj.name}: {a} [A CONFIRMAR], {s} [SUPOSIÇÃO]")
    if linhas:
        print("\nPendências abertas (informativo, não reprova):")
        print("\n".join(linhas))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base")
    ap.add_argument("--staged", action="store_true")
    ns = ap.parse_args()

    base = resolver_base(ns.base, ns.staged)
    if base:
        mudancas = arquivos_alterados(base, ns.staged)
        msg = mensagens(base, ns.staged)
        print(f"Comparando com `{base}` — {len(mudancas)} arquivo(s) alterado(s).")
        checar_inputs(mudancas, msg)
        checar_templates(mudancas, msg)
        checar_decisoes_append_only(mudancas, base, ns.staged)
    else:
        print("Sem commit anterior para comparar: rodando só as checagens estruturais.")

    checar_estrutura()
    checar_adaptadores()

    for a in avisos:
        print(f"AVISO: {a}")
    if erros:
        print("\nGuardrails violados:\n")
        for e in erros:
            print(f"  ERRO: {e}\n")
        resumo_pendencias()
        return 1
    print("\nGuardrails OK.")
    resumo_pendencias()
    return 0


if __name__ == "__main__":
    sys.exit(main())
