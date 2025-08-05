import { ChatStatus } from '@/types/chat';

interface ResponseDisplayProps {
  status: ChatStatus;
  intermediateResponses: string[];
  error: string | null;
}

export const ResponseDisplay = ({ status, intermediateResponses, error }: ResponseDisplayProps) => {
  if (status === 'idle') return null;

  return (
    <div className="mt-6">
      <h3 className="text-lg font-medium text-gray-900 mb-2">Response</h3>
      <div className={`p-4 rounded-md ${
        error 
          ? 'bg-red-50 border border-red-200' 
          : 'bg-gray-50 border border-gray-200'
      }`}>
        {error ? (
          <p className="text-red-700">{error}</p>
        ) : (
          <div className="space-y-2">
            {status === 'processing' && (
              <div className="flex items-center space-x-2 text-gray-600">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                <span>Processing...</span>
              </div>
            )}
            {intermediateResponses.map((response, index) => (
              <p key={index} className="text-gray-700 whitespace-pre-wrap">
                {response}
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}; 
