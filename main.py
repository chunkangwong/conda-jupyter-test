from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time

QUESTION_CLASS = "._2sv26PNy"
RATIONALE_CLASS = "._258b_SOg p"
ANSWERS_CLASS = "fieldset ._2GF7gJr9"
QUESTION_ID_CLASS = "._1xYxGLT9"
PROGRESS_CLASS = "._25ux-wEX"
NEXT_QUESTION_BUTTON_CLASS = ".lo-7FUSc ._1akKA3CB"
RADIO_BUTTON_CLASS = "._2Jz8gM21"


def answer_question(driver: WebDriver):
    radio_button_elems = driver.find_element(By.CSS_SELECTOR, RADIO_BUTTON_CLASS)
    radio_button_elems.click()
    click_button(driver, "Submit")


def extract_question(driver: WebDriver):
    question = driver.find_element(By.CSS_SELECTOR, QUESTION_CLASS).text
    rationale = driver.find_element(By.CSS_SELECTOR, RATIONALE_CLASS).text
    answer_elems = driver.find_elements(By.CSS_SELECTOR, ANSWERS_CLASS)
    answers = [elem.text for elem in answer_elems]
    question_id = driver.find_element(By.CSS_SELECTOR, QUESTION_ID_CLASS).text.split(
        " "
    )[1]
    return {
        "question": question,
        "rationale": rationale,
        "answers": answers,
        "question_id": question_id,
    }


def click_button(driver: WebDriver, button_text: str):
    button_elems = driver.find_elements(By.CSS_SELECTOR, NEXT_QUESTION_BUTTON_CLASS)
    for button_elem in button_elems:
        if button_elem.text == button_text and button_elem.is_enabled():
            button_elem.click()
            return True
    return False


def write_question(question):
    filename = "01.json"
    with open(filename, "r") as file:
        data = json.load(file)
    data.append(question)
    with open(filename, "w") as file:
        json.dump(data, file)


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)

    to_continue = True
    to_answer = False
    while to_continue:
        if to_answer:
            answer_question(driver)
            time.sleep(0.3)
        question = extract_question(driver)
        print(question["question"])
        write_question(question)
        to_continue = click_button(driver, "Next Question")
        time.sleep(0.3)


if __name__ == "__main__":
    main()
