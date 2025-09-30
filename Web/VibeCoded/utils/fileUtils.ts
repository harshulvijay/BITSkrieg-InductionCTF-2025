import { supabase } from "@/lib/supabase";

export interface FileRecord {
  id: string;
  name: string;
  file_name: string;
  file_path: string;
  file_size: number;
  is_public: boolean;
  created_at: string;
  user_id: string;
}

export const generateRandomFileName = (originalName: string): string => {
  const extension = originalName.split(".").pop();
  const randomString =
    Math.random().toString(36).substring(2) + Date.now().toString(36);
  return `${randomString}.${extension}`;
};

export const uploadFile = async (
  file: File,
  fileName: string,
  isPublic: boolean
): Promise<string> => {
  if (file.size > 1024 * 1024) {
    throw new Error("File size must be less than 1MB");
  }

  const randomFileName = generateRandomFileName(file.name);
  const filePath = `${isPublic ? "public" : "private"}/${randomFileName}`;

  const { data, error } = await supabase.storage
    .from("files")
    .upload(filePath, file);

  if (error) {
    throw error;
  }
  const { data: userData, error: userError } = await supabase.auth.getUser();

  if (userError) {
    await supabase.storage.from("files").remove([filePath]);
    throw new Error("Authentication failed");
  }

  if (!userData.user) {
    await supabase.storage.from("files").remove([filePath]);
    throw new Error("User not authenticated");
  }

  const { data: insertData, error: dbError } = await supabase
    .from("files")
    .insert({
      name: fileName,
      file_name: file.name,
      file_path: filePath,
      file_size: file.size,
      is_public: isPublic,
      user_id: userData.user.id,
    })
    .select();

  if (dbError) {
    await supabase.storage.from("files").remove([filePath]);
    throw new Error(`Database error: ${dbError.message}`);
  }

  return filePath;
};

export const getPublicFiles = async (): Promise<FileRecord[]> => {
  const { data, error } = await supabase
    .from("files")
    .select("*")
    .eq("is_public", true)
    .order("created_at", { ascending: false });

  if (error) {
    throw error;
  }

  return data || [];
};

export const getUserFiles = async (): Promise<FileRecord[]> => {
  const { data: user } = await supabase.auth.getUser();
  if (!user.user) {
    throw new Error("User not authenticated");
  }

  const { data, error } = await supabase
    .from("files")
    .select("*")
    .eq("user_id", user.user.id)
    .order("created_at", { ascending: false });

  if (error) {
    throw error;
  }

  return data || [];
};
