export type ChatStatus = 'idle' | 'processing' | 'complete' | 'error';

export interface ChatEvent {
  type: 'status' | 'response' | 'error';
  data: {
    status?: ChatStatus;
    message?: string;
    error?: string;
  };
}

export interface ChatState {
  status: ChatStatus;
  message: string;
  error: string | null;
  intermediateResponses: string[];
} 
