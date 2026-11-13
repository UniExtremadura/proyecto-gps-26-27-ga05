from ....dao.firebase.firebaseConnector import FirebaseConnector
from ....dto.artistDTO import artistDTO
from typing import Any, Dict, List, Optional


class FirebaseArtistaDAO:
    def __init__(self, connector: FirebaseConnector) -> None:
        self.connector = connector

    def get_all_artistas(self) -> List[Any]:
        return [artistDTO().set_data(item) for item in self.connector.get_all_artistas()]

    def get_artista_by_id(self, artist_id: str) -> Optional[Any]:
        doc = self.connector.get_artista_by_id(artist_id)
        if doc is None or not getattr(doc, "exists", False):
            return None
        data = doc.to_dict() or {}
        data["id"] = data.get("id") or doc.id
        data["slug"] = data.get("slug") or doc.id
        return artistDTO().set_data(data)

    def get_artista_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        return self.connector.get_artista_by_slug(slug)

    def create_artista(self, artist_data: Dict[str, Any]) -> bool:
        return bool(self.connector.create_artista(artist_data))

    def update_artista(self, artist_id: str, artist_data: Dict[str, Any]) -> bool:
        return self.connector.update_artista(artist_id, artist_data)

    def delete_artista(self, artist_id: str) -> bool:
        return self.connector.delete_artista(artist_id)
