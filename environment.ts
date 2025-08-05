// Environment configuration for the application
export const ENV_CONFIG = {
  // Default API version to use (now only Gemini)
  DEFAULT_API_VERSION: 'gemini' as const,
  
  // API endpoints - now using Gemini-only backend on port 8002
  API_ENDPOINTS: {
    OPENAI: {
      BASE_URL: 'http://localhost:8000',
      CHAT: 'http://localhost:8000/api/chat',
      HEALTH: 'http://localhost:8000/api/health',
    },
    GEMINI: {
      BASE_URL: 'http://localhost:8002',
      CHAT: 'http://localhost:8002/api/chat',
      HEALTH: 'http://localhost:8002/api/health',
    },
  },
  
  // Feature flags
  FEATURES: {
    ENABLE_API_VERSION_TOGGLE: true,
    ENABLE_HEALTH_CHECK: true,
    ENABLE_ERROR_RETRY: true,
  },
  
  // Timeouts and retry settings
  TIMEOUTS: {
    API_REQUEST: 30000, // 30 seconds
    HEALTH_CHECK: 5000, // 5 seconds
    RETRY_DELAY: 1000, // 1 second
    MAX_RETRIES: 3,
  },
};

// Helper function to get environment variable with fallback
export const getEnvVar = (key: string, fallback: string = ''): string => {
  if (typeof window !== 'undefined') {
    // Client-side: check localStorage or use fallback
    return localStorage.getItem(key) || fallback;
  }
  // Server-side: check process.env or use fallback
  return process.env[key] || fallback;
};

// Helper function to set environment variable
export const setEnvVar = (key: string, value: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(key, value);
  }
}; 