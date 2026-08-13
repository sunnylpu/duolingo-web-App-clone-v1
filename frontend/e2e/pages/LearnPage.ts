import { Page, Locator } from "@playwright/test";

export class LearnPage {
  readonly page: Page;
  readonly recommendedSkillNode: Locator;
  readonly headerStreak: Locator;
  readonly headerXP: Locator;
  readonly headerHearts: Locator;

  constructor(page: Page) {
    this.page = page;
    this.recommendedSkillNode = page.locator("button[aria-label*='Available skill']").first();
    this.headerStreak = page.locator("div[title='Current Streak']");
    this.headerXP = page.locator("div[title='Total XP']");
    this.headerHearts = page.locator("button[title*='Hearts']");
  }

  async goto() {
    await this.page.goto("/learn");
  }

  async clickRecommendedSkill() {
    await this.recommendedSkillNode.click();
  }
}
