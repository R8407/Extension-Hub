from urllib import request, response
from fastapi import FastAPI, Query, UploadFile, File
import shutil
from pathlib import Path


app = FastAPI()
notes_base_dir = Path("E:/ObsadianNotes") #replace with your obsidian file path
notes = {}

def load_notes():
    notes.clear()
    for md_file in notes_base_dir.rglob("*.md"): #searches for .md files
        with open(md_file, encoding="utf-8", errors="ignore") as f:
            notes[str(md_file)] = f.read() # key: file path as string, value: file content

load_notes()

@app.get("/query")
def query_notes(q: str = Query(..., min_length=1)):
    results = []
    for path, content in notes.items():
        if q.lower() in content.lower():
            results.append({"file": path, "snippet": content[:500]})
    return {"matches": results}

@app.get("/reload")
def reload_notes():
    load_notes()
    return {"status": "reloaded", "count": len(notes)}

@app.post("/write")
async def write_note(file: UploadFile = File(...)):
    with open(f"{notes_base_dir}/notes/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}



@app.post("/export")
async def upload_file(file: UploadFile = File(...)):
    export_path = notes_base_dir / "exports" / file.filename
    export_path.parent.mkdir(parents=True, exist_ok=True)

    with open(export_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    return {"filename": str(export_path)}

