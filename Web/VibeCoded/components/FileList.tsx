"use client";

import { useState } from "react";
import { FileRecord } from "@/utils/fileUtils";
import { supabase } from "@/lib/supabase";

interface FileListProps {
  files: FileRecord[];
  title: string;
  showDownloadButton?: boolean;
}

export default function FileList({
  files,
  title,
  showDownloadButton = false,
}: FileListProps) {
  const [downloading, setDownloading] = useState<string | null>(null);

  const handleDownload = async (file: FileRecord) => {
    setDownloading(file.id);
    try {
      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session?.access_token) {
        throw new Error("Not authenticated");
      }

      const response = await fetch("/api/downloadFile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${session.access_token}`,
        },
        body: JSON.stringify({ filePath: file.file_path }),
      });

      if (!response.ok) {
        throw new Error("Download failed");
      }

      const { downloadUrl } = await response.json();

      // Create a temporary link to download the file
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = file.name;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error("Download error:", error);
      alert("Download failed");
    } finally {
      setDownloading(null);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="bg-gray-800 p-6 rounded-xl shadow-xl border border-gray-700">
      <div className="flex items-center mb-6">
        <span className="text-2xl mr-3">
          {title.includes("Public") ? "🌐" : "📁"}
        </span>
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        <span className="ml-auto text-sm text-gray-400">
          {files.length} {files.length === 1 ? "file" : "files"}
        </span>
      </div>

      {files.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📂</div>
          <p className="text-gray-400 text-lg">No files found</p>
          <p className="text-gray-500 text-sm mt-1">
            {title.includes("Public")
              ? "No public files have been shared yet"
              : "Upload your first file to get started"}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {files.map((file) => (
            <div
              key={file.id}
              className="flex items-center justify-between p-4 bg-gray-700 border border-gray-600 rounded-lg hover:bg-gray-650 transition-colors duration-200"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center mb-2">
                  <span className="text-lg mr-2">📄</span>
                  <h4 className="font-medium text-white truncate">
                    {file.name}
                  </h4>
                </div>
                <div className="flex items-center text-sm text-gray-400 space-x-4">
                  <span className="flex items-center">
                    <span className="mr-1">💾</span>
                    {formatFileSize(file.file_size)}
                  </span>
                  <span className="flex items-center">
                    <span className="mr-1">📅</span>
                    {formatDate(file.created_at)}
                  </span>
                  <span
                    className={`flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                      file.is_public
                        ? "bg-green-900/50 text-green-300 border border-green-500/50"
                        : "bg-orange-900/50 text-orange-300 border border-orange-500/50"
                    }`}
                  >
                    <span className="mr-1">{file.is_public ? "🌐" : "🔒"}</span>
                    {file.is_public ? "Public" : "Private"}
                  </span>
                </div>
              </div>

              {showDownloadButton && (
                <button
                  onClick={() => handleDownload(file)}
                  disabled={downloading === file.id}
                  className="ml-4 px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 flex items-center"
                >
                  {downloading === file.id ? (
                    <>
                      <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-2"></div>
                      Downloading...
                    </>
                  ) : (
                    <>
                      <span className="mr-1">⬇️</span>
                      Download
                    </>
                  )}
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
