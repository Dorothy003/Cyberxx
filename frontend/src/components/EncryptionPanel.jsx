import React from 'react';
function ControlButton({ children }) {
  return (
    <button className="control-btn bg-gray-800 hover:bg-blue-700 text-white px-3 py-2 rounded mt-2 w-full">
      {children}
    </button>
  );
}
export default function EncryptionPanel() {
  return (
    <div className="card bg-gray-800 rounded-lg p-5 flex flex-col w-full md:w-1/3 shadow">
      <div className="mb-4">
        <h3 className="font-medium text-lg mb-2">🔑 Encryption Tools</h3>
        <div>
          <label className="block text-gray-400 mb-1">Encryption Method</label>
          <div className="flex gap-2 mb-2">
            <button className="bg-blue-700 text-white px-2 py-1 rounded">AES-256</button>
            <button className="bg-gray-700 text-white px-2 py-1 rounded">RSA</button>
          </div>
          <label className="block text-gray-400 mb-1">Key Management</label>
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-gray-900 px-2 py-1 rounded text-white text-xs">RSA-2048 (Active)</span>
            <button className="bg-gray-700 p-1 rounded text-blue-400">🔒</button>
            <button className="bg-gray-700 p-1 rounded text-blue-400">📋</button>
          </div>
          <ControlButton>Generate New Keys</ControlButton>
        </div>
      </div>
      <div>
        <label className="block text-gray-400 mb-1">Encryption Status</label>
        <div className="w-full bg-gray-700 rounded mb-1 h-2">
          <div className="bg-blue-500 h-2 rounded" style={{width: "100%"}}></div>
        </div>
        <span className="text-xs text-gray-300">System Protected <b>100%</b></span>
      </div>
    </div>
  );
}
