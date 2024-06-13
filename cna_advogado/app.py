from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# timeout excepion
from selenium.common.exceptions import TimeoutException
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class NameRequest(BaseModel):
    name: str


def run(name: str) -> dict:
    # Start WebDriver
    with webdriver.Chrome() as driver:
        # Navigate to the website
        driver.get("https://cna.oab.org.br/")

        # Find "Nome" element and input the name
        nome_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="txtName"]'))
        )
        nome_element.click()
        driver.find_element(By.CSS_SELECTOR, "#txtName").send_keys(name)
        driver.find_element(By.CSS_SELECTOR, "#btnFind").click()

        results = []
        try:
            # Find and extract data from result elements
            result_elements = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "#divResult > div")
                )
            )
            for result_element in result_elements:
                nome = result_element.find_element(
                    By.CSS_SELECTOR, "div.rowName > span:nth-child(2)"
                ).text
                tipo = result_element.find_element(
                    By.CSS_SELECTOR, "div.rowTipoInsc > span:nth-child(3)"
                ).text
                inscricao = result_element.find_element(
                    By.CSS_SELECTOR, "div.rowInsc > span:nth-child(3)"
                ).text
                uf = result_element.find_element(
                    By.CSS_SELECTOR, "div.rowUf > span:nth-child(3)"
                ).text
                results.append(
                    {"Nome": nome, "TIPO": tipo, "INSCRICAO": inscricao, "UF": uf}
                )
        except TimeoutException:
            raise HTTPException(status_code=404, detail="Nenhum resultado encontrado")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")

        return results if results else {"message": "Nenhum resultado encontrado"}


@app.post("/search")
def search_name(request: NameRequest):
    result = run(request.name)
    return result


if __name__ == "__main__":
    print(run("string"))
