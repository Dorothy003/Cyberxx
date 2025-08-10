
import React, { useState, useRef } from "react";
import FileItem from "./FileItem";

export default function FileManagementPanel({ setActivities }) {
  const [files, setFiles] = useState([
    { name: "financial_report_2025.pdf", size: "1.2 MB", encrypted: true },
    { name: "passport_scan.jpg", size: "3.5 MB", encrypted: true },
    { name: "passwords.txt", size: "0.1 MB", encrypted: true },
  ]);
  const fileInputRef = useRef();

  const handleFileUpload = (event) => {
    const newFiles = Array.from(event.target.files).map((file) => ({
      name: file.name,
      size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
      encrypted: false,
    }));
    setFiles((prev) => [...prev, ...newFiles]);
    setActivities((prev) => [
      { text: `File uploaded: ${newFiles.map(f => f.name).join(', ')}`, time: new Date().toLocaleString() },
      ...prev,
    ]);
  };

  const handleDelete = (name) => {
    setFiles(files.filter((f) => f.name !== name));
    setActivities((prev) => [
      { text: `File deleted: ${name}`, time: new Date().toLocaleString() }, ...prev
    ]);
  };

  const handleDownload = (name) => {
    setActivities((prev) => [
      { text: `File downloaded: ${name}`, time: new Date().toLocaleString() }, ...prev
    ]);
   
    alert(`Download simulated for ${name}`);
  };


  return (
    <div className="bg-gray-800 rounded-lg p-5 flex flex-col w-full md:w-1/3 shadow">
      <h3 className="font-medium text-lg mb-2">📂 File Management</h3>
      <input
        type="file"
        multiple
        style={{ display: "none" }}
        ref={fileInputRef}
        onChange={handleFileUpload}
      />
      <div
        className="drag-drop-area flex flex-col items-center justify-center border-2 border-dashed border-gray-700 rounded py-6 mb-4 bg-gray-900 cursor-pointer"
        onClick={() => fileInputRef.current.click()}
      >
        <span className="text-gray-400 mb-2">Drag & drop files here</span>
        <button className="bg-blue-700 text-white px-4 py-2 rounded">
          Browse Files
        </button>
      </div>
      <div>
        <div className="text-sm text-gray-400 mb-1 flex items-center justify-between">
          <span>Recent Files</span>
        </div>
        <div>
          {files.map((f) => (
            <FileItem
              key={f.name}
              {...f}
              onDelete={() => handleDelete(f.name)}
              onDownload={() => handleDownload(f.name)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
