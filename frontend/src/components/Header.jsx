
import React from "react";
import { BellIcon } from "@heroicons/react/24/outline"; // Or use any SVG/icon

export default function Header() {
  return (
    <header className="bg-gray-900 px-6 py-4 flex items-center justify-between border-b border-gray-700">
      <div className="text-blue-300 font-semibold text-lg">🔒 SecureVault</div>
      <button className="bg-gray-800 hover:bg-blue-700 text-white px-4 py-2 rounded flex items-center">
        <BellIcon className="h-5 w-5 mr-2" />
        Manage Keys
      </button>
    </header>
  );
}
