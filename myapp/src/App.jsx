import React from "react";
import ActivityLog from "./components/ActivityLog";
import EncryptionPanel from "./components/EncryptionPanel";
import VerificationPanel from "./components/VerficationPanel";
import FileManager from "./components/FileManager";
import { Toaster } from "react-hot-toast";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-900 p-8 font-sans text-gray-200">
      {/* Header */}
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-extrabold text-indigo-400">
          🔒 SecureVault
        </h1>
        <button className="bg-indigo-600 text-white px-5 py-2 rounded-lg shadow hover:bg-indigo-500 transition duration-300">
          Manage Keys
        </button>
      </header>

      {/* Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div>
          <EncryptionPanel />
        </div>
        <div>
          <FileManager />
        </div>
        <div>
          <VerificationPanel />
        </div>
      </div>

      {/* Activity Log */}
      <div className="mt-10">
        <ActivityLog />
      </div>

      <Toaster position="top-right" />
    </div>
  );
}
