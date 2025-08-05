import { ENV_CONFIG } from './environment';

export type ApiVersion = 'openai' | 'gemini';

export interface ApiConfig {
  baseUrl: string;
  chatEndpoint: string;
  healthEndpoint: string;
  name: string;
}

export const API_CONFIGS: Record<ApiVersion, ApiConfig> = {
  openai: {
    baseUrl: ENV_CONFIG.API_ENDPOINTS.OPENAI.BASE_URL,
    chatEndpoint: ENV_CONFIG.API_ENDPOINTS.OPENAI.CHAT,
    healthEndpoint: ENV_CONFIG.API_ENDPOINTS.OPENAI.HEALTH,
    name: 'OpenAI Version'
  },
  gemini: {
    baseUrl: ENV_CONFIG.API_ENDPOINTS.GEMINI.BASE_URL,
    chatEndpoint: ENV_CONFIG.API_ENDPOINTS.GEMINI.CHAT,
    healthEndpoint: ENV_CONFIG.API_ENDPOINTS.GEMINI.HEALTH,
    name: 'Gemini Version'
  }
};

// Get the current API version from environment variable or default to gemini
export const getCurrentApiVersion = (): ApiVersion => {
  if (typeof window !== 'undefined') {
    return (localStorage.getItem('apiVersion') as ApiVersion) || ENV_CONFIG.DEFAULT_API_VERSION;
  }
  return ENV_CONFIG.DEFAULT_API_VERSION;
};

// Set the current API version
export const setCurrentApiVersion = (version: ApiVersion): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('apiVersion', version);
  }
};

// Get the current API configuration
export const getCurrentApiConfig = (): ApiConfig => {
  const version = getCurrentApiVersion();
  return API_CONFIGS[version];
};

// Check if the API is healthy with timeout and retry logic
export const checkApiHealth = async (version?: ApiVersion): Promise<boolean> => {
  const config = version ? API_CONFIGS[version] : getCurrentApiConfig();
  
  for (let attempt = 1; attempt <= ENV_CONFIG.TIMEOUTS.MAX_RETRIES; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), ENV_CONFIG.TIMEOUTS.HEALTH_CHECK);
      
      const response = await fetch(config.healthEndpoint, {
        signal: controller.signal,
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        return true;
      }
    } catch (error) {
      console.warn(`API health check attempt ${attempt} failed:`, error);
      
      if (attempt < ENV_CONFIG.TIMEOUTS.MAX_RETRIES) {
        // Wait before retrying
        await new Promise(resolve => setTimeout(resolve, ENV_CONFIG.TIMEOUTS.RETRY_DELAY));
      }
    }
  }
  
  return false;
};

// Enhanced API request function with retry logic
export const makeApiRequest = async (
  endpoint: string,
  options: RequestInit = {},
  retries: number = ENV_CONFIG.TIMEOUTS.MAX_RETRIES
): Promise<Response> => {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), ENV_CONFIG.TIMEOUTS.API_REQUEST);
      
      const response = await fetch(endpoint, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });
      
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      console.warn(`API request attempt ${attempt} failed:`, error);
      
      if (attempt < retries) {
        // Wait before retrying
        await new Promise(resolve => setTimeout(resolve, ENV_CONFIG.TIMEOUTS.RETRY_DELAY));
      } else {
        throw error;
      }
    }
  }
  
  throw new Error('All API request attempts failed');
}; 