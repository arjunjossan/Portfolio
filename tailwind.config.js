/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./templates/**/*.html",
    "./portfolio_app/**/*.py",
    "./static/js/**/*.js",
  ],
  theme: {
    container: {
      center: true,
      padding: {
        DEFAULT: "1rem",
        sm: "1.5rem",
        lg: "2rem",
        xl: "2.5rem",
      },
      screens: {
        "2xl": "1280px",
      },
    },
    extend: {
      colors: {
        brand: {
          50: "#eef9ff",
          100: "#d9f1ff",
          200: "#bce7ff",
          300: "#8cd8ff",
          400: "#56c0ff",
          500: "#2ca5f5",
          600: "#1683d6",
          700: "#1268ad",
          800: "#14588f",
          900: "#164875",
          950: "#0c2944",
          DEFAULT: "#2ca5f5",
        },
        secondary: {
          50: "#ecfdf8",
          100: "#d1faef",
          200: "#a8f5e0",
          300: "#72ead0",
          400: "#39d5bb",
          500: "#16b8a0",
          600: "#109181",
          700: "#117468",
          800: "#125c53",
          900: "#114c46",
          950: "#042d2b",
          DEFAULT: "#16b8a0",
        },
        accent: {
          50: "#fff7ed",
          100: "#ffeed4",
          200: "#ffd9a8",
          300: "#ffbc70",
          400: "#ff9337",
          500: "#ff7411",
          600: "#f25807",
          700: "#c94109",
          800: "#9f3410",
          900: "#7f2d11",
          950: "#451306",
          DEFAULT: "#ff7411",
        },
        app: {
          bg: {
            light: "#f6f8fc",
            dark: "#050816",
          },
          surface: {
            light: "rgba(255,255,255,0.78)",
            dark: "rgba(12,18,36,0.72)",
          },
          border: {
            light: "rgba(15,23,42,0.08)",
            dark: "rgba(255,255,255,0.12)",
          },
          text: {
            primaryLight: "#0f172a",
            primaryDark: "#e5eefc",
            secondaryLight: "#334155",
            secondaryDark: "#c1d0ea",
            mutedLight: "#64748b",
            mutedDark: "#8da2c0",
          },
        },
      },
      fontFamily: {
        sans: ["Manrope", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Space Grotesk", "ui-sans-serif", "system-ui", "sans-serif"],
        editorial: ["Playfair Display", "ui-serif", "Georgia", "serif"],
      },
      fontSize: {
        "display-1": ["4.5rem", { lineHeight: "0.95", letterSpacing: "-0.05em", fontWeight: "700" }],
        "display-2": ["3.5rem", { lineHeight: "1", letterSpacing: "-0.04em", fontWeight: "700" }],
        "heading-1": ["2.75rem", { lineHeight: "1.05", letterSpacing: "-0.035em", fontWeight: "700" }],
        "heading-2": ["2rem", { lineHeight: "1.1", letterSpacing: "-0.03em", fontWeight: "700" }],
        "heading-3": ["1.5rem", { lineHeight: "1.2", letterSpacing: "-0.02em", fontWeight: "600" }],
        "heading-4": ["1.125rem", { lineHeight: "1.35", letterSpacing: "-0.01em", fontWeight: "600" }],
      },
      borderRadius: {
        "4xl": "2rem",
        "5xl": "2.5rem",
      },
      boxShadow: {
        soft: "0 18px 60px rgba(8, 15, 35, 0.12)",
        glass: "0 24px 80px rgba(6, 12, 28, 0.28)",
        lift: "0 16px 44px rgba(8, 15, 35, 0.18)",
      },
      backdropBlur: {
        glass: "18px",
      },
      spacing: {
        section: "5.5rem",
      },
      transitionDuration: {
        280: "280ms",
        320: "320ms",
      },
      backgroundImage: {
        "hero-mesh-dark":
          "radial-gradient(circle at top left, rgba(44,165,245,0.18), transparent 28%), radial-gradient(circle at top right, rgba(22,184,160,0.14), transparent 24%), linear-gradient(180deg, #050816 0%, #0a1020 52%, #050816 100%)",
        "hero-mesh-light":
          "radial-gradient(circle at top left, rgba(44,165,245,0.14), transparent 26%), radial-gradient(circle at top right, rgba(22,184,160,0.12), transparent 24%), linear-gradient(180deg, #f8fbff 0%, #eef4fb 52%, #f8fbff 100%)",
        "brand-gradient":
          "linear-gradient(135deg, rgba(44,165,245,0.96) 0%, rgba(22,184,160,0.96) 100%)",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.45s ease forwards",
      },
    },
  },
  plugins: [],
};
