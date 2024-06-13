import re
from playwright.sync_api import Playwright, sync_playwright, expect
import typer
import time

app = typer.Typer()


def run(playwright: Playwright, name: str) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://cna.oab.org.br/")
    page.get_by_label("Nome").click()
    page.get_by_label("Nome").fill(name)
    page.get_by_role("button", name="Pesquisar").click()
    # get by selector
    try:
        nome_selector = page.wait_for_selector(
            "#divResult > div > div.rowName > span:nth-child(2)"
        ).text_content()
        tipo = page.wait_for_selector(
            "#divResult > div > div.rowTipoInsc > span:nth-child(3)"
        ).text_content()
        inscricao = page.wait_for_selector(
            "#divResult > div > div.rowInsc > span:nth-child(3)"
        ).text_content()
        uf = page.wait_for_selector(
            "#divResult > div > div.rowUf > span:nth-child(3)"
        ).text_content()
    except Exception:
        raise ValueError("Usuario não encontrado")

    # write to excel
    with open("cna.txt", "a") as f:
        f.write(f"Nome: {nome_selector};TIPO: {tipo};INSCRICAO: {inscricao};UF: {uf}\n")


@app.command()
def main():
    name = typer.prompt("Digite o nome")
    with sync_playwright() as playwright:
        run(playwright, name)


if __name__ == "__main__":
    app()
