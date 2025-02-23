from playwright.sync_api import Page, expect
from sudoku import Sudoku


def cook_the_sudoku(page: Page):
    boxes = page.locator('[data-testid^="sudoku-cell-"]').all()

    filledIndex = []
    filledValue = []

    for i, box in enumerate(boxes):
        label = box.get_attribute("aria-label")
        if label != "empty":
            filledIndex.append(i)
            filledValue.append(label)

    sudoku = Sudoku(filledIndex, filledValue)
    print("Initial Sudoku State")
    sudoku.visualize()
    new_value = sudoku.solve()
    print("\nSolved Sudoku State")
    sudoku.visualize()

    for i, box in enumerate(boxes):
        label = box.get_attribute("aria-label")
        box_class = box.get_attribute("class")
        if label == "empty":
            box_value = new_value[i]
            box.scroll_into_view_if_needed()

            if box_class and "selected" not in box_class.split():
                box.click()

            page.keyboard.type(str(box_value))


def test_sudoku(page: Page):
    page.goto("https://www.nytimes.com/puzzles/sudoku/easy")
    levels = ['easy', 'medium', 'hard']

    for level in levels:
        print(f"\n\nCurrent Level: {level}")
        popup = page.get_by_text("We’ve updated our terms")
        continueBtn = page.get_by_role("button", name="Continue")

        if popup.is_visible():
            continueBtn.click()

        cook_the_sudoku(page)

        congratsPopup = page.get_by_test_id("header")
        congratsPopup.wait_for(state="visible", timeout=5000)
        if congratsPopup.is_visible() and level != "hard":
            page.get_by_test_id("btn-play-another-sudoku").click()

    page.pause()
