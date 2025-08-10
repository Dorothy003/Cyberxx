import React from 'react';
export default function FileItem({ name, size, encrypted = true }) {
  return (
    <div className="file-item flex items-center justify-between bg-gray-900 rounded px-3 py-2 mb-2">
      <div>
        <span className="font-medium text-white">{name}</span>{" "}
        <span className="text-xs text-gray-400">{size} • {encrypted ? "Encrypted" : "Not Encrypted"}</span>
      </div>
      <div className="flex gap-2">
        <button className="text-blue-400 hover:text-blue-600">⬇️</button>
        <button className="text-gray-400 hover:text-red-600">🗑️</button>
      </div>
    </div>
  );
}
