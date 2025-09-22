from fastapi import Request, UploadFile, File, Form, HTTPException, Header
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
import json

from utils import simplify_metadata, extract_metadata, is_valid_metadata
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

async def chat(
    request: Request,
    gem_id: Optional[str] = None,
    x_chat_metadata: Optional[str] = Header(None, alias="X-Chat-Metadata"),
    files: List[UploadFile] = File(None),
):
    try:
        gemini_client = request.app.state.gemini_client

        # Decrypt metadata if provided in headers
        metadata = None
        if x_chat_metadata:
            if is_valid_metadata(x_chat_metadata):
                try:
                    metadata = extract_metadata(x_chat_metadata)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Failed to extract metadata: {str(e)}")
            else:
                metadata = None

        is_new_chat = True
        if metadata:
            is_new_chat = False

        # Initialize chat with metadata
        chat = gemini_client.start_chat(model="gemini-2.5-flash", metadata=metadata, gem=gem_id)

        # Model set to default gemini-2.5-flash
        
        # Check content type to determine if it's JSON or form data
        content_type = request.headers.get('content-type', '')
    
        if 'multipart/form-data' in content_type:
            # Handle file uploads
            form_data = await request.form()
            message = form_data.get('message', '')
            
            if not message and not files:
                raise HTTPException(status_code=400, detail="Either message or files must be provided")
                
            # Process files if any
            file_contents = []
            if files:
                for file in files:
                    content = await file.read()
                    file_contents.append((file.filename, content, file.content_type))
            
            response = await chat.send_message(message, files=[file_contents])
        else:
            # Handle JSON request
            try:
                json_data = await request.json()
                chat_request = ChatRequest(**json_data)
                response = await chat.send_message(chat_request.message, files=[])
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON data")
        
        # Encrypt the updated metadata for the next request
        simplified_metadata = simplify_metadata(chat.metadata)

        return JSONResponse(
            content={"data": {
                "text": response.text,
                "is_new_chat": is_new_chat,
                "user": request.state.user
            }},
            status_code=201,
            headers={"X-Chat-Metadata": simplified_metadata}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
