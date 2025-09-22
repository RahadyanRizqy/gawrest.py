from fastapi import Request, Body, Header, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
import json

async def gems_get(
    request: Request, 
    gem_id: Optional[str] = None,
    predefined: Optional[str] = Query(default=None),
    hidden: Optional[str] = Query(default=None)
):
    try:
        gemini_client = request.app.state.gemini_client

        if hidden is None:
            hidden = False
        else:
            hidden = hidden.lower() in ["", "true", "1", "yes"]

        await gemini_client.fetch_gems(include_hidden=hidden)
        gems = gemini_client.gems

        if predefined is None:
            pass

        if predefined is not None:
            if predefined.lower() in ["", "true", "1", "yes"]:
                gems = gems.filter(predefined=True)

            if predefined.lower() in ["false", "0", "no"]:
                gems = gems.filter(predefined=False)

        if gem_id:
            gems = gems.get(id=gem_id)

        return JSONResponse(
            content={"data": {
                "gems": jsonable_encoder(gems),
                "user": request.state.user
            }},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def gems_post(
    request: Request, 
    name: str,
    prompt: str,
    description: str
    
):
    try:
        gemini_client = request.app.state.gemini_client
        created_gem = await gemini_client.create_gem(
            name=name,
            prompt=prompt,
            description=description
        )
        return JSONResponse(
            content={"data": {
                "created_gem": jsonable_encoder(created_gem),
                "user": request.state.user
            }},
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def gems_put(
    request: Request, 
    gem_id: str,
    name: Optional[str] = None,
    prompt: Optional[str] = None,
    description: Optional[str] = None
):
    try:    
        gemini_client = request.app.state.gemini_client
        await gemini_client.fetch_gems(include_hidden=True)

        update_fields = {}
        if name is not None:
            update_fields["name"] = name
        if prompt is not None:
            update_fields["prompt"] = prompt
        if description is not None:
            update_fields["description"] = description

        updated_gem = await gemini_client.update_gem(
            gem=gem_id,
            **update_fields
        )
        return JSONResponse(
            content={"data": {
                "updated_gem": jsonable_encoder(updated_gem),
                "user": request.state.user
            }},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def gems_delete(
    request: Request, 
    gem_id: Optional[str] = None,
    name: Optional[str] = None
):
    try:
        gemini_client = request.app.state.gemini_client
        await gemini_client.fetch_gems(include_hidden=False)
        gems = gemini_client.gems

        deleted_gem = None
        if name:
            deleted_gem = gems.get(name=name)
            await gemini_client.delete_gem(deleted_gem)
        elif gem_id:
            deleted_gem = gems.get(id=gem_id)
            await gemini_client.delete_gem(gem_id)
        
        return JSONResponse(
            content={"data": {
                "deleted_gem": jsonable_encoder(deleted_gem),
                "user": request.state.user
            }},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

async def gems(
    request: Request,
    gem_id: Optional[str] = None,
    predefined: Optional[str] = Query(default=None),
    hidden: Optional[str] = Query(default=None),
    name: Optional[str] = Body(None),
    prompt: Optional[str] = Body(None),
    description: Optional[str] = Body(None),
):
    if request.method == "GET":
        return await gems_get(request, gem_id=gem_id, predefined=predefined, hidden=hidden)
    elif request.method == "POST":
        return await gems_post(request, name=name, prompt=prompt, description=description)
    elif request.method == "PUT":
        return await gems_put(request, gem_id=gem_id, name=name, prompt=prompt, description=description)
    elif request.method == "DELETE":
        return await gems_delete(request, gem_id=gem_id, name=name)

