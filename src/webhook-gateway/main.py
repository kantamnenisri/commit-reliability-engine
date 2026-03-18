from fastapi import FastAPI, Request
import uvicorn

app = FastAPI(title="Commit Reliability Engine - Webhook Gateway")

@app.post("/webhook")
async def receive_github_webhook(request: Request):
    # Parse the incoming JSON payload from GitHub
    payload = await request.json()
    
    # Check if this is a 'push' event (a code commit)
    if "commits" in payload:
        for commit in payload["commits"]:
            commit_id = commit.get("id")
            author = commit.get("author", {}).get("name")
            message = commit.get("message")
            added_files = commit.get("added", [])
            modified_files = commit.get("modified", [])
            
            # For now, we will just print this to the console.
            # Later, we will send this to the Feature Extractor.
            print(f"New Commit Detected: {commit_id}")
            print(f"Author: {author}")
            print(f"Message: {message}")
            print(f"Files Modified: {len(modified_files)}")
            print("**************************************************")
            
        return {"status": "success", "message": "Commits processed"}
    
    return {"status": "ignored", "message": "Not a push event"}

@app.get("/ping")
async def ping():
    return "OK"

if __name__ == "__main__":
    # Runs the server locally on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)