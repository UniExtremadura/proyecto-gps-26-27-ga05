# Autenticación OAuth 2.0

Documentación de la integración OAuth de Subsonic Festival (TK-004-4).

## Proveedores soportados

| Proveedor | Uso | Configuración |
| --- | --- | --- |
| Google | Login/registro con cuenta de Google | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` |
| Apple | Login/registro con Apple ID | `APPLE_CLIENT_ID`, `APPLE_TEAM_ID`, `APPLE_KEY_ID`, `APPLE_PRIVATE_KEY`, `APPLE_REDIRECT_URI` |

Las variables se declaran en `backend/.env.example` y se cargan desde `backend/src/config/oauth.py`.

## Arquitectura

1. El frontend (`frontend/js/oauth.js`) inicia el flujo con Google o Apple.
2. El proveedor devuelve un `id_token` / `identity_token`.
3. El frontend lo envía a `POST /api/oauth/google/callback` o `POST /api/oauth/apple/callback`.
4. El backend valida el token externo (`backend/src/security/oauth.py`) y emite un JWT propio.
5. El JWT se guarda en `localStorage.sessionToken` y se envía como `Authorization: Bearer ...`.

## Endpoints

- `GET /api/oauth/providers`: proveedores configurados.
- `GET /api/oauth/{provider}/start`: URL de autorización.
- `POST /api/oauth/google/callback`: callback de Google.
- `POST /api/oauth/apple/callback`: callback de Apple (simulado en desarrollo).

## Desarrollo local

Sin credenciales reales se puede probar el flujo demo:

1. Abrir `#login` y pulsar el botón de Apple.
2. La SPA navega a `#oauth-callback?provider=apple&demo=1`.
3. El backend emite un JWT para `apple.demo@subsonicfest.com`.

## Seguridad

- Los tokens externos se validan en el servidor; nunca se confía solo en el frontend.
- El `state` de OAuth debe firmarse con `OAUTH_STATE_SECRET` en producción.
- Los JWT propios expiran a las 24 horas y pueden revocarse en el logout.
