import React from 'react';

export default function RecentActivity() {
  const items = [
    { text: 'File uploaded: passwords.txt', time: 'May 15, 2025 10:21 AM' },
    { text: 'File encrypted: passwords.txt', time: 'May 15, 2025 10:22 AM' },
    { text: 'Integrity check completed: All files verified', time: 'May 15, 2025 10:23 AM' },
    { text: 'File downloaded: passport_scan.jpg', time: 'May 14, 2025 03:45 PM' },
  ];
  return (
    <div className="card bg-gray-800 rounded-lg p-5 mt-2 shadow">
      <div className="flex items-center justify-between mb-2">
        <span className="font-medium text-lg">🕒 Recent Activity</span>
        <button className="text-xs text-blue-400 hover:underline">View All</button>
      </div>
      <ul>
        {items.map((i, idx) => (
          <li className="flex items-center text-sm text-gray-300 mb-2" key={idx}>
            <span className="bg-gray-700 rounded px-2 py-1 mr-2">•</span> 
            <span>{i.text}</span>
            <span className="ml-auto text-xs text-gray-400">{i.time}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
