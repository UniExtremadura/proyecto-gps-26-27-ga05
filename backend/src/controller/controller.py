from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import auth
from datetime import datetime
from typing import Optional, Tuple
import json
from model.model import Model
from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory
from config.config import ALLOWED_ORIGINS, ERROR_MESSAGES, SUCCESS_MESSAGES

# Inicialización de FastAPI
app = FastAPI(
    title="Subsonic Festival API",
    version="1.0.0",
    description="API REST para Subsonic Festival con Firebase y MVC-DAO-FACTORY"
)

# Agregar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# configuración de la aplicación

# Componentes
mymodel = Model(factory=FirebaseDAOFactory())

# Sesiones (en producción, usar Redis)
# diccionario en memoria para mapear uid/token a datos de sesion activos
sessions = {}

# Credenciales demo para fallback de login cuando Firebase Auth no está disponible.
DEMO_LOGIN_CREDENTIALS = {
    "cliente.demo@subsonicfest.com": "Cliente123!",
    "proveedor.demo@subsonicfest.com": "Proveedor123!",
    "gestor.demo@subsonicfest.com": "Gestor123!"
}


@app.on_event("shutdown")
async def clear_purchase_history_on_shutdown():
    """Borra el historial de compras (pedidos) al cerrar el backend."""
    # elimina pedidos al apagar para mantener entorno demo limpio
    deleted = mymodel.clear_all_pedidos()
    print(f"Shutdown cleanup completado. Pedidos eliminados: {deleted}")

# utilidades

def verify_session(request: Request):
    """Verifica si el usuario tiene sesión activa (por cookie o por header Authorization)"""
    # intenta reconstruir sesion consultando firestore a partir del uid
    def _hydrate_session(uid: str):
        if not uid:
            return None
        user = mymodel.get_usuario(uid)
        if user and not user.is_Empty():
            # guarda sesion reconstruida para siguientes solicitudes
            user_data = user.user_to_dict()
            sessions[uid] = user_data
            return user_data
        return None

    # Intentar verificar por cookie primero
    cookie = request.cookies.get("session")
    if cookie:
        if cookie in sessions:
            return sessions[cookie]
        rehydrated = _hydrate_session(cookie)
        if rehydrated:
            return rehydrated
    
    # Si no hay cookie, intentar por header Authorization
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        session_token = auth_header[7:]  # Remover "Bearer "
        if session_token in sessions:
            return sessions[session_token]

        # Permitir que el token sea UID persistido en localStorage
        rehydrated = _hydrate_session(session_token)
        if rehydrated:
            return rehydrated

        # Compatibilidad: si llega un Firebase ID token, extraer UID y reconstruir sesión
        try:
            decoded = auth.verify_id_token(session_token)
            uid = decoded.get("uid")
            rehydrated = _hydrate_session(uid)
            if rehydrated:
                return rehydrated
        except Exception:
            pass
    
    return None

# api health

@app.get("/")
async def root():
    """Ruta raíz amigable para comprobar que el backend está vivo"""
    # endpoint minimo para comprobar disponibilidad de la api
    return {
        "status": "ok",
        "message": "Subsonic Festival API activa",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
async def health():
    """Verifica el estado del servidor"""
    # devuelve timestamp para comprobar latencia y estado en tiempo real
    return {
        "status": "ok",
        "message": "Servidor funcionando correctamente",
        "timestamp": datetime.now().isoformat()
    }

# autenticación

@app.post("/api/auth/login")
async def login(data: dict = Body(...)):
    """Login con Firebase ID Token"""
    try:
        # obtiene el token enviado por el frontend
        idtoken = data.get("token")
        if not idtoken:
            raise HTTPException(status_code=400, detail="Token required")

        decoded_token = auth.verify_id_token(idtoken)
        uid = decoded_token.get('uid')
        email = decoded_token.get('email')
        # normaliza rol solicitado por el cliente para crear perfil inicial
        requested_role = str(data.get("role") or "cliente").strip().lower()
        if requested_role not in {"cliente", "proveedor"}:
            requested_role = "cliente"

        if not uid:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = mymodel.get_usuario(uid)
        
        if user is None or user.is_Empty():
            # Si no existe por UID, intentar recuperar perfil por email para respetar su rol real.
            existing_by_email = None
            if email:
                factory = mymodel.factory
                if not isinstance(factory, FirebaseDAOFactory):
                    raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

                usuarios_collection = factory.connector.get_usuarios_collection()
                if usuarios_collection is not None:
                    docs = usuarios_collection.where("email", "==", email).limit(1).stream()
                    existing_by_email = next(docs, None)

            if existing_by_email is not None and existing_by_email.exists:
                existing_data = existing_by_email.to_dict() or {}
                user_data = {
                    "email": email,
                    "uid": uid,
                    "name": existing_data.get("name") or decoded_token.get('name', ''),
                    "role": existing_data.get("role", "cliente"),
                    "address": existing_data.get("address", ""),
                    "postal_code": existing_data.get("postal_code", ""),
                    "city": existing_data.get("city", ""),
                    "country": existing_data.get("country", ""),
                    "profile_image_url": existing_data.get("profile_image_url", ""),
                    "company_name": existing_data.get("company_name", ""),
                    "business_area": existing_data.get("business_area", ""),
                    "card_number": existing_data.get("card_number", ""),
                    "created_at": existing_data.get("created_at", datetime.now().isoformat()),
                    "updated_at": datetime.now().isoformat()
                }
            else:
                # crea perfil minimo con datos del token cuando no hay perfil previo
                user_data = {
                    "email": email,
                    "uid": uid,
                    "name": decoded_token.get('name', ''),
                    "role": requested_role,
                    "address": "",
                    "postal_code": "",
                    "city": "",
                    "country": "",
                    "profile_image_url": "",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }

            mymodel.create_usuario(uid, user_data)
            user = mymodel.get_usuario(uid)

        if user and not user.is_Empty():
            user_json = user.user_to_dict()
            # almacena sesion local para acceso rapido en proximas llamadas
            sessions[uid] = user_json
            
            response = JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": SUCCESS_MESSAGES["login_success"],
                    "user": user_json,
                    "sessionToken": uid
                }
            )
            response.set_cookie(key="session", value=uid, httponly=True)
            return response

    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.post("/api/auth/register")
