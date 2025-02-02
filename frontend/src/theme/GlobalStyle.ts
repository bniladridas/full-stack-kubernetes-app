import { createTheme } from '@mui/material/styles';
import { experimental_extendTheme as extendTheme } from '@mui/material/styles';

const theme = extendTheme({
  colorSchemes: {
    dark: {
      palette: {
        primary: {
          main: '#00FFD4',     // Vibrant cyan for primary interactions
          light: '#69FFDB',
          dark: '#00B3A6',
        },
        secondary: {
          main: '#FF6B6B',     // Energetic coral for secondary actions
          light: '#FF8F8F',
          dark: '#E74C3C',
        },
        background: {
          default: '#0A1128',   // Deep, dark navy
          paper: '#121C40',     // Slightly lighter navy for surfaces
        },
        text: {
          primary: '#E6E6E6',   // Soft, light text
          secondary: '#8C93A3', // Muted secondary text
        },
        action: {
          active: '#00FFD4',
          hover: 'rgba(0, 255, 212, 0.12)',
          selected: 'rgba(0, 255, 212, 0.16)',
        },
      },
    },
  },
  shape: {
    borderRadius: 12,
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
      letterSpacing: '-0.05em',
    },
    h2: {
      fontWeight: 600,
      letterSpacing: '-0.03em',
    },
    body1: {
      lineHeight: 1.6,
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: `
        @keyframes glowPulse {
          0% { box-shadow: 0 0 10px rgba(0, 255, 212, 0.4); }
          50% { box-shadow: 0 0 20px rgba(0, 255, 212, 0.6); }
          100% { box-shadow: 0 0 10px rgba(0, 255, 212, 0.4); }
        }
        body {
          background-color: #0A1128;
          scrollbar-width: thin;
          scrollbar-color: #00FFD4 #121C40;
        }
        ::-webkit-scrollbar {
          width: 8px;
        }
        ::-webkit-scrollbar-track {
          background: #121C40;
        }
        ::-webkit-scrollbar-thumb {
          background-color: #00FFD4;
          border-radius: 20px;
        }
      `,
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            animation: 'glowPulse 1.5s infinite',
          },
        },
        containedPrimary: {
          background: 'linear-gradient(135deg, #00FFD4, #00B3A6)',
          boxShadow: '0 4px 15px rgba(0, 255, 212, 0.4)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          background: 'linear-gradient(145deg, rgba(18, 28, 64, 0.8), rgba(10, 17, 40, 0.8))',
          backdropFilter: 'blur(15px)',
          border: '1px solid rgba(0, 255, 212, 0.2)',
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'scale(1.02)',
            boxShadow: '0 10px 25px rgba(0, 255, 212, 0.3)',
          },
        },
      },
    },
  },
});

export default theme;

export const GlobalStyles = {
  background: {
    main: {
      background: 'linear-gradient(135deg, #0A1128 0%, #121C40 100%)',
      minHeight: '100vh',
      position: 'relative',
      overflow: 'hidden',
    },
    overlay: {
      position: 'absolute',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      background: 'radial-gradient(circle at 30% 80%, rgba(0, 255, 212, 0.1) 0%, transparent 50%)',
      pointerEvents: 'none',
    },
  },
};
