import os
import sys
from datetime import datetime
from openclaw.tools import browser, kimi_chat, write

def main(user_handle: str):
    print(f"[X Monitor] Starting monitoring for @{user_handle}'s bookmarks...")
    
    bookmarks_url = f"https://x.com/{user_handle}/bookmarks"
    os.makedirs("memory", exist_ok=True) # Ensure memory directory exists
    memory_file = f"memory/x-bookmarks-{datetime.now().strftime('%Y-%m-%d')}.md"
    
    # Attempt to open the bookmarks page
    try:
        print(f"[X Monitor] Attempting to open: {bookmarks_url}")
        res = browser(action="open", targetUrl=bookmarks_url, profile="openclaw", timeoutMs=30000)
        print(f"[X Monitor] Browser open response: {res}")

        snapshot_res = browser(action="snapshot", snapshotFormat="text", timeoutMs=15000)
        page_content = snapshot_res.get("content", "")
        # print(f"[X Monitor] Page content snippet: {page_content[:500]}...") # Debugging line

        # Basic check for login elements or if bookmarks content is missing
        if "Log in to X" in page_content or "Sign in" in page_content and "bookmarks" not in page_content.lower():
            message = f"[X Monitor] Authentication required for @{user_handle}'s bookmarks. Please provide session cookies or an API key securely.\n"
            message += f"To proceed, I need a way to authenticate  with your X account. \n"
            message += f"Option 1: Provide X.com session cookies (complex, less secure for long-term). \n"
            message += f"Option 2: Explore X Developer API for bookmark access (most secure, if available)."
            print(message)
            write(path=memory_file, content=message)
            return # Stop execution if auth is needed

        # --- Placeholder for actual bookmark extraction and research ---
        mock_posts = [
            {"topic": "Latest AI agent architectures", "url": "https://x.com/post1"},
            {"topic": "Venture capital trends in AI", "url": "https://x.com/post2"},
        ]

        report_content = f"# X Bookmark Monitor Report for @{user_handle} ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n"
        report_content += "## Key Insights from Bookmarks\n\n"

        for post in mock_posts:
            print(f"[X Monitor] Researching topic: {post['topic']} from {post['url']}")
            kimi_research = kimi_chat(
                prompt=f"Provide a concise summary and potential implementation ideas for a product partner based on the topic: {post['topic']}"
            )
            research_summary = kimi_research.get("choices", [{}])[0].get("message", {}).get("content", "No summary.")
            
            report_content += f"### Topic: {post['topic']} \n"
            report_content += f"- Source: {post['url']}\n"
            report_content += f"- **Kimi's Research:**\n{research_summary}\n\n"

        write(path=memory_file, content=report_content)
        print(f"[X Monitor] Report saved to {memory_file}")

    except Exception as e:
        error_message = f"[X Monitor] Error during monitoring for @{user_handle}: {e}"
        print(error_message)
        write(path=memory_file, content=error_message)
    finally:
        browser(action="close") # Ensure browser is closed

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(user_handle=sys.argv[1])
    else:
        print("Usage: python3 main.py <user_handle>")