async def register(data: dict = Body(...)):
    """Registro de nuevo usuario"""
    try:
        # normaliza datos principales de registro
        email = (data.get("email") or "").strip().lower()
        password = data.get("password")
        name = (data.get("name") or "").strip()
        role = (data.get("role", "cliente") or "cliente").strip()
        
        if not email or not password or not name:
            raise HTTPException(status_code=400, detail="Missing required fields")

        if len(password) < 6:
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_password"])

        user_data = {
            "email": email,
            "name": name,
            "role": role,
            "address": (data.get("address") or "").strip(),
            "postal_code": (data.get("postal_code") or "").strip(),
            "city": (data.get("city") or "").strip(),
            "country": (data.get("country") or "").strip(),
            "profile_image_url": (data.get("profile_image_url") or "").strip(),
            "updated_at": datetime.now().isoformat()
        }

        if role == "proveedor":
            # completa campos extra exigidos para el perfil proveedor
            user_data["company_name"] = data.get("company_name", "")
            user_data["business_area"] = data.get("business_area", "")
            user_data["card_number"] = data.get("card_number", "")

        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )

            user_data["uid"] = user.uid
            user_data["created_at"] = datetime.now().isoformat()
            mymodel.create_usuario(user.uid, user_data)

            return JSONResponse(
                status_code=201,
                content={
                    "status": "success",
                    "message": SUCCESS_MESSAGES["register_success"],
                    "uid": user.uid
                }
            )
        except auth.EmailAlreadyExistsError:
            # si ya existe auth, sincroniza perfil firestore sin fallar el registro
            existing_user = auth.get_user_by_email(email)
            user_data["uid"] = existing_user.uid

            existing_profile = mymodel.get_usuario(existing_user.uid)
            if existing_profile is None or existing_profile.is_Empty():
                user_data["created_at"] = datetime.now().isoformat()
                mymodel.create_usuario(existing_user.uid, user_data)
            else:
                mymodel.update_usuario(existing_user.uid, user_data)

            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Usuario existente sincronizado correctamente",
                    "uid": existing_user.uid
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Register error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])


@app.post("/api/auth/google-register")
async def google_register(data: dict = Body(...)):
    """Registro/Login con Google usando ID token + datos de perfil opcionales"""
    try:
        # valida token de google emitido en frontend
        idtoken = data.get("token")
        if not idtoken:
            raise HTTPException(status_code=400, detail="Token required")

        decoded_token = auth.verify_id_token(idtoken)
        uid = decoded_token.get("uid")
        email = (decoded_token.get("email") or "").strip().lower()

        if not uid or not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        requested_role = (data.get("role") or "cliente").strip() or "cliente"
        if requested_role not in {"cliente", "gestor", "proveedor"}:
            requested_role = "cliente"

        user = mymodel.get_usuario(uid)

        if user is None or user.is_Empty():
            # busca perfil previo por email para no duplicar usuarios
            existing_by_email = None
            factory = mymodel.factory
            if isinstance(factory, FirebaseDAOFactory):
                usuarios_collection = factory.connector.get_usuarios_collection()
                if usuarios_collection is not None:
                    docs = usuarios_collection.where("email", "==", email).limit(1).stream()
                    existing_by_email = next(docs, None)

            if requested_role == "proveedor":
                # exige campos de negocio cuando el rol solicitado es proveedor
                company_name = (data.get("company_name") or "").strip()
                business_area = (data.get("business_area") or "").strip()
                card_number = (data.get("card_number") or "").strip()
                if not company_name or not business_area or not card_number:
                    raise HTTPException(status_code=400, detail="Missing provider fields")

            if existing_by_email is not None and existing_by_email.exists:
                existing_data = existing_by_email.to_dict() or {}
                role = existing_data.get("role") or requested_role
                user_data = {
                    "email": email,
                    "uid": uid,
                    "name": (data.get("name") or existing_data.get("name") or decoded_token.get("name") or "").strip(),
                    "role": role,
                    "address": (data.get("address") or existing_data.get("address") or "").strip(),
                    "postal_code": (data.get("postal_code") or existing_data.get("postal_code") or "").strip(),
                    "city": (data.get("city") or existing_data.get("city") or "").strip(),
                    "country": (data.get("country") or existing_data.get("country") or "").strip(),
                    "profile_image_url": (data.get("profile_image_url") or existing_data.get("profile_image_url") or decoded_token.get("picture") or "").strip(),
                    "company_name": (data.get("company_name") or existing_data.get("company_name") or "").strip(),
                    "business_area": (data.get("business_area") or existing_data.get("business_area") or "").strip(),
                    "card_number": (data.get("card_number") or existing_data.get("card_number") or "").strip(),
                    "created_at": existing_data.get("created_at", datetime.now().isoformat()),
                    "updated_at": datetime.now().isoformat()
                }
            else:
                user_data = {
                    "email": email,
                    "uid": uid,
                    "name": (data.get("name") or decoded_token.get("name") or "").strip(),
                    "role": requested_role,
                    "address": (data.get("address") or "").strip(),
                    "postal_code": (data.get("postal_code") or "").strip(),
                    "city": (data.get("city") or "").strip(),
                    "country": (data.get("country") or "").strip(),
                    "profile_image_url": (data.get("profile_image_url") or decoded_token.get("picture") or "").strip(),
                    "company_name": (data.get("company_name") or "").strip(),
                    "business_area": (data.get("business_area") or "").strip(),
                    "card_number": (data.get("card_number") or "").strip(),
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }

            mymodel.create_usuario(uid, user_data)
            user = mymodel.get_usuario(uid)

        if user and not user.is_Empty():
            user_json = user.user_to_dict()
            # registra sesion en memoria y setea cookie http only
            sessions[uid] = user_json

            response = JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": SUCCESS_MESSAGES["login_success"],
                    "user": user_json,
                    "sessionToken": uid
                }
            )
            response.set_cookie(key="session", value=uid, httponly=True)
            return response

        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])
    except HTTPException:
        raise
    except Exception as e:
        print(f"Google register error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])


@app.get("/api/auth/check_email")
async def check_email(email: Optional[str] = None):
    """Comprueba si ya existe un usuario con el email dado"""
    try:
        if not email:
            raise HTTPException(status_code=400, detail="Email required")

        try:
            auth.get_user_by_email(email)
            return JSONResponse(status_code=200, content={"status": "success", "exists": True})
        except auth.UserNotFoundError:
            return JSONResponse(status_code=200, content={"status": "success", "exists": False})
    except HTTPException:
        raise
    except Exception as e:
        print(f"Check email error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.post("/api/auth/logout")
async def logout(request: Request):
    """Logout del usuario"""
    try:
        # elimina sesion local si existe para invalidar acceso inmediato
        cookie = request.cookies.get("session")
        if cookie and cookie in sessions:
            del sessions[cookie]
        
        response = JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Logout exitoso"}
        )
        response.delete_cookie("session")
        return response
    except Exception as e:
        print(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])


