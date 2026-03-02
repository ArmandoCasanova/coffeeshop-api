import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID
from redis import asyncio as aioredis


SESSION_KEY_PREFIX = "session:"
SESSION_TIMEOUT = 24 * 60 * 60


class SessionManager:
    def __init__(self, redis_client: aioredis.Redis):
        self.redis_client = redis_client

    async def create_session(
        self,
        user_id: str,
        user_data: Dict[str, Any],
        device_info: Optional[Dict[str, str]] = None,
        expires_in: int = SESSION_TIMEOUT
    ) -> str:
        try:
            from uuid import uuid4
            session_id = str(uuid4())
            
            session_data = {
                "user_id": user_id,
                "session_id": session_id,
                "created_at": datetime.utcnow().isoformat(),
                "last_activity": datetime.utcnow().isoformat(),
                "device_info": device_info or {},
                **user_data
            }
            
            key = f"{SESSION_KEY_PREFIX}{session_id}"
            
            await self.redis_client.setex(
                key,
                expires_in,
                json.dumps(session_data, default=str)
            )
            
            user_key = f"{SESSION_KEY_PREFIX}{user_id}:sessions"
            await self.redis_client.sadd(user_key, session_id)
            
            return session_id
            
        except Exception as e:
            raise

    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        try:
            key = f"{SESSION_KEY_PREFIX}{session_id}"
            data = await self.redis_client.get(key)
            
            if data:
                session_data = json.loads(data)
                session_data["last_activity"] = datetime.utcnow().isoformat()
                await self.redis_client.setex(key, SESSION_TIMEOUT, json.dumps(session_data, default=str))
                return session_data
            
            return None
        except Exception as e:        
            return None

    async def delete_session(self, session_id: str) -> bool:
        try:
            key = f"{SESSION_KEY_PREFIX}{session_id}"
            
            data = await self.redis_client.get(key)
            if data:
                session_data = json.loads(data)
                user_id = session_data.get("user_id")
                
                await self.redis_client.delete(key)
                if user_id:
                    user_key = f"{SESSION_KEY_PREFIX}{user_id}:sessions"
                    await self.redis_client.srem(user_key, session_id)
                
                return True
            
            return False
        except Exception as e:
            return False

    async def delete_all_user_sessions(self, user_id: str) -> int:
        try:
            user_key = f"{SESSION_KEY_PREFIX}{user_id}:sessions"
            sessions = await self.redis_client.smembers(user_key)
            
            count = 0
            for session_id in sessions:
                key = f"{SESSION_KEY_PREFIX}{session_id.decode() if isinstance(session_id, bytes) else session_id}"
                await self.redis_client.delete(key)
                count += 1
            
            await self.redis_client.delete(user_key)
            
            return count
            
        except Exception as e:
            return 0

    async def is_session_valid(self, session_id: str) -> bool:
        try:
            key = f"{SESSION_KEY_PREFIX}{session_id}"
            exists = await self.redis_client.exists(key)
            return exists == 1
        except Exception as e:
            return False

    async def get_user_sessions(self, user_id: str) -> list:
        try:
            user_key = f"{SESSION_KEY_PREFIX}{user_id}:sessions"
            session_ids = await self.redis_client.smembers(user_key)
            
            sessions = []
            for session_id in session_ids:
                session_id_str = session_id.decode() if isinstance(session_id, bytes) else session_id
                session_data = await self.get_session(session_id_str)
                if session_data:
                    sessions.append(session_data)
            
            return sessions
        except Exception as e:
            return []
