
import React, { useState } from "react";

export default function RecentActivity({ activities }) {
  const [showAll, setShowAll] = useState(false);
  const displayed = showAll ? activities : activities.slice(0, 4);

  return (
    <div className="bg-gray-800 rounded-lg p-5 mt-2 shadow">
      <div className="flex items-center justify-between mb-2">
        <span className="font-medium text-lg">🕒 Recent Activity</span>
        <button
          className="text-xs text-blue-400 hover:underline"
          onClick={() => setShowAll((v) => !v)}
        >
          {showAll ? "Show Less" : "View All"}
        </button>
      </div>
      <ul>
        {displayed.map((i, idx) => (
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