@app.post("/api/auth/login-basic")
async def login_basic(data: dict = Body(...)):
    """Fallback de login por email/password para cuentas demo cuando Firebase Auth falla"""
    try:
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not email or not password:
            raise HTTPException(status_code=400, detail="Missing email or password")

        expected_password = DEMO_LOGIN_CREDENTIALS.get(email)
        # compara contra credenciales demo para fallback controlado
        if not expected_password or expected_password != password:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        factory = mymodel.factory
        if not isinstance(factory, FirebaseDAOFactory):
            raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

        usuarios_collection = factory.connector.get_usuarios_collection()
        if usuarios_collection is None:
            raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

        docs = usuarios_collection.where("email", "==", email).limit(1).stream()
        user_doc = next(docs, None)
        if user_doc is None or not user_doc.exists:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en Firestore")

        user_json = user_doc.to_dict() or {}
        if not user_json.get("uid"):
            user_json["uid"] = user_doc.id

        uid = user_json["uid"]
        # guarda sesion y retorna token simple basado en uid
        sessions[uid] = user_json

        response = JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": SUCCESS_MESSAGES["login_success"],
                "user": user_json,
                "sessionToken": uid,
                "auth_mode": "fallback"
            }
        )
        response.set_cookie(key="session", value=uid, httponly=True)
        return response
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login basic error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

# perfil de usuario

@app.get("/api/user/profile")
async def get_user_profile(request: Request):
    """Obtener perfil del usuario autenticado"""
    try:
        # verifica sesion activa por cookie o bearer token
        session_user = verify_session(request)
        if not session_user:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])

        uid = session_user.get("uid")
        fresh_user = mymodel.get_usuario(uid) if uid else None
        if fresh_user and not fresh_user.is_Empty():
            # refresca sesion en memoria con datos actuales de base de datos
            user_data = fresh_user.user_to_dict()
            sessions[uid] = user_data
        else:
            user_data = session_user
        
        return JSONResponse(
            status_code=200,
            content={"status": "success", "user": user_data}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get profile error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])


def _extract_profile_credentials(data: dict, user_data: dict):
    # extrae y valida email y contrasenas asociadas al cambio de perfil
    current_email = (user_data.get("email") or "").strip().lower()
    new_email = (data.get("email", current_email) or "").strip().lower()
    raw_password = data.get("password")
    raw_confirm_password = data.get("confirm_password")
    raw_old_password = data.get("old_password")

    new_password = str(raw_password or "").strip()
    confirm_password = str(raw_confirm_password or "").strip()
    old_password = str(raw_old_password or "").strip()
    password_update_requested = raw_password is not None and str(raw_password) != ""

    if password_update_requested and len(new_password) < 6:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_password"])

    if password_update_requested and new_password != confirm_password:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["passwords_not_match"])

    if password_update_requested and not old_password:
        raise HTTPException(status_code=400, detail="Debes introducir tu contraseña actual para cambiarla")

    if password_update_requested:
        expected_demo_password = DEMO_LOGIN_CREDENTIALS.get(current_email)
        if expected_demo_password is not None and old_password != expected_demo_password:
            raise HTTPException(status_code=400, detail="La contraseña actual no es correcta")

    return current_email, new_email, new_password


