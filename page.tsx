'use client';

import { useState, useEffect } from 'react';
import { FormInput } from '@/components/FormInput';
import { SubmitButton } from '@/components/SubmitButton';
import { ResponseDisplay } from '@/components/ResponseDisplay';
import { getCurrentApiConfig, getCurrentApiVersion, setCurrentApiVersion, ApiVersion, checkApiHealth, makeApiRequest } from '@/config/api';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [apiVersion, setApiVersion] = useState<ApiVersion>('gemini');
  const [apiStatus, setApiStatus] = useState<'healthy' | 'unhealthy' | 'checking'>('checking');

  // Check API health on component mount and when API version changes
  useEffect(() => {
    const checkHealth = async () => {
      setApiStatus('checking');
      const isHealthy = await checkApiHealth(apiVersion);
      setApiStatus(isHealthy ? 'healthy' : 'unhealthy');
    };

    checkHealth();
  }, [apiVersion]);

  const handleApiVersionChange = (version: ApiVersion) => {
    setApiVersion(version);
    setCurrentApiVersion(version);
    setError(null);
    setResponse(null);
  };

  const handleSubmit = async () => {
    if (!prompt.trim()) return;
    
    setIsLoading(true);
    setError(null);
    setResponse(null);

    try {
      const apiConfig = getCurrentApiConfig();
      const res = await makeApiRequest(apiConfig.chatEndpoint, {
        method: 'POST',
        body: JSON.stringify({ message: prompt }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${res.status}: ${res.statusText}`);
      }

      const data = await res.json();
      setResponse(data.response);
    } catch (err) {
      console.error('Submit request failed:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = () => {
    switch (apiStatus) {
      case 'healthy': return 'text-green-600';
      case 'unhealthy': return 'text-red-600';
      case 'checking': return 'text-yellow-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusText = () => {
    switch (apiStatus) {
      case 'healthy': return 'Connected';
      case 'unhealthy': return 'Disconnected';
      case 'checking': return 'Checking...';
      default: return 'Unknown';
    }
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-2xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Content Generator
          </h1>
          
          {/* API Version Toggle */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">API Version:</span>
              <select
                value={apiVersion}
                onChange={(e) => handleApiVersionChange(e.target.value as ApiVersion)}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="gemini">Gemini (Port 8001)</option>
                <option value="openai">OpenAI (Port 8000)</option>
              </select>
            </div>
            
            {/* API Status Indicator */}
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${apiStatus === 'healthy' ? 'bg-green-500' : apiStatus === 'unhealthy' ? 'bg-red-500' : 'bg-yellow-500'}`}></div>
              <span className={`text-sm ${getStatusColor()}`}>
                {getStatusText()}
              </span>
            </div>
          </div>
        </div>
        
        <div className="space-y-6">
          <FormInput value={prompt} onChange={setPrompt} />
          <SubmitButton isLoading={isLoading} onClick={handleSubmit} />
          <ResponseDisplay 
            status={isLoading ? 'processing' : response ? 'complete' : 'idle'}
            intermediateResponses={response ? [response] : []}
            error={error}
          />
        </div>
      </div>
    </main>
  );
}
