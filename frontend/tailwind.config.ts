import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./features/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        duo: {
          green: "#58cc02",
          "green-dark": "#46a302",
          blue: "#1cb0f6",
          "blue-dark": "#1899d6",
          purple: "#ce82ff",
          yellow: "#ffc800",
          red: "#ff4b4b",
          dark: "#131f24",
          "dark-card": "#182830",
          "dark-border": "#37464f",
        },
      },
    },
  },
  plugins: [],
};

export default config;