def _sync_user_auth(uid: str, current_email: str, new_email: str, new_password: str):
    # sincroniza cambios de email y contrasena en firebase authentication
    auth_update_payload = {}

    if new_email and new_email != current_email:
        auth_update_payload["email"] = new_email
    if new_password:
        auth_update_payload["password"] = new_password

    if not auth_update_payload:
        return

    try:
        auth.update_user(uid, **auth_update_payload)
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["email_already_registered"])


def _build_profile_update_data(data: dict, user_data: dict, new_email: str):
    # construye payload final de perfil conservando valores anteriores cuando no llegan nuevos
    def _as_text(value, fallback: str = "") -> str:
        if value is None:
            return fallback
        text = str(value).strip()
        return text or fallback

    def _pick_non_empty(field_name: str, fallback_value: str = ""):
        raw_value = data.get(field_name, None)
        if raw_value is None:
            return fallback_value

        normalized = str(raw_value).strip()
        if not normalized:
            return fallback_value

        return normalized

    return {
        "name": _pick_non_empty("name", _as_text(user_data.get("name"))),
        "email": _as_text(new_email or user_data.get("email")),
        "address": _pick_non_empty("address", _as_text(user_data.get("address"))),
        "postal_code": _pick_non_empty("postal_code", _as_text(user_data.get("postal_code"))),
        "city": _pick_non_empty("city", _as_text(user_data.get("city"))),
        "country": _pick_non_empty("country", _as_text(user_data.get("country"))),
        "profile_image_url": _pick_non_empty("profile_image_url", _as_text(user_data.get("profile_image_url"))),
        "company_name": _pick_non_empty("company_name", _as_text(user_data.get("company_name"))),
        "business_area": _pick_non_empty("business_area", _as_text(user_data.get("business_area"))),
        "card_number": _pick_non_empty("card_number", _as_text(user_data.get("card_number"))),
        "updated_at": datetime.now().isoformat()
    }


def _safe_float(value, fallback=0.0):
    # convierte a float sin romper flujo si el valor no es valido
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _safe_int(value, fallback=0):
    # convierte a int con valor por defecto ante errores de parseo
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _parse_order_datetime(raw_value):
    # parsea fecha iso de pedido y soporta sufijo z de utc
    if not raw_value:
        return None
    try:
        text = str(raw_value)
        if text.endswith("Z"):
            text = text.replace("Z", "+00:00")
        return datetime.fromisoformat(text)
    except Exception:
        return None


def _format_order_datetime(raw_value):
    # genera etiqueta legible para mostrar fecha en listados
    parsed = _parse_order_datetime(raw_value)
    if not parsed:
        return "Fecha no disponible"
    return parsed.strftime("%d/%m/%Y %H:%M")


def _build_provider_product_maps(products):
    # construye indices auxiliares para relacionar item con proveedor
    provider_by_id = {}
    provider_by_name = {}

    for product in products:
        product_id = str(product.get("id", "")).strip()
        provider_name = str(product.get("provider", "")).strip().lower()
        product_name = str(product.get("name", "")).strip().lower()

        if product_id and provider_name:
            provider_by_id[product_id] = provider_name
        if product_name and provider_name:
            provider_by_name[product_name] = provider_name

    return provider_by_id, provider_by_name


def _matches_provider_item(item, provider_targets, provider_by_id, provider_by_name):
    # determina si un item vendido pertenece al proveedor autenticado
    direct_provider = str(item.get("provider") or item.get("company_name") or "").strip().lower()
    if direct_provider and direct_provider in provider_targets:
        return True

    product_id = str(item.get("product_id") or item.get("id") or "").strip()
    if product_id:
        mapped = provider_by_id.get(product_id)
        if mapped and mapped in provider_targets:
            return True

    product_name = str(item.get("name") or item.get("product_name") or "").strip().lower()
    if product_name:
        mapped = provider_by_name.get(product_name)
        if mapped and mapped in provider_targets:
            return True

    return False


def _is_ticket_item(item):
    # detecta si un item corresponde a entradas de evento
    text_type = str(item.get("type") or item.get("category") or "").strip().lower()
    text_name = str(item.get("name") or item.get("product_name") or "").strip().lower()
    return "ticket" in text_type or "entrada" in text_type or "entrada" in text_name


def _extract_ticket_event_name(item):
    # intenta obtener el nombre del evento asociado a una entrada
    direct_name = str(item.get("event_name") or item.get("event") or item.get("festival") or "").strip()
    if direct_name:
        return direct_name

    item_name = str(item.get("name") or item.get("product_name") or "").strip()
    if not item_name:
        return ""

    normalized = item_name
    for prefix in ["entrada:", "entrada vip:", "entrada general:"]:
        if normalized.lower().startswith(prefix):
            normalized = normalized[len(prefix):].strip()
            break

    return normalized


def _normalize_event_name(value):
    return str(value or "").strip().lower()


def _match_event_id_by_ticket_name(ticket_event_name, events):
    # relaciona nombre de entrada con id de evento mediante coincidencia exacta o parcial
    ticket_name_normalized = _normalize_event_name(ticket_event_name)
    if not ticket_name_normalized:
        return ""

    for event in events:
        event_id = str(event.get("id") or "").strip()
        event_name = _normalize_event_name(event.get("name") or event.get("title"))
        if not event_id or not event_name:
            continue

        if ticket_name_normalized == event_name:
            return event_id

    for event in events:
        event_id = str(event.get("id") or "").strip()
        event_name = _normalize_event_name(event.get("name") or event.get("title"))
        if not event_id or not event_name:
            continue

        if ticket_name_normalized in event_name or event_name in ticket_name_normalized:
            return event_id

    return ""


