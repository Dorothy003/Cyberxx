
import React, { useState } from "react";

function ControlButton({ children, ...props }) {
  return (
    <button
      className="bg-gray-800 hover:bg-blue-700 text-white px-3 py-2 rounded mt-2 w-full"
      {...props}
    >
      {children}
    </button>
  );
}

export default function EncryptionPanel({ setActivities }) {
  const [method, setMethod] = useState('AES-256');
  const [key, setKey] = useState('RSA-2048 (Active)');
  const [showCopied, setShowCopied] = useState(false);

  const handleKeyGen = () => {
    setKey('RSA-4096 (New)');
    setActivities(
      prev => [
        { text: "New keys generated (RSA-4096)", time: new Date().toLocaleString() },
        ...prev,
      ]
    );
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(key);
    setShowCopied(true);
    setTimeout(() => setShowCopied(false), 2000);
  };

  return (
    <div className="bg-gray-800 rounded-lg p-5 flex flex-col w-full md:w-1/3 shadow">
      <h3 className="font-medium text-lg mb-3">🔑 Encryption Tools</h3>
      <div className="mb-4">
        <label className="block text-gray-400 mb-1">Encryption Method</label>
        <div className="flex gap-2 mb-2">
          <button
            className={`px-2 py-1 rounded ${method === 'AES-256' ? 'bg-blue-700' : 'bg-gray-700'} text-white`}
            onClick={() => setMethod('AES-256')}
          >AES-256</button>
          <button
            className={`px-2 py-1 rounded ${method === 'RSA' ? 'bg-blue-700' : 'bg-gray-700'} text-white`}
            onClick={() => setMethod('RSA')}
          >RSA</button>
        </div>
        <label className="block text-gray-400 mb-1">Key Management</label>
        <div className="flex items-center gap-2 mb-2">
          <span className="bg-gray-900 px-2 py-1 rounded text-white text-xs">{key}</span>
          <button
            className="bg-gray-700 p-1 rounded text-blue-400"
            title="Copy Key"
            onClick={handleCopy}
          >📋</button>
          {showCopied && <span className="text-green-400 text-xs ml-2">Copied!</span>}
        </div>
        <ControlButton onClick={handleKeyGen}>Generate New Keys</ControlButton>
      </div>
      <div>
        <label className="block text-gray-400 mb-1">Encryption Status</label>
        <div className="w-full bg-gray-700 rounded mb-1 h-2">
          <div className="bg-blue-500 h-2 rounded" style={{ width: "100%" }}></div>
        </div>
        <span className="text-xs text-gray-300">
          System Protected <b>100%</b>
        </span>
      </div>
    </div>
  );
}
