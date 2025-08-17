import React, { useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";

export default function EncryptionPanel() {
  const [keys, setKeys] = useState(null);

  const generateKeys = async () => {
    try {
      const { data } = await axios.post("http://localhost:8000/keys/generate");
      setKeys(data);
      toast.success("Keys generated successfully");
    } catch (err) {
      toast.error("Error generating keys");
      console.log(err)
    }
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg hover:shadow-xl transition duration-300">
      <h2 className="text-xl font-bold text-indigo-400 mb-4">🔑 Encryption Tools</h2>

      <button
        onClick={generateKeys}
        className="bg-indigo-600 text-white px-5 py-2 rounded-lg shadow hover:bg-indigo-500 transition duration-300 mb-4"
      >
        Generate New Keys
      </button>

      {keys && (
        <div className="space-y-4">
          <div>
            <p className="text-sm text-gray-400 mb-1">Public Key:</p>
            <textarea
              className="w-full bg-gray-900 border border-gray-700 p-3 rounded-lg text-gray-200 font-mono focus:outline-none focus:ring-2 focus:ring-indigo-400"
              value={keys.public_key}
              readOnly
              rows={3}
            />
          </div>

          <div>
            <p className="text-sm text-gray-400 mb-1">Private Key:</p>
            <textarea
              className="w-full bg-gray-900 border border-gray-700 p-3 rounded-lg text-gray-200 font-mono focus:outline-none focus:ring-2 focus:ring-indigo-400"
              value={keys.private_key}
              readOnly
              rows={3}
            />
          </div>
        </div>
      )}
    </div>
  );
}
