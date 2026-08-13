import { test, expect } from "@playwright/test";
import { LeaderboardPage } from "../pages/LeaderboardPage";

test.describe("Leaderboard Standings & Tab Navigation", () => {
  test("renders podium, period tabs, and current user rank", async ({ page }) => {
    const leaderboardPage = new LeaderboardPage(page);
    await leaderboardPage.goto();

    await expect(leaderboardPage.leaderboardTitle).toBeVisible();

    // Verify period tabs
    await expect(leaderboardPage.weeklyTab).toBeVisible();
    await expect(leaderboardPage.monthlyTab).toBeVisible();
    await expect(leaderboardPage.allTimeTab).toBeVisible();

    // Switch tabs
    await leaderboardPage.monthlyTab.click();
    await expect(leaderboardPage.monthlyTab).toHaveClass(/border-\[\#1cb0f6\]/);

    await leaderboardPage.allTimeTab.click();
    await expect(leaderboardPage.allTimeTab).toHaveClass(/border-\[\#1cb0f6\]/);
  });
});
