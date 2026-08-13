import { Page, Locator } from "@playwright/test";

export class LessonPage {
  readonly page: Page;
  readonly startLessonButton: Locator;
  readonly checkButton: Locator;
  readonly continueButton: Locator;
  readonly exitButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.startLessonButton = page.locator("button:has-text('START LESSON')");
    this.checkButton = page.locator("button:has-text('CHECK')");
    this.continueButton = page.locator("button:has-text('CONTINUE')");
    this.exitButton = page.locator("button[aria-label='Exit lesson']");
  }

  async startLesson() {
    await this.startLessonButton.click();
  }

  async selectOption(optionText: string) {
    await this.page.click(`button:has-text("${optionText}")`);
  }

  async clickCheck() {
    await this.checkButton.click();
  }

  async clickContinue() {
    await this.continueButton.click();
  }
}
