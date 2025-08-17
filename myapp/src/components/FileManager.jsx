import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import toast from "react-hot-toast";

export default function FileManager() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [recipients, setRecipients] = useState("");
  const [username, setUsername] = useState("lash");

  const fetchFiles = useCallback(async () => {
    try {
      const { data } = await axios.get("http://localhost:8000/files", { params: { username } });
      setFiles(Array.isArray(data) ? data : data.files || []);
    } catch (err) {
      console.error(err);
      toast.error("Failed to fetch files");
    }
  }, [username]);

  useEffect(() => {
    fetchFiles();
  }, [fetchFiles]);

  const uploadFile = async () => {
    if (!selectedFile) return toast.error("Select a file first");
    if (!recipients) return toast.error("Enter at least one recipient");

    const recipientList = recipients.split(",").map(r => r.trim());
    const formData = new FormData();
    formData.append("owner", username);
    recipientList.forEach(r => formData.append("recipients", r));
    formData.append("f", selectedFile);

    try {
      await axios.post("http://localhost:8000/files/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      toast.success("File uploaded");
      setSelectedFile(null);
      setRecipients("");
      fetchFiles();
    } catch (err) {
      console.error(err.response || err);
      toast.error("Upload failed");
    }
  };

  const downloadFile = async (fileId, filename) => {
    try {
      const res = await axios.get(`http://localhost:8000/files/${fileId}/download`, {
        params: { username },
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success("File downloaded successfully");
    } catch (err) {
      console.error(err.response || err);
      toast.error("Download failed");
    }
  };

  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg hover:shadow-xl transition duration-300 max-w-md mx-auto">
      <h2 className="text-xl font-bold text-indigo-400 mb-4">📂 File Management</h2>

      {/* Username */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-400 mb-1">Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-2 border border-gray-700 rounded-lg bg-gray-900 text-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
      </div>

      {/* Recipients */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-400 mb-1">Recipients (comma-separated)</label>
        <input
          type="text"
          value={recipients}
          onChange={(e) => setRecipients(e.target.value)}
          className="w-full p-2 border border-gray-700 rounded-lg bg-gray-900 text-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
      </div>

      {/* File Upload */}
      <div className="mb-4">
        <input
          type="file"
          onChange={(e) => setSelectedFile(e.target.files[0])}
          className="w-full text-gray-200"
        />
      </div>

      <button
        onClick={uploadFile}
        className="bg-indigo-600 text-white px-5 py-2 rounded-lg shadow hover:bg-indigo-500 transition duration-300 mb-6"
      >
        Encrypt & Upload
      </button>

      {/* File List */}
      <h3 className="text-md font-semibold mb-2 text-gray-200">Files Shared With You</h3>
      <div className="max-h-64 overflow-y-auto">
        {files.length === 0 && <p className="text-gray-400">No files yet.</p>}
        {files.map((f) => (
          <div
            key={f.id}
            className="flex justify-between items-center bg-gray-700 p-3 rounded-lg mt-2 border border-gray-600 hover:bg-gray-600 transition"
          >
            <span className="text-gray-200">{f.orig_filename}</span>
            <button
              className="text-indigo-400 text-sm hover:underline"
              onClick={() => downloadFile(f.id, f.orig_filename)}
            >
              Download
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
