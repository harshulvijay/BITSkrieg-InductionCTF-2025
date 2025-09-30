# File Upload App with Supabase Authentication

A Next.js application that allows users to upload and manage files with authentication using Supabase.

## Features

- **Authentication**: Email/password authentication using Supabase Auth
- **File Upload**: Upload files up to 1MB with custom names
- **Public/Private Files**: Choose whether files are public or private
- **File Management**: View and download your uploaded files
- **Public File Gallery**: Browse all public files from other users
- **Secure Downloads**: Protected download URLs with authentication middleware
- **Random File Names**: Files are stored with random names for security

## Setup Instructions

### 1. Supabase Setup

1. Create a new project at [https://supabase.com](https://supabase.com)
2. Go to **Settings > API** and copy your URL and anon key (already configured in `.env.local`)

### 2. Database Setup

Run the following SQL commands in your Supabase SQL Editor:

```sql
-- Create the files table
CREATE TABLE files (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  file_name TEXT NOT NULL,
  file_path TEXT NOT NULL,
  file_size INTEGER NOT NULL,
  is_public BOOLEAN DEFAULT false,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable Row Level Security
ALTER TABLE files ENABLE ROW LEVEL SECURITY;

-- Create policies
-- Users can insert their own files
CREATE POLICY "Users can insert their own files" ON files
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can view their own files
CREATE POLICY "Users can view their own files" ON files
  FOR SELECT USING (auth.uid() = user_id);

-- Everyone can view public files
CREATE POLICY "Everyone can view public files" ON files
  FOR SELECT USING (is_public = true);

-- Users can update their own files
CREATE POLICY "Users can update their own files" ON files
  FOR UPDATE USING (auth.uid() = user_id);

-- Users can delete their own files
CREATE POLICY "Users can delete their own files" ON files
  FOR DELETE USING (auth.uid() = user_id);
```

### 3. Storage Setup

1. Go to **Storage** in your Supabase dashboard
2. Create a new bucket called `files`
3. Set the bucket to **Private** (we'll handle permissions via RLS)
4. In the bucket settings, create the following policies:

```sql
-- Allow authenticated users to upload files
CREATE POLICY "Allow authenticated uploads" ON storage.objects
  FOR INSERT WITH CHECK (bucket_id = 'files' AND auth.role() = 'authenticated');

-- Allow users to view their own files and public files
CREATE POLICY "Allow authenticated access" ON storage.objects
  FOR SELECT USING (bucket_id = 'files' AND auth.role() = 'authenticated');

-- Allow users to delete their own files (optional)
CREATE POLICY "Allow users to delete own files" ON storage.objects
  FOR DELETE USING (bucket_id = 'files' AND auth.uid()::text = (storage.foldername(name))[1]);
```

### 4. Run the Application

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start the development server:

   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Usage

1. **Sign Up/Sign In**: Create an account or sign in with existing credentials
2. **Upload Files**:
   - Select a file (max 1MB)
   - Give it a custom name
   - Choose whether to make it public or private
3. **View Files**:
   - Use the tabs to switch between Upload, Public Files, and My Files
   - Download files by clicking the Download button
4. **File Security**:
   - Private files are only accessible to the uploader
   - Public files can be viewed by anyone
   - All downloads require authentication

## API Routes

- `POST /api/downloadFile`: Returns a signed download URL for a file
  - Requires authentication via Bearer token
  - Checks file permissions (public files or user-owned files)
  - Returns temporary signed URLs that expire in 60 seconds

## Middleware

The application includes middleware that:

- Protects the `/api/downloadFile` route
- Requires Bearer token authentication
- Validates requests before they reach the API handler

## Tech Stack

- **Frontend**: Next.js 15, React 19, TypeScript
- **Styling**: Tailwind CSS
- **Backend**: Supabase (Authentication, Database, Storage)
- **File Storage**: Supabase Storage (S3-compatible)

## Security Features

- Row Level Security (RLS) on database tables
- Random file names to prevent guessing
- Protected API routes with middleware
- Temporary signed URLs for downloads
- File size limits (1MB)
- Authentication required for all file operations
