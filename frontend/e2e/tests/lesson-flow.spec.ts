import { test, expect } from "@playwright/test";

test.describe("Lesson Player & Exercise Flow", () => {
  test("starts lesson, submits answer, and plays exercises", async ({ page }) => {
    await page.goto("/lesson/lsn_greetings_1");

    // Intro page
    await expect(page.locator("h1:has-text('Basic Greetings 1')")).toBeVisible();
    await page.click("button:has-text('START LESSON')");

    // Lesson player
    await expect(page.locator("button:has-text('CHECK')")).toBeVisible();

    // Select option & check
    await page.click("button:has-text('Hola')");
    await page.click("button:has-text('CHECK')");

    // Verify feedback bar
    await expect(page.locator("button:has-text('CONTINUE')")).toBeVisible();
  });
});
