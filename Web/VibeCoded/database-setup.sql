-- Complete Database Setup for File Upload App
-- Run these commands in your Supabase SQL Editor

-- 1. Drop the table if it exists to start fresh
DROP TABLE IF EXISTS files CASCADE;

-- 2. Create the files table with proper structure
CREATE TABLE files (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_path TEXT NOT NULL,
  file_size INTEGER NOT NULL,
  is_public BOOLEAN DEFAULT false,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Enable Row Level Security
ALTER TABLE files ENABLE ROW LEVEL SECURITY;

-- 4. Create RLS policies with explicit role targeting

-- Allow authenticated users to insert their own files
CREATE POLICY "authenticated_users_insert_own_files" ON files
  FOR INSERT 
  TO authenticated
  WITH CHECK (auth.uid() = user_id AND auth.uid() IS NOT NULL);

-- Allow users to view their own files
CREATE POLICY "authenticated_users_select_own_files" ON files
  FOR SELECT 
  TO authenticated
  USING (auth.uid() = user_id AND auth.uid() IS NOT NULL);

-- Allow everyone to view public files (including authenticated and anon)
CREATE POLICY "everyone_select_public_files" ON files
  FOR SELECT 
  TO authenticated, anon
  USING (is_public = true);

-- Allow users to update their own files
CREATE POLICY "authenticated_users_update_own_files" ON files
  FOR UPDATE 
  TO authenticated
  USING (auth.uid() = user_id AND auth.uid() IS NOT NULL)
  WITH CHECK (auth.uid() = user_id AND auth.uid() IS NOT NULL);

-- Allow users to delete their own files
CREATE POLICY "authenticated_users_delete_own_files" ON files
  FOR DELETE 
  TO authenticated
  USING (auth.uid() = user_id AND auth.uid() IS NOT NULL);

CREATE POLICY "Allow authenticated uploads" ON storage.objects
  FOR INSERT WITH CHECK (bucket_id = 'files' AND auth.role() = 'authenticated');

-- Allow users to view their own files and public files
CREATE POLICY "Allow authenticated access" ON storage.objects
  FOR SELECT USING (bucket_id = 'files' AND auth.role() = 'authenticated');

-- Allow users to delete their own files (optional)
CREATE POLICY "Allow users to delete own files" ON storage.objects
  FOR DELETE USING (bucket_id = 'files' AND auth.uid()::text = (storage.foldername(name))[1]);


-- 5. Grant necessary permissions explicitly
GRANT USAGE ON SCHEMA public TO authenticated, anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON files TO authenticated;
GRANT SELECT ON files TO anon;