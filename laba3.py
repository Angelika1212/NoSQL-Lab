from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import wikipedia
from wikipedia.exceptions import WikipediaException
from json import dump


def configuration():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options)
    driver.get("https://ru.wikipedia.org/wiki/Список_действующих_глав_государств_и_правительств")
    return driver


def extract_data_from_tables(driver):
    tables = driver.find_elements(By.TAG_NAME, "table")
    print(f"Найдено таблиц: {len(tables)}")

    result_data = []

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        row_number = 1  # Без заголовка

        while row_number < len(rows):

            country_data = {
                "country": "",
                "leader": {}
            }

            cells = rows[row_number].find_elements(By.TAG_NAME, "td")

            country = cells[1].text
            rowspan = get_rowspan_number(cells[1])
            country_data["country"] = country
            leader_data = {}

            header = cells[2].get_attribute("colspan")
            if header is not None:
                if int(header) == 6:
                    cells = rows[row_number + 1].find_elements(By.TAG_NAME, "td")
                    leader_info = cells[1].find_elements(By.TAG_NAME, "a")[0]
                    board_date = cells[2].find_elements(By.TAG_NAME, "a")[0].get_attribute("title")

                    leader_data = {
                        "name": leader_info.get_attribute("title"),
                        "role": cells[0].text,
                        "board_date": int(board_date.split()[0]),
                        "article": leader_info.get_attribute("href"),
                        "reference_data": ""
                    }

            else:
                leader_info = cells[3].find_elements(By.TAG_NAME, "a")[0]
                board_date = cells[4].find_elements(By.TAG_NAME, "a")[0].get_attribute("title")

                leader_data = {
                    "name": leader_info.get_attribute("title"),
                    "role": cells[2].text,
                    "board_date": int(board_date.split()[0]),
                    "article": leader_info.get_attribute("href"),
                    "reference_data": get_leader_info(leader_info.get_attribute("title"))
                }

            country_data["leader"] = leader_data
            print(country_data)
            result_data.append(country_data)
            row_number = row_number + (1 if rowspan is None else rowspan)
    return result_data


def get_rowspan_number(elem):
    try:
        rowspan = elem.get_attribute("rowspan")
        if rowspan:
            return int(rowspan)
    except:
        pass
    return None


def get_leader_info(leader_name, lang='ru'):
    try:
        wikipedia.set_lang(lang)
        page = wikipedia.page(leader_name)
        summary = page.summary
        if len(summary) > 500:
            summary = summary[:500] + "..."
        return summary
    except WikipediaException as e:
        print(f"Ошибка Wikipedia API для {leader_name}: {e}")
        return ""
    except Exception as e:
        print(f"Общая ошибка для {leader_name}: {e}")
        return ""


def save_to_json(data, filename="data.json"):
    with open(filename, "w") as outfile:
        dump(data, outfile)


if __name__ == "__main__":
    main_driver = configuration()
    main_data = extract_data_from_tables(main_driver)
    save_to_json(main_data)
    main_driver.quit()
