import { Page, Locator } from "@playwright/test";

export class LeaderboardPage {
  readonly page: Page;
  readonly leaderboardTitle: Locator;
  readonly weeklyTab: Locator;
  readonly monthlyTab: Locator;
  readonly allTimeTab: Locator;

  constructor(page: Page) {
    this.page = page;
    this.leaderboardTitle = page.locator("h1:has-text('Leaderboard')");
    this.weeklyTab = page.locator("button:has-text('Weekly')");
    this.monthlyTab = page.locator("button:has-text('Monthly')");
    this.allTimeTab = page.locator("button:has-text('All Time')");
  }

  async goto() {
    await this.page.goto("/leaderboard");
  }
}
