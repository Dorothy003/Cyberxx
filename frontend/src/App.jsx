// App.jsx
import Header from "./components/Header";
import EncryptionPanel from "./components/EncryptionPanel";
import FileManagementPanel from "./components/FileManagementPanel";
import IntegritySection from "./components/IntegritySection";
import RecentActivity from "./components/RecentActivity";

export default function App() {
  return (
    <div className="securevault-app bg-gray-900  min-h-screen text-gray-200 font-sans">
      <Header />
      <div className="container mx-auto px-4 py-6">
        <h2 className="text-xl font-semibold mb-1">Secure File Management</h2>
        <p className="mb-6 text-gray-400">Encrypt, store, and verify your files with military-grade security</p>
        <div className="main-panels flex flex-col md:flex-row gap-6 mb-8">
          <EncryptionPanel />
          <FileManagementPanel />
          <IntegritySection />
        </div>
        <RecentActivity />
      </div>
      <footer className="text-xs text-gray-500 py-4 text-center border-t border-gray-700">
        © 2025 SecureVault. All rights reserved.
      </footer>
    </div>
  );
}
