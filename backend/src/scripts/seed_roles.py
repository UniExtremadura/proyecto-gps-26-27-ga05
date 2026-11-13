"""Ejecuta la siembra de roles: python -m scripts.seed_roles."""
from model.dao.firebase.firebaseDAOFactory import FirebaseDAOFactory
from model.roles import seed_roles


def main() -> None:
    factory = FirebaseDAOFactory()
    total = seed_roles(factory.connector)
    print(f"Roles sembrados: {total}")


if __name__ == "__main__":
    main()
