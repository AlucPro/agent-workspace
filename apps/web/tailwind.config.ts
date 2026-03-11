import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./hooks/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#161616",
        paper: "#f4efe8",
        accent: "#d3632b",
        accentSoft: "#f0c3a3",
        line: "#d6cabb",
        panel: "#fffaf3",
        muted: "#6d655d",
      },
      boxShadow: {
        panel: "0 18px 50px rgba(22, 22, 22, 0.08)",
      },
      fontFamily: {
        sans: [
          "\"SF Pro Display\"",
          "\"PingFang SC\"",
          "\"Hiragino Sans GB\"",
          "\"Microsoft YaHei\"",
          "system-ui",
          "sans-serif",
        ],
      },
      backgroundImage: {
        "paper-grid":
          "linear-gradient(rgba(214, 202, 187, 0.45) 1px, transparent 1px), linear-gradient(90deg, rgba(214, 202, 187, 0.45) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};

export default config;