def _get_manager_user_stats() -> Tuple[int, int]:
    # calcula usuarios totales y proveedores activos para panel de gestor
    users_collection = mymodel.factory.connector.get_usuarios_collection() # type: ignore
    if users_collection is None:
        return 0, 0

    total_users = 0
    active_providers = 0
    for user_doc in users_collection.stream():
        total_users += 1
        role = str((user_doc.to_dict() or {}).get("role") or "").strip().lower()
        if role == "proveedor":
            active_providers += 1

    return total_users, active_providers


@app.get("/api/manager/dashboard")
async def get_manager_dashboard(request: Request):
    """Obtener resumen real para el perfil del gestor."""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])

        if user_data.get("role") != "gestor":
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        all_events = json.loads(mymodel.get_all_eventos())
        if not isinstance(all_events, list):
            all_events = []

        all_orders = json.loads(mymodel.get_all_pedidos())
        if not isinstance(all_orders, list):
            all_orders = []

        event_ticket_units = {}
        event_ticket_revenue = {}
        total_ticket_units = 0
        total_ticket_revenue = 0.0
        monthly_ticket_revenue = 0.0
        now = datetime.now()

        for order in all_orders:
            # ignora pedidos cancelados para no inflar metricas
            status_lower = str(order.get("status") or "").strip().lower()
            if status_lower == "cancelada":
                continue

            order_date = _parse_order_datetime(order.get("created_at"))
            is_current_month = bool(order_date and order_date.month == now.month and order_date.year == now.year)

            items = order.get("items")
            if not isinstance(items, list):
                continue

            for item in items:
                # solo computa items que sean entradas de eventos
                if not isinstance(item, dict) or not _is_ticket_item(item):
                    continue

                quantity = max(1, _safe_int(item.get("quantity") or item.get("qty") or 1, 1))
                unit_price = _safe_float(item.get("price") or 0, 0.0)
                line_total = unit_price * quantity

                total_ticket_units += quantity
                total_ticket_revenue += line_total
                if is_current_month:
                    monthly_ticket_revenue += line_total

                direct_event_id = str(item.get("event_id") or "").strip()
                event_id = direct_event_id or _match_event_id_by_ticket_name(_extract_ticket_event_name(item), all_events)
                if not event_id:
                    continue

                event_ticket_units[event_id] = event_ticket_units.get(event_id, 0) + quantity
                event_ticket_revenue[event_id] = event_ticket_revenue.get(event_id, 0.0) + line_total

        festivals = []
        for event in all_events:
            # arma vista resumida por festival para el dashboard del gestor
            event_id = str(event.get("id") or "").strip()
            event_name = str(event.get("name") or event.get("title") or "Festival sin nombre").strip() or "Festival sin nombre"
            location = str(event.get("location") or event.get("loc") or "Ubicación no disponible").strip() or "Ubicación no disponible"
            date_text = str(event.get("date") or event.get("start_date") or "Fecha no disponible").strip() or "Fecha no disponible"
            status_text = str(event.get("status") or "publicado").strip() or "publicado"

            festivals.append({
                "id": event_id,
                "name": event_name,
                "location": location,
                "date": date_text,
                "status": status_text,
                "tickets_sold": int(event_ticket_units.get(event_id, 0)),
                "ticket_revenue": round(float(event_ticket_revenue.get(event_id, 0.0)), 2),
            })

        festivals.sort(key=lambda festival: festival.get("tickets_sold", 0), reverse=True)

        total_users, active_providers = _get_manager_user_stats()
        summary = {
            "total_users": int(total_users),
            "active_providers": int(active_providers),
            "total_festivals": len(festivals),
            "total_tickets_sold": int(total_ticket_units),
            "total_revenue": round(float(total_ticket_revenue), 2),
            "monthly_revenue": round(float(monthly_ticket_revenue), 2),
        }

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "festivals": festivals,
                    "summary": summary,
                }
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get manager dashboard error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])


