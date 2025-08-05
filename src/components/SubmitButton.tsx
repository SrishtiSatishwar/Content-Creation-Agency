interface SubmitButtonProps {
  isLoading: boolean;
  onClick: () => void;
}

export const SubmitButton = ({ isLoading, onClick }: SubmitButtonProps) => {
  return (
    <button
      onClick={onClick}
      disabled={isLoading}
      className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white 
        ${isLoading 
          ? 'bg-indigo-400 cursor-not-allowed' 
          : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
        }`}
    >
      {isLoading ? 'Processing...' : 'Submit'}
    </button>
  );
}; 
