import { useState, useCallback } from 'react';
import { ChatState, ChatStatus, ChatEvent } from '@/types/chat';
import { getCurrentApiConfig, makeApiRequest } from '@/config/api';

const initialState: ChatState = {
  status: 'idle',
  message: '',
  error: null,
  intermediateResponses: [],
};

export const useChat = () => {
  const [state, setState] = useState<ChatState>(initialState);

  const sendMessage = useCallback(async (message: string) => {
    setState(prev => ({
      ...prev,
      status: 'processing',
      message: '',
      error: null,
      intermediateResponses: [],
    }));

    try {
      const apiConfig = getCurrentApiConfig();
      const response = await makeApiRequest(apiConfig.chatEndpoint, {
        method: 'POST',
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }

      // Handle the response as a stream
      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response stream available');
      }

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // Convert the Uint8Array to string
        const chunk = new TextDecoder().decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const chatEvent: ChatEvent = JSON.parse(line.slice(6));
              
              switch (chatEvent.type) {
                case 'status':
                  setState(prev => ({
                    ...prev,
                    status: chatEvent.data.status || 'processing',
                  }));
                  break;
                case 'response':
                  setState(prev => ({
                    ...prev,
                    intermediateResponses: [...prev.intermediateResponses, chatEvent.data.message || ''],
                  }));
                  break;
                case 'error':
                  setState(prev => ({
                    ...prev,
                    status: 'error',
                    error: chatEvent.data.error || 'An error occurred',
                  }));
                  break;
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e);
            }
          }
        }
      }

      // Set status to complete when stream ends
      setState(prev => ({
        ...prev,
        status: 'complete',
      }));

    } catch (error) {
      console.error('Chat request failed:', error);
      setState(prev => ({
        ...prev,
        status: 'error',
        error: error instanceof Error ? error.message : 'An error occurred',
      }));
    }
  }, []);

  const reset = useCallback(() => {
    setState(initialState);
  }, []);

  return {
    ...state,
    sendMessage,
    reset,
  };
}; 