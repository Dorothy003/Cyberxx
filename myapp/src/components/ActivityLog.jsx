import React, { useState, useEffect } from "react";
import axios from "axios";
import toast from "react-hot-toast";

export default function ActivityLog() {
  const [activity, setActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchActivity = async () => {
    try {
      const { data } = await axios.get("http://localhost:8000/activity");
      setActivity(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      toast.error("Failed to load activity");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchActivity();
  }, []);

  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg max-h-96 overflow-y-auto">
      <h2 className="text-xl font-bold text-indigo-400 mb-4">🕑 Recent Activity</h2>

      {loading ? (
        <p className="text-gray-400">Loading...</p>
      ) : activity.length > 0 ? (
        <ul>
          {activity.map((a, idx) => (
            <li
              key={idx}
              className="flex justify-between items-center py-2 border-b border-gray-700 hover:bg-gray-700 transition"
            >
              <span className="text-gray-200 font-medium">{a.event}</span>
              <span className="text-gray-400 text-sm">{a.timestamp}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-400">No recent activity</p>
      )}
    </div>
  );
}
