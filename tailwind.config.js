/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './core/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          blue: '#1a4674',     /* Deep blue from Chinese text / borders */
          magenta: '#b71a4c',  /* Rich magenta/crimson from English text and rope */
          gold: '#c0964b',     /* Metallic gold from rope and accents */
          cream: '#f8f9fa',    /* Very light gray/off-white for sections instead of heavy yellow */
        },
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'sans-serif'],
        display: ['Playfair Display', 'serif'],
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
