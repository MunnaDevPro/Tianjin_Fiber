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
        'scroll-drop': 'scrollDrop 1.5s cubic-bezier(0.15, 0.41, 0.69, 0.94) infinite',
        'chevron-fade': 'chevronFade 1.5s infinite',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        scrollDrop: {
          '0%': { transform: 'translateY(0)', opacity: '0' },
          '10%': { opacity: '1' },
          '50%': { opacity: '1' },
          '100%': { transform: 'translateY(20px)', opacity: '0' },
        },
        chevronFade: {
          '0%': { opacity: '0' },
          '50%': { opacity: '1' },
          '100%': { opacity: '0' },
        }
      }
    },
  },
  plugins: [],
}
