from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, RadioField, SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired, Optional, Length, Email

class CareServiceForm(FlaskForm):
    """介護サービス利用のための情報収集フォーム"""
    
    # 基本情報
    name = StringField('お名前', validators=[DataRequired(message='お名前を入力してください')])
    
    gender = SelectField('性別', 
                        choices=[('', '選択してください'), ('male', '男性'), ('female', '女性'), ('other', 'その他')],
                        validators=[DataRequired(message='性別を選択してください')])
    
    birthdate = DateField('生年月日', format='%Y-%m-%d', 
                         validators=[DataRequired(message='生年月日を選択してください')])
    
    # 連絡先情報
    phone = StringField('電話番号', validators=[DataRequired(message='電話番号を入力してください')])
    
    email = StringField('メールアドレス', validators=[Optional(), Email(message='有効なメールアドレスを入力してください')])
    
    # 紹介情報
    referrer_name = StringField('紹介者のお名前', validators=[Optional()])
    
    referrer_contact = StringField('紹介者の連絡先', validators=[Optional()])
    
    # 介護状況
    care_level = SelectField('要介護度', 
                           choices=[
                               ('', '選択してください'),
                               ('none', '認定なし'),
                               ('level1', '要介護1'),
                               ('level2', '要介護2'),
                               ('level3', '要介護3'),
                               ('level4', '要介護4'),
                               ('level5', '要介護5')
                           ],
                           validators=[Optional()])
    
    support_level = SelectField('要支援度', 
                              choices=[
                                  ('', '選択してください'),
                                  ('none', '認定なし'),
                                  ('level1', '要支援1'),
                                  ('level2', '要支援2')
                              ],
                              validators=[Optional()])
    
    # 希望サービス
    service_type = RadioField('希望内容', 
                             choices=[
                                 ('medical', '受診同行'),
                                 ('daily', '生活支援'),
                                 ('other', 'その他')
                             ],
                             validators=[DataRequired(message='希望内容を選択してください')])
    
    other_service = StringField('その他の希望内容', validators=[Optional()])
    
    # 受診同行の詳細（服薬情報）
    has_medication = RadioField('現在服用している薬はありますか？',
                               choices=[
                                   ('yes', 'はい'),
                                   ('no', 'いいえ')
                               ],
                               validators=[Optional()])
    
    medication_details = TextAreaField('お薬の名前', validators=[Optional(), Length(max=500)])
    
    # 生活支援の詳細（介助レベル）
    toilet_assistance = SelectField('トイレの介助', 
                                 choices=[
                                     ('', '選択してください'),
                                     ('none', '介助なし'),
                                     ('partial', '一部介助'),
                                     ('full', '全介助')
                                 ],
                                 validators=[Optional()])
    
    meal_assistance = SelectField('食事の介助', 
                               choices=[
                                   ('', '選択してください'),
                                   ('none', '介助なし'),
                                   ('partial', '一部介助'),
                                   ('full', '全介助')
                               ],
                               validators=[Optional()])
    
    walking_assistance = SelectField('歩行の介助', 
                                  choices=[
                                      ('', '選択してください'),
                                      ('none', '介助なし'),
                                      ('partial', '一部介助'),
                                      ('full', '全介助')
                                  ],
                                  validators=[Optional()])
    
    # 希望日時
    preferred_date = DateField('希望日', format='%Y-%m-%d', 
                             validators=[DataRequired(message='希望日を選択してください')])
    
    preferred_time = SelectField('希望時間', 
                              choices=[
                                  ('', '選択してください'),
                                  ('9', '9:00'),
                                  ('10', '10:00'),
                                  ('11', '11:00'),
                                  ('12', '12:00'),
                                  ('13', '13:00'),
                                  ('14', '14:00'),
                                  ('15', '15:00'),
                                  ('16', '16:00'),
                                  ('17', '17:00'),
                                  ('18', '18:00'),
                                  ('19', '19:00')
                              ],
                              validators=[DataRequired(message='希望時間を選択してください')])
    
    # 健康情報
    medical_history = TextAreaField('既往歴', validators=[Optional(), Length(max=1000)])
    
    special_notes = TextAreaField('配慮してほしい事項', validators=[Optional(), Length(max=1000)])
    
    # 同意
    agreement = RadioField('個人情報の取り扱いに同意する', 
                          choices=[('agree', '同意する')],
                          validators=[DataRequired(message='個人情報の取り扱いに同意してください')])
    
    submit = SubmitField('確認画面へ')
