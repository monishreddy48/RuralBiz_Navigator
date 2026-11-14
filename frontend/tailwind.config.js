/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        forest: {
          50: "#F2F7F4",
          100: "#E3EFE9",
          200: "#C3DDCF",
          300: "#9BC3AE",
          400: "#6DA488",
          500: "#458564",
          600: "#2E6A4C",
          700: "#22533B",
          800: "#1B4230",
          900: "#0F5132",
          950: "#0A2E1D",
        },
        ivory: {
          50: "#FDFCF8",
          100: "#FAF7EE",
          200: "#F2ECE0",
          300: "#E5DCCB",
          400: "#D3C6AE",
        },
        sage: {
          50: "#F4F7F4",
          100: "#E6ECE5",
          200: "#D1DDD0",
          300: "#B2C5B1",
          400: "#8FA98E",
          500: "#6E896D",
        },
        charcoal: {
          950: "#0B0F17",
          900: "#111827",
          800: "#1E293B",
          700: "#334155",
          600: "#475569",
          500: "#64748B",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "Inter", "sans-serif"],
        serif: ["var(--font-serif)", "Merriweather", "serif"],
      },
      boxShadow: {
        subtle: "0 1px 3px rgba(0, 0, 0, 0.04), 0 2px 6px rgba(0, 0, 0, 0.02)",
        editorial: "0 4px 20px -2px rgba(15, 81, 50, 0.06), 0 2px 6px -1px rgba(0, 0, 0, 0.04)",
        card: "0 10px 25px -5px rgba(15, 81, 50, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.03)",
        lift: "0 20px 30px -10px rgba(15, 81, 50, 0.12), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
      },
    },
  },
  plugins: [],
};

