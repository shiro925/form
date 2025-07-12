from app import db
from datetime import datetime


# models.py
from werkzeug.security import generate_password_hash, check_password_hash

class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)






class CareServiceRequest(db.Model):
    __tablename__ = 'care_service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    
    # 紹介情報
    referrer_name = db.Column(db.String(100), nullable=True)
    referrer_contact = db.Column(db.String(100), nullable=True)
    
    # 介護状況
    care_level = db.Column(db.String(20), nullable=True)
    support_level = db.Column(db.String(20), nullable=True)
    
    # 希望サービス
    service_type = db.Column(db.String(20), nullable=False)
    other_service = db.Column(db.String(200), nullable=True)
    
    # 生活支援の詳細
    toilet_assistance = db.Column(db.String(20), nullable=True)
    meal_assistance = db.Column(db.String(20), nullable=True)
    walking_assistance = db.Column(db.String(20), nullable=True)
    
    # 受診同行の詳細（服薬情報）
    has_medication = db.Column(db.String(10), nullable=True)
    medication_details = db.Column(db.Text, nullable=True)
    
    # 希望日時
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.String(10), nullable=False)
    
    # 健康情報
    medical_history = db.Column(db.Text, nullable=True)
    special_notes = db.Column(db.Text, nullable=True)
    
    # システム情報
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CareServiceRequest {self.id}: {self.name}>'