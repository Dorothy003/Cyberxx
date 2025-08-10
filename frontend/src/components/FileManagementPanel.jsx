import React from 'react';
import FileItem from './FileItem';
export default function FileManagementPanel() {
  const files = [
    { name: "financial_report_2025.pdf", size: "1.2 MB", encrypted: true },
    { name: "passport_scan.jpg", size: "3.5 MB", encrypted: true },
    { name: "passwords.txt", size: "0.1 MB", encrypted: true },
  ];
  return (
    <div className="card bg-gray-800 rounded-lg p-5 flex flex-col w-full md:w-1/3 shadow">
      <h3 className="font-medium text-lg mb-2">📂 File Management</h3>
      <div className="drag-drop-area flex flex-col items-center justify-center border-2 border-dashed border-gray-700 rounded py-6 mb-4 bg-gray-900">
        <span className="text-gray-400 mb-2">Drag & drop files here</span>
        <button className="bg-blue-700 text-white px-4 py-2 rounded">Browse Files</button>
      </div>
      <div>
        <div className="text-sm text-gray-400 mb-1 flex items-center justify-between">
          <span>Recent Files</span>
          <button className="text-gray-400 hover:text-white text-xs">Filter</button>
        </div>
        <div>
          {files.map(f => (
            <FileItem key={f.name} {...f} />
          ))}
        </div>
      </div>
    </div>
  );
}
