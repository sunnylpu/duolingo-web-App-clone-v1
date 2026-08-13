import { test, expect } from "@playwright/test";
import { ProfilePage } from "../pages/ProfilePage";

test.describe("Profile & Achievements", () => {
  test("renders profile header, statistics, and achievement cards", async ({ page }) => {
    const profilePage = new ProfilePage(page);
    await profilePage.goto();

    await expect(profilePage.profileTitle).toBeVisible();
    await expect(profilePage.totalXPStat).toBeVisible();
    await expect(profilePage.achievementsSection).toBeVisible();
  });
});
