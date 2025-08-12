
import React, { useState } from "react";

export default function IntegritySection({ setActivities }) {
  const [verified, setVerified] = useState(true);

  const files = [
    {
      name: "financial_report_2025.pdf",
      hash: "3a5c9e...375d",
      status: "Verified",
      algo: "SHA-256",
      date: "May 10, 2025"
    },
    {
      name: "passport_scan.jpg",
      hash: "a125fc...f5ab",
      status: "Verified",
      algo: "SHA-256",
      date: "May 12, 2025"
    },
    {
      name: "passwords.txt",
      hash: "6892a0...6a0a",
      status: "Verified",
      algo: "SHA-256",
      date: "May 9, 2025"
    }
  ];

  const handleVerify = () => {
    setVerified(true);
    setActivities((prev) => [
      { text: "Integrity check completed: All files verified", time: new Date().toLocaleString() },
      ...prev,
    ]);
  };

  return (
    <div className="bg-gray-800 rounded-lg p-5 flex flex-col w-full md:w-1/3 shadow">
      <h3 className="font-medium text-lg mb-2">✅ Integrity Verification</h3>
      <div className="mb-3">
        <div className="bg-gray-900 rounded px-4 py-2">
          <span className="font-bold">All files verified</span>
          <div className="text-xs text-gray-400">
            Last scan: {files[0].date} 10:23 AM
          </div>
        </div>
      </div>
      <div>
        <span className="text-gray-400 mb-2 block">Hash Verification</span>
        {files.map((file) => (
          <div
            className="flex items-center justify-between bg-gray-900 rounded px-3 py-2 mb-2"
            key={file.name}
          >
            <div>
              <span className="text-white text-sm">{file.name}</span>
              <div className="text-xs text-gray-400">{file.hash}</div>
            </div>
            <div className="flex flex-col items-end">
              <span className="bg-gray-700 text-xs text-blue-300 rounded px-2 mb-1">
                {file.algo}
              </span>
              <span className="text-green-400 text-xs font-bold">{file.status}</span>
            </div>
          </div>
        ))}
      </div>
      <button
        className="bg-blue-700 hover:bg-blue-600 text-white px-4 py-2 rounded mt-4"
        onClick={handleVerify}
      >
        Verify All Files
      </button>
      {verified && (
        <span className="text-green-300 font-bold mt-2 block">
          Verification Complete!
        </span>
      )}
    </div>
  );
}