@app.get("/api/provider/sales")
async def get_provider_sales(request: Request):
    """Obtener ventas de productos del proveedor autenticado."""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])

        if user_data.get("role") != "proveedor":
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        provider_uid = str(user_data.get("uid", "")).strip()
        provider_targets = {
            str(user_data.get("company_name") or "").strip().lower(),
            str(user_data.get("name") or "").strip().lower(),
        }
        provider_targets.discard("")

        all_products = json.loads(mymodel.get_all_productos())
        if not isinstance(all_products, list):
            all_products = []
        provider_by_id, provider_by_name = _build_provider_product_maps(all_products)

        all_orders = json.loads(mymodel.get_all_pedidos())
        if not isinstance(all_orders, list):
            all_orders = []

        operations = []
        total_revenue = 0.0
        today_revenue = 0.0
        units_sold = 0
        product_units = {}
        today_date = datetime.now().date()

        for order in all_orders:
            # evita contar compras del propio proveedor como venta propia
            order_uid = str(order.get("uid", "")).strip()
            if provider_uid and order_uid == provider_uid:
                continue

            status_text = str(order.get("status") or "pendiente").strip()
            status_lower = status_text.lower()
            if status_lower == "cancelada":
                continue

            created_at = order.get("created_at")
            parsed_date = _parse_order_datetime(created_at)
            date_label = _format_order_datetime(created_at)

            items = order.get("items")
            if not isinstance(items, list):
                items = []

            for item in items:
                # solo toma items que correspondan a productos del proveedor
                if not isinstance(item, dict):
                    continue

                if not _matches_provider_item(item, provider_targets, provider_by_id, provider_by_name):
                    continue

                quantity = _safe_int(item.get("quantity") or item.get("qty") or 1, 1)
                unit_price = _safe_float(item.get("price") or 0, 0.0)
                line_total = unit_price * max(1, quantity)

                product_name = str(item.get("name") or item.get("product_name") or "Producto").strip() or "Producto"
                order_id = str(order.get("id") or order.get("order_id") or "").strip()
                if not order_id:
                    order_id = f"ORD-{len(operations) + 1}"

                operations.append({
                    "id": order_id,
                    "item": product_name,
                    "type": "Venta Producto",
                    "date": date_label,
                    "created_at": str(created_at or ""),
                    "amount": round(line_total, 2),
                    "status": status_text,
                    "canCancel": False,
                    "quantity": max(1, quantity),
                })

                total_revenue += line_total
                units_sold += max(1, quantity)
                product_units[product_name] = product_units.get(product_name, 0) + max(1, quantity)

                if parsed_date and parsed_date.date() == today_date:
                    today_revenue += line_total

        operations.sort(
            key=lambda op: (_parse_order_datetime(op.get("created_at")) or datetime.min),
            reverse=True
        )

        top_product = "Ninguno"
        if product_units:
            top_product = max(product_units.items(), key=lambda item: item[1])[0]

        summary = {
            "total_balance": round(total_revenue, 2),
            "sales_today": round(today_revenue, 2),
            "units_sold": units_sold,
            "top_product": top_product,
        }

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": {
                    "operations": operations,
                    "summary": summary,
                }
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get provider sales error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.put("/api/user/profile")
async def update_user_profile(request: Request, data: dict = Body(...)):
    """Actualizar perfil del usuario"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])
        
        uid = user_data.get("uid")
        if not uid:
            raise HTTPException(status_code=400, detail="UID no encontrado en sesión")

        current_email, new_email, new_password = _extract_profile_credentials(data, user_data)
        # sincroniza credenciales auth y actualiza documento de perfil
        _sync_user_auth(uid, current_email, new_email, new_password)
        update_data = _build_profile_update_data(data, user_data, new_email)
        
        mymodel.update_usuario(uid, update_data)
        updated_user = mymodel.get_usuario(uid)
        
        if updated_user:
            user_dict = updated_user.user_to_dict()
            sessions[uid] = user_dict
            
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": SUCCESS_MESSAGES["profile_updated"],
                    "user": user_dict
                }
            )

            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])

    except HTTPException:
        raise
    except Exception as e:
        print(f"Update profile error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

# productos

@app.get("/api/products")
async def get_all_products():
    """Obtener todos los productos"""
    try:
        productos = mymodel.get_all_productos()
        # devuelve catalogo completo en la clave data
        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": json.loads(productos)}
        )
    except Exception as e:
        print(f"Get products error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    """Obtener un producto específico"""
    try:
        producto = mymodel.get_producto_by_id(product_id)
        producto_dict = json.loads(producto)
        
        if not producto_dict:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])
        
        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": producto_dict}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get product error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.post("/api/products")
async def create_product(request: Request, data: dict = Body(...)):
    """Crear nuevo producto (gestor y proveedor)"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])
        
        role = str(user_data.get("role") or "").strip().lower()
        if role not in {"gestor", "proveedor"}:
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        product_data = dict(data or {})

        # Para proveedor, persiste metadatos de propietario desde sesión autenticada.
        if role == "proveedor":
            provider_uid = str(user_data.get("uid") or "").strip()
            provider_name = str(
                user_data.get("company_name") or user_data.get("name") or user_data.get("email") or ""
            ).strip()
            provider_email = str(user_data.get("email") or "").strip()

            if provider_uid:
                product_data["provider_uid"] = provider_uid
                product_data["owner_uid"] = provider_uid
                product_data["uid"] = provider_uid
            if provider_name:
                product_data["provider"] = provider_name
                product_data.setdefault("company_name", provider_name)
            if provider_email:
                product_data["owner_email"] = provider_email

        mymodel.create_producto(product_data)
        
        return JSONResponse(
            status_code=201,
            content={"status": "success", "message": "Producto creado exitosamente"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Create product error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

def _can_provider_manage_product(product: dict, user_data: dict) -> bool:
    provider_uid = str(user_data.get("uid") or "").strip().lower()
    provider_email = str(user_data.get("email") or "").strip().lower()
    provider_name = str(user_data.get("name") or "").strip().lower()
    provider_company = str(user_data.get("company_name") or "").strip().lower()

    product_candidates = {
        str(product.get("provider_uid") or "").strip().lower(),
        str(product.get("owner_uid") or "").strip().lower(),
        str(product.get("uid") or "").strip().lower(),
        str(product.get("owner_email") or "").strip().lower(),
        str(product.get("provider") or "").strip().lower(),
        str(product.get("company_name") or "").strip().lower(),
    }

    if provider_uid and provider_uid in product_candidates:
        return True
    if provider_email and provider_email in product_candidates:
        return True
    if provider_name and provider_name in product_candidates:
        return True
    if provider_company and provider_company in product_candidates:
        return True
    return False

@app.put("/api/products/{product_id}")
async def update_product(request: Request, product_id: str, data: dict = Body(...)):
    """Actualizar producto (gestor o proveedor propietario)"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])

        role = str(user_data.get("role") or "").strip().lower()
        if role not in {"gestor", "proveedor"}:
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        existing_product_json = mymodel.get_producto_by_id(product_id)
        existing_product = json.loads(existing_product_json)
        if not existing_product:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])

        if role == "proveedor" and not _can_provider_manage_product(existing_product, user_data):
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        update_data = dict(data or {})

        # Blindaje de ownership cuando actualiza un proveedor.
        if role == "proveedor":
            provider_uid = str(user_data.get("uid") or "").strip()
            provider_name = str(
                user_data.get("company_name") or user_data.get("name") or user_data.get("email") or ""
            ).strip()
            provider_email = str(user_data.get("email") or "").strip()

            if provider_uid:
                update_data["provider_uid"] = provider_uid
                update_data["owner_uid"] = provider_uid
                update_data["uid"] = provider_uid
            if provider_name:
                update_data["provider"] = provider_name
                update_data["company_name"] = provider_name
            if provider_email:
                update_data["owner_email"] = provider_email

        success = mymodel.update_producto(product_id, update_data)
        if not success:
            raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Producto actualizado exitosamente"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update product error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.delete("/api/products/{product_id}")
async def delete_product(request: Request, product_id: str):
    """Eliminar producto (gestor o proveedor propietario)"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])

        role = str(user_data.get("role") or "").strip().lower()
        if role not in {"gestor", "proveedor"}:
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        existing_product_json = mymodel.get_producto_by_id(product_id)
        existing_product = json.loads(existing_product_json)
        if not existing_product:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])

        if role == "proveedor" and not _can_provider_manage_product(existing_product, user_data):
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        success = mymodel.delete_producto(product_id)
        if not success:
            raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Producto eliminado exitosamente"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete product error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

