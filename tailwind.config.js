/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Bebas Neue"', 'cursive'],
        mono: ['"JetBrains Mono"', 'monospace'],
        body: ['"DM Sans"', 'sans-serif'],
      },
      colors: {
        fleet: {
          bg:       '#0a0a0a',
          surface:  '#111111',
          card:     '#161616',
          border:   '#222222',
          amber:    '#f59e0b',
          amber2:   '#fbbf24',
          red:      '#ef4444',
          green:    '#22c55e',
          blue:     '#3b82f6',
          muted:    '#555555',
          text:     '#e5e5e5',
          subtle:   '#888888',
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-in': 'slideIn 0.3s ease-out',
        'pulse-slow': 'pulse 3s infinite',
      },
      keyframes: {
        fadeIn: { from: { opacity: 0 }, to: { opacity: 1 } },
        slideIn: { from: { opacity: 0, transform: 'translateY(8px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
      },
    },
  },
  plugins: [],
}
