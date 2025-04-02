from fastapi import APIRouter, HTTPException, Response
import markdown
import os
from pathlib import Path
import re

router = APIRouter()

@router.get("/api/get-release-notes")
async def get_release_notes():
    try:
        # Get Markdown file path
        md_path = Path("app/pages/release.md")
        
        # Check if file exists
        if not md_path.exists():
            raise HTTPException(status_code=404, detail="Release notes file not found")
        
        # Read Markdown file
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        
        # Convert Markdown to HTML with extensions for better formatting
        html_content = markdown.markdown(
            md_content,
            extensions=['extra', 'nl2br']
        )
        
        # Clean up any remaining newlines
        html_content = html_content.replace('\n', '')
        
        # Return as plain text with HTML content type
        return Response(content=html_content, media_type="text/html")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error occurred while fetching release notes: {str(e)}")