# pedidos

@app.get("/api/orders")
async def get_user_orders(request: Request):
    """Obtener pedidos del usuario autenticado"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])
        
        uid = user_data.get("uid")
        # consulta historial de pedidos del usuario autenticado
        pedidos = mymodel.get_pedidos_by_uid(uid)
        
        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": json.loads(pedidos)}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get orders error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.get("/api/orders/{order_id}")
async def get_order(request: Request, order_id: str):
    """Obtener un pedido específico"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])
        
        pedido = mymodel.get_pedido_by_id(order_id)
        pedido_dict = json.loads(pedido)
        
        if not pedido_dict:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])
        
        if pedido_dict.get("uid") != user_data.get("uid"):
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])
        
        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": pedido_dict}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get order error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.post("/api/orders")
async def create_order(request: Request, data: dict = Body(...)):
    """Crear nuevo pedido"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])
        
        order_data = {
            # relaciona pedido con usuario autenticado y datos de compra
            "uid": user_data.get("uid"),
            "items": data.get("items", []),
            "total_price": data.get("total_price", 0),
            "status": "pendiente",
            "payment_method": data.get("payment_method", ""),
            "delivery_address": data.get("delivery_address", "")
        }
        
        mymodel.create_pedido(order_data)
        
        return JSONResponse(
            status_code=201,
            content={"status": "success", "message": SUCCESS_MESSAGES["order_created"]}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Create order error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.put("/api/orders/{order_id}")
async def update_order(request: Request, order_id: str, data: dict = Body(...)):
    """Actualizar un pedido"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])
        
        pedido = mymodel.get_pedido_by_id(order_id)
        pedido_dict = json.loads(pedido)
        
        if not pedido_dict:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])
        
        if pedido_dict.get("uid") != user_data.get("uid"):
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])
        
        mymodel.update_pedido(order_id, data)
        
        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": SUCCESS_MESSAGES["order_updated"]}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update order error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

# eventos

@app.get("/api/events")
async def get_all_events():
    """Obtener todos los eventos"""
    try:
        eventos = mymodel.get_all_eventos()
        # envia eventos en bruto para listados del frontend
        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": json.loads(eventos)}
        )
    except Exception as e:
        print(f"Get events error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.get("/api/events/search")
async def search_events(q: str = ""):
    """Buscar eventos por nombre, ubicación o descripción
    
    Parámetros:
    - q: término de búsqueda
    
    Ejemplo: /api/events/search?q=boombastic
    """
    try:
        eventos_data = mymodel.get_all_eventos()
        eventos = json.loads(eventos_data)
        
        # Convertir a lista si es necesario
        if isinstance(eventos, dict):
            eventos = [eventos]
        elif not isinstance(eventos, list):
            eventos = []
        
        # Filtrar por término de búsqueda (nombre, ubicación, descripción)
        filtered = eventos
        
        if q:
            # aplica filtro simple por texto en campos comunes del evento
            q_lower = q.lower()
            filtered = [
                event for event in filtered
                if q_lower in str(event.get("name", "")).lower()
                or q_lower in str(event.get("title", "")).lower()
                or q_lower in str(event.get("location", "")).lower()
                or q_lower in str(event.get("loc", "")).lower()
                or q_lower in str(event.get("description", "")).lower()
                or q_lower in str(event.get("artist", "")).lower()
            ]
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "query": q,
                "total": len(filtered),
                "data": filtered
            }
        )
    except Exception as e:
        print(f"Search events error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.get("/api/events/{event_id}")
async def get_event(event_id: str):
    """Obtener un evento específico"""
    try:
        evento = mymodel.get_evento_by_id(event_id)
        evento_dict = json.loads(evento)
        
        if not evento_dict:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])
        
        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": evento_dict}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get event error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.post("/api/events")
