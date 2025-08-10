// App.jsx
import Header from "./components/Header";
import EncryptionPanel from "./components/EncryptionPanel";
import FileManagementPanel from "./components/FileManagementPanel";
import IntegritySection from "./components/IntegritySection";
import RecentActivity from "./components/RecentActivity";
import React, { useState } from "react";

export default function App() {
  // Centralized activity log
  const [activities, setActivities] = useState([
    { text: 'File uploaded: passwords.txt', time: 'May 15, 2025 10:21 AM' },
    { text: 'File encrypted: passwords.txt', time: 'May 15, 2025 10:22 AM' },
    { text: 'Integrity check completed: All files verified', time: 'May 15, 2025 10:23 AM' },
    { text: 'File downloaded: passport_scan.jpg', time: 'May 14, 2025 03:45 PM' },
  ]);

  // You'll pass setActivities to subcomponents as needed!
  return (
    <div className="bg-gray-900 min-h-screen text-gray-200 font-sans">
      <Header />
      <div className="container mx-auto px-4 py-6">
        <h2 className="text-xl font-semibold mb-1">Secure File Management</h2>
        <p className="mb-6 text-gray-400">
          Encrypt, store, and verify your files with military-grade security
        </p>
        <div className="main-panels flex flex-col md:flex-row gap-6 mb-8">
          <EncryptionPanel setActivities={setActivities} />
          <FileManagementPanel setActivities={setActivities} />
          <IntegritySection setActivities={setActivities} />
        </div>
        <RecentActivity activities={activities} />
      </div>
      <footer className="text-xs text-gray-500 py-4 text-center border-t border-gray-700">
        © 2025 SecureVault. All rights reserved.
      </footer>
    </div>
  );
}
