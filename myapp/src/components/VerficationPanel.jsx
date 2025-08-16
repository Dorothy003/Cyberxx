import React, { useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";

export default function VerificationPanel() {
  const [statusList, setStatusList] = useState([]);
  const [loading, setLoading] = useState(false);

  const verifyFiles = async () => {
    setLoading(true);
    setStatusList([]);
    try {
      const { data } = await axios.post("http://localhost:8000/files/verify");
      
      // Expecting data to be an array of { filename, success, message }
      if (Array.isArray(data)) {
        setStatusList(data);
        toast.success("Verification complete");
      } else {
        toast.error("Unexpected response format");
      }
    } catch (err) {
      console.error(err.response || err);
      toast.error("Verification failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 rounded-xl p-4 shadow max-w-md mx-auto">
      <h2 className="text-lg font-semibold mb-3">✅ Integrity Verification</h2>
      <button
        onClick={verifyFiles}
        disabled={loading}
        className={`px-3 py-2 rounded mb-4 ${
          loading ? "bg-gray-500 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-500"
        }`}
      >
        {loading ? "Verifying..." : "Verify All Files"}
      </button>

      {statusList.length > 0 && (
        <div className="mt-4">
          <h3 className="font-semibold mb-2">Verification Results:</h3>
          <ul>
            {statusList.map((s, idx) => (
              <li
                key={idx}
                className={`p-2 rounded mb-1 ${
                  s.success ? "bg-green-700" : "bg-red-700"
                }`}
              >
                <span className="font-medium">{s.filename}</span>: {s.message}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
