"""JWT 鉴权依赖：后台接口全局拦截"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.utils.security import decode_token

security = HTTPBearer(auto_error=False)


def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未登录或令牌缺失")
    try:
        payload = decode_token(credentials.credentials)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="无效令牌")
        return username
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌已过期或无效")
