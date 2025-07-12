from app import app, db
import models  # モデルをインポートしておくことが重要！

with app.app_context():
    db.create_all()
    print("✅ care_service.db を作成しました！")
