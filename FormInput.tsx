import { ChangeEvent } from "react";

interface FormInputProps {
  value: string;
  onChange: (value: string) => void;
}

export const FormInput = ({ value, onChange }: FormInputProps) => {
  return (
    <div className="w-full">
      <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
        Enter your prompt
      </label>
      <textarea
        id="prompt"
        value={value}
        onChange={(e: ChangeEvent<HTMLTextAreaElement>) => onChange(e.target.value)}
        className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
        placeholder="Describe your area of interest or context..."
        rows={4}
      />
    </div>
  );
}; 