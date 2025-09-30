import { nextui } from "@nextui-org/react";

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
    // Add your other content paths here, e.g.:
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        akira: ['Akira Expanded', 'sans-serif'],
      },
    },
  },
  darkMode: "class",
  plugins: [nextui()],
};