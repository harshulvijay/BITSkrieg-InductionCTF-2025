"use client";

import { useState } from "react";
import { uploadFile } from "@/utils/fileUtils";

interface FileUploadProps {
  onUploadSuccess: () => void;
}

export default function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState("");
  const [isPublic, setIsPublic] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.size > 1024 * 1024) {
        setError("File size must be less than 1MB");
        return;
      }
      setFile(selectedFile);
      setFileName(selectedFile.name.split(".")[0]);
      setError("");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !fileName.trim()) {
      setError("Please select a file and provide a name");
      return;
    }

    setLoading(true);
    setError("");

    try {
      await uploadFile(file, fileName.trim(), isPublic);
      setFile(null);
      setFileName("");
      setIsPublic(false);
      const fileInput = document.getElementById(
        "file-input"
      ) as HTMLInputElement;
      if (fileInput) fileInput.value = "";
      onUploadSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-xl shadow-xl border border-gray-700">
      <div className="flex items-center mb-4">
        <span className="text-2xl mr-3">📤</span>
        <h3 className="text-lg font-semibold text-white">Upload File</h3>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label
            htmlFor="file-input"
            className="block text-sm font-medium text-gray-300 mb-2"
          >
            Select File (max 1MB)
          </label>
          <div className="relative">
            <input
              type="file"
              id="file-input"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-300 bg-gray-700 border border-gray-600 rounded-lg cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 file:mr-4 file:py-2 file:px-4 file:rounded-l-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700 file:cursor-pointer transition-colors duration-200"
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="file-name"
            className="block text-sm font-medium text-gray-300 mb-2"
          >
            Display Name
          </label>
          <input
            type="text"
            id="file-name"
            value={fileName}
            onChange={(e) => setFileName(e.target.value)}
            placeholder="Enter a name for your file"
            className="block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg shadow-sm text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors duration-200"
          />
        </div>

        <div className="flex items-center">
          <input
            type="checkbox"
            id="is-public"
            checked={isPublic}
            onChange={(e) => setIsPublic(e.target.checked)}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-600 bg-gray-700 rounded"
          />
          <label
            htmlFor="is-public"
            className="ml-3 block text-sm text-gray-300"
          >
            <span className="font-medium">Make this file public</span>
            <span className="block text-xs text-gray-400 mt-1">
              Public files can be viewed and downloaded by anyone
            </span>
          </label>
        </div>

        {error && (
          <div className="bg-red-900/50 border border-red-500 text-red-300 text-sm p-3 rounded-lg">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !file || !fileName.trim()}
          className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Uploading...
            </>
          ) : (
            <>
              <span className="mr-2">📤</span>
              Upload File
            </>
          )}
        </button>
      </form>
    </div>
  );
}
