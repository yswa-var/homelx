// Configuration for API endpoints
const config = {
  // Development - local backend
  development: {
    baseURL: 'http://localhost:8000'
  },
  // Production - Render backend
  production: {
    baseURL: 'https://your-render-app-name.onrender.com' // Replace with your actual Render URL
  }
};

// Get current environment
const isDevelopment = import.meta.env.DEV;

// Export the appropriate config
export const apiConfig = isDevelopment ? config.development : config.production;

// Helper function to get full API URL
export const getApiUrl = (endpoint) => {
  return `${apiConfig.baseURL}${endpoint}`;
}; 