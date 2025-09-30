import { createClient } from "@supabase/supabase-js";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(req: NextRequest) {
  // Check if the path is for the downloadFile API
  if (req.nextUrl.pathname.startsWith("/api/downloadFile")) {
    const authHeader = req.headers.get("authorization");
    const { filePath } = await req.json();
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return NextResponse.json(
        { error: "Unauthorized", errorFrom: "middleware" },
        { status: 401 }
      );
    }
    if (!filePath) {
      return NextResponse.json(
        { error: "File path is required", errorFrom: "middleware" },
        { status: 400 }
      );
    }

    const token = authHeader.split(" ")[1];

    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL as string,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY as string,
      {
        global: {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      }
    );

    const {
      data: { user },
      error: authError,
    } = await supabase.auth.getUser(token);

    if (authError || !user) {
      return NextResponse.json(
        { error: "Invalid authentication token", errorFrom: "middleware" },
        { status: 401 }
      );
    }

    const { data: fileRecord, error: dbError } = await supabase
      .from("files")
      .select("*")
      .eq("file_path", filePath)
      .single();

    if (dbError || !fileRecord) {
      return NextResponse.json({ error: "File not found" }, { status: 404 });
    }

    if (!fileRecord.is_public && fileRecord.user_id !== user.id) {
      return NextResponse.json({ error: "Access denied" }, { status: 403 });
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/api/downloadFile/:path*"],
};
