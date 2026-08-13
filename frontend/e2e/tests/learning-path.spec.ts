import { test, expect } from "@playwright/test";
import { LearnPage } from "../pages/LearnPage";

test.describe("Learning Path Navigation & Node States", () => {
  test("renders learning path with unit headers and skill nodes", async ({ page }) => {
    const learnPage = new LearnPage(page);
    await learnPage.goto();

    // Verify main brand & learn title
    await expect(page.locator("h1:has-text('Spanish Course Path')")).toBeVisible();

    // Verify stats bar widgets
    await expect(learnPage.headerStreak).toBeVisible();
    await expect(learnPage.headerXP).toBeVisible();
    await expect(learnPage.headerHearts).toBeVisible();

    // Verify skill node rendering
    await expect(learnPage.recommendedSkillNode).toBeVisible();
  });
});
