import { Page, Locator } from "@playwright/test";

export class ProfilePage {
  readonly page: Page;
  readonly profileTitle: Locator;
  readonly totalXPStat: Locator;
  readonly achievementsSection: Locator;

  constructor(page: Page) {
    this.page = page;
    this.profileTitle = page.locator("h1:has-text('Learner Profile')");
    this.totalXPStat = page.locator("text=Total XP");
    this.achievementsSection = page.locator("h2:has-text('Achievements')");
  }

  async goto() {
    await this.page.goto("/profile");
  }
}