async def create_event(request: Request, data: dict = Body(...)):
    """Crear nuevo evento (solo gestor)"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])
        
        if user_data.get("role") != "gestor":
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])
        
        mymodel.create_evento(data)
        
        return JSONResponse(
            status_code=201,
            content={"status": "success", "message": "Evento creado exitosamente"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Create event error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.put("/api/events/{event_id}")
async def update_event(request: Request, event_id: str, data: dict = Body(...)):
    """Actualizar evento (solo gestor)"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])

        if user_data.get("role") != "gestor":
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        evento = mymodel.get_evento_by_id(event_id)
        evento_dict = json.loads(evento)
        if not evento_dict:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])

        # imprime trazas de depuracion para revisar payload de actualizacion
        print(f"\n=== UPDATE EVENT DEBUG ===")
        print(f"Event ID: {event_id}")
        print(f"Received data keys: {list(data.keys())}")
        if "lineup" in data:
            print(f"Lineup data: {data['lineup']}")
        print(f"===========================\n")

        mymodel.update_evento(event_id, data)

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Evento actualizado exitosamente"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update event error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.delete("/api/events/{event_id}")
async def delete_event(request: Request, event_id: str):
    """Eliminar evento (solo gestor)"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])

        if user_data.get("role") != "gestor":
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        evento = mymodel.get_evento_by_id(event_id)
        evento_dict = json.loads(evento)
        if not evento_dict:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])

        mymodel.delete_evento(event_id)

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Evento eliminado exitosamente"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete event error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

# artistas

@app.get("/api/artists")
async def get_all_artists():
    """Obtener todos los artistas"""
    try:
        artistas = mymodel.get_all_artistas()
        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": json.loads(artistas)}
        )
    except Exception as e:
        print(f"Get artists error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.get("/api/artists/search")
async def search_artists(q: str = "", genre: str = ""):
    """Buscar artistas por nombre o género
    
    Parámetros:
    - q: término de búsqueda (nombre del artista)
    - genre: filtrar por género
    
    Ejemplo: /api/artists/search?q=charlotte&genre=electronic
    """
    try:
        artistas_data = mymodel.get_all_artistas()
        artistas = json.loads(artistas_data)
        
        # Convertir a lista si es necesario
        if isinstance(artistas, dict):
            artistas = [artistas]
        elif not isinstance(artistas, list):
            artistas = []
        
        # Filtrar por término de búsqueda (nombre, género, país)
        filtered = artistas
        
        if q:
            # filtra por nombre, genero, pais o bio
            q_lower = q.lower()
            filtered = [
                artist for artist in filtered
                if q_lower in str(artist.get("name", "")).lower()
                or q_lower in str(artist.get("genre", "")).lower()
                or q_lower in str(artist.get("country", "")).lower()
                or q_lower in str(artist.get("bio", "")).lower()
            ]
        
        # Filtrar por género si se especifica
        if genre:
            # aplica filtro adicional por genero
            genre_lower = genre.lower()
            filtered = [
                artist for artist in filtered
                if genre_lower in str(artist.get("genre", "")).lower()
            ]
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "query": q,
                "genre_filter": genre,
                "total": len(filtered),
                "data": filtered
            }
        )
    except Exception as e:
        print(f"Search artists error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.get("/api/artists/{slug}")
async def get_artist_by_slug(slug: str):
    """Obtener un artista por slug"""
    try:
        artista = mymodel.get_artista_by_slug(slug)
        artista_dict = json.loads(artista)

        if not artista_dict:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])

        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": artista_dict}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get artist error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.post("/api/artists")
async def create_artist(request: Request, data: dict = Body(...)):
    """Crear nuevo artista (solo gestor)"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])
        
        if user_data.get("role") != "gestor":
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])
        
        mymodel.create_artista(data)
        
        return JSONResponse(
            status_code=201,
            content={"status": "success", "message": "Artista creado exitosamente"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Create artist error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.put("/api/artists/{artist_id}")
async def update_artist(request: Request, artist_id: str, data: dict = Body(...)):
    """Actualizar artista (solo gestor)"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])

        if user_data.get("role") != "gestor":
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        artista = mymodel.get_artista_by_id(artist_id)
        artista_dict = json.loads(artista)
        if not artista_dict:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])

        mymodel.update_artista(artist_id, data)

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Artista actualizado exitosamente"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update artist error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

@app.delete("/api/artists/{artist_id}")
async def delete_artist(request: Request, artist_id: str):
    """Eliminar artista (solo gestor)"""
    try:
        user_data = verify_session(request)
        if not user_data:
            raise HTTPException(status_code=401, detail=ERROR_MESSAGES["unauthorized"])

        if user_data.get("role") != "gestor":
            raise HTTPException(status_code=403, detail=ERROR_MESSAGES["forbidden"])

        artista = mymodel.get_artista_by_id(artist_id)
        artista_dict = json.loads(artista)
        if not artista_dict:
            raise HTTPException(status_code=404, detail=ERROR_MESSAGES["not_found"])

        mymodel.delete_artista(artist_id)

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Artista eliminado exitosamente"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete artist error: {e}")
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["server_error"])

# health check

@app.get("/api/health")
async def health_check():
    """Health check del servidor"""
    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": "Servidor funcionando correctamente"}
    )


# ---------------------------------------------------------------------------
# Routers incrementales (TK-001-1)
# ---------------------------------------------------------------------------
from controller.extra_routes import include_extra_routes  # noqa: E402

include_extra_routes(app)
