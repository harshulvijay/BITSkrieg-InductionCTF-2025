"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import AuthForm from "@/components/AuthForm";
import FileUpload from "@/components/FileUpload";
import FileList from "@/components/FileList";
import { getPublicFiles, getUserFiles, FileRecord } from "@/utils/fileUtils";

export default function Home() {
  const { user, loading, signOut } = useAuth();
  const [authMode, setAuthMode] = useState<"signin" | "signup">("signin");
  const [publicFiles, setPublicFiles] = useState<FileRecord[]>([]);
  const [userFiles, setUserFiles] = useState<FileRecord[]>([]);
  const [activeTab, setActiveTab] = useState<"upload" | "public" | "myfiles">(
    "upload"
  );

  const loadFiles = async () => {
    try {
      const [publicFilesData, userFilesData] = await Promise.all([
        getPublicFiles(),
        user ? getUserFiles() : Promise.resolve([]),
      ]);
      setPublicFiles(publicFilesData);
      setUserFiles(userFilesData);
    } catch (error) {
      console.error("Error loading files:", error);
    }
  };

  useEffect(() => {
    if (user) {
      loadFiles();
    }
  }, [user]);

  const handleUploadSuccess = () => {
    loadFiles();
  };

  const handleSignOut = async () => {
    try {
      await signOut();
      setPublicFiles([]);
      setUserFiles([]);
      setActiveTab("upload");
    } catch (error) {
      console.error("Sign out error:", error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="flex flex-col items-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
          <div className="text-lg text-gray-300">Loading...</div>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-gray-900">
        <AuthForm
          mode={authMode}
          onToggleMode={() =>
            setAuthMode(authMode === "signin" ? "signup" : "signin")
          }
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4 bg-gray-900">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="bg-gray-800 p-6 rounded-xl shadow-xl mb-6 border border-gray-700">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg"></div>
              <h1 className="text-2xl font-bold text-white">File Storage</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-300 text-sm">
                Welcome,{" "}
                <span className="text-blue-400 font-medium">{user.email}</span>
              </span>
              <button
                onClick={handleSignOut}
                className="px-4 py-2 text-sm bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200 font-medium"
              >
                Sign Out
              </button>
            </div>
          </div>
        </header>

        {/* Navigation Tabs */}
        <div className="bg-gray-800 p-1 rounded-xl shadow-xl mb-6 border border-gray-700">
          <nav className="flex space-x-1">
            <button
              onClick={() => setActiveTab("upload")}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-lg transition-all duration-200 ${
                activeTab === "upload"
                  ? "bg-blue-600 text-white shadow-lg"
                  : "text-gray-300 hover:text-white hover:bg-gray-700"
              }`}
            >
              📤 Upload Files
            </button>
            <button
              onClick={() => setActiveTab("public")}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-lg transition-all duration-200 ${
                activeTab === "public"
                  ? "bg-blue-600 text-white shadow-lg"
                  : "text-gray-300 hover:text-white hover:bg-gray-700"
              }`}
            >
              🌐 Public Files ({publicFiles.length})
            </button>
            <button
              onClick={() => setActiveTab("myfiles")}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-lg transition-all duration-200 ${
                activeTab === "myfiles"
                  ? "bg-blue-600 text-white shadow-lg"
                  : "text-gray-300 hover:text-white hover:bg-gray-700"
              }`}
            >
              📁 My Files ({userFiles.length})
            </button>
          </nav>
        </div>

        {/* Content */}
        <div className="space-y-6">
          {activeTab === "upload" && (
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          )}

          {activeTab === "public" && (
            <FileList
              files={publicFiles}
              title="Public Files"
              showDownloadButton={true}
            />
          )}

          {activeTab === "myfiles" && (
            <FileList
              files={userFiles}
              title="My Files"
              showDownloadButton={true}
            />
          )}
        </div>
      </div>
    </div>
  );
}
