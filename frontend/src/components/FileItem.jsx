
import React from "react";

export default function FileItem({ name, size, encrypted = false, onDelete, onDownload }) {
  return (
    <div className="flex items-center justify-between bg-gray-900 rounded px-3 py-2 mb-2">
      <div>
        <span className="font-medium text-white">{name}</span>{" "}
        <span className="text-xs text-gray-400">
          {size} • {encrypted ? "Encrypted" : "Not Encrypted"}
        </span>
      </div>
      <div className="flex gap-2">
        <button
          className="text-blue-400 hover:text-blue-600"
          title="Download"
          onClick={onDownload}
        >⬇️</button>
        <button
          className="text-gray-400 hover:text-red-600"
          title="Delete"
          onClick={onDelete}
        >🗑️</button>
      </div>
    </div>
  );
}
