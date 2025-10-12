import { nextui } from "@nextui-org/react";

/** @type {import('tailwindcss').Config} */
const config = {
  content: [
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
    // Add your other content paths here, e.g.:
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        akira: ['"Akira Expanded"', 'sans-serif'],
      },
      colors: {
        blue: {
          50: "#e6f1fe",
          100: "#cce3fd",
          200: "#99c7fb",
          300: "#66aaf9",
          400: "#338ef7",
          500: "#006FEE",
          600: "#005bc4",
          700: "#004493",
          800: "#002e62",
          900: "#001731",
        },
      },
    },
  },
  darkMode: "class",
  plugins: [nextui()],
};

export default config;