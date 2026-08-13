import { test, expect } from "@playwright/test";

test.describe("Gamification & Out of Hearts Recovery Modal", () => {
  test("opens Out of Hearts modal from header hearts widget", async ({ page }) => {
    await page.goto("/learn");

    // Click hearts widget in header
    await page.click("button[title*='Hearts']");

    // Verify modal overlay
    await expect(page.locator("h2:has-text('Out of Hearts!')")).toBeVisible();
    await expect(page.locator("button:has-text('PRACTICE FOR HEART')")).toBeVisible();
    await expect(page.locator("button:has-text('MOCK REFILL')")).toBeVisible();
  });
});
