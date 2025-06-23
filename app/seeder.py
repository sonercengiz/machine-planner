from datetime import datetime
from app.db.session import SessionLocal
from app.models.user import User

def run_seed():
    db = SessionLocal()

    email = 'soner.cengiz@outlook.com'
    existing = db.query(User).filter_by(email=email).first()

    if existing:
        print(f"⚠ Kullanıcı zaten mevcut: {email}")
    else:
        admin = User(
            email=email,
            username='sonercengiz',
            full_name='Soner Cengiz',
            hashed_password='$2b$12$2m7HAJvrZfEv5HHVaOWrMOe4vp2rufxrIXtLiL8TqzQVDYlGrkzAC',
            is_active=True,
            is_superuser=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(admin)
        db.commit()
        print(f"✅ Superuser eklendi: {email}")

    db.close()

if __name__ == '__main__':
    run_seed()
