import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

def send_form_data_email(form_data, recipient_email="testtest09250529@gmail.com"):
    """
    フォームデータをSMTP経由で送信する
    """

    # --- 環境変数などから送信設定を取得（環境に応じて変更） ---
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')  # 例: smtp.gmail.com
    smtp_port = int(os.environ.get('SMTP_PORT', 587))            # TLSなら587
    smtp_user = os.environ.get('SMTP_USER', 'testtest09250529@gmail.com')    # 送信元メールアドレス
    smtp_pass = os.environ.get('SMTP_PASSWORD', 'oxfptmmockaxtxly')  # SMTPパスワード（アプリパスワード）

    # --- メール件名・本文 ---
    subject = f"介護サービス申込 - {form_data['name']}様 ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    
    body = f"""
介護サービス申込フォームより、以下の内容で申込がありました。

==== 基本情報 ====
氏名: {form_data['name']}
性別: {form_data['gender']}
生年月日: {form_data['birthdate']}
電話番号: {form_data['phone']}
メールアドレス: {form_data.get('email', '未入力')}

==== 紹介情報 ====
紹介者: {form_data.get('referrer_name', '未入力')}
紹介者連絡先: {form_data.get('referrer_contact', '未入力')}

==== 介護状況 ====
要介護度: {form_data.get('care_level', '未入力')}
要支援度: {form_data.get('support_level', '未入力')}

==== 希望サービス ====
希望内容: {form_data['service_type']}
"""

    # --- サービスタイプに応じた追加情報 ---
    if form_data['service_type'] == '受診同行' and form_data.get('medication_data'):
        med = form_data['medication_data']
        body += f"""
---- 服薬情報 ----
服用中の薬: {med.get('has_medication', '未記入')}
薬の詳細: {med.get('medication_details', '未記入')}
"""
    elif form_data['service_type'] == '生活支援' and form_data.get('assistance_data'):
        assist = form_data['assistance_data']
        body += f"""
---- 介助情報 ----
トイレ介助: {assist.get('toilet_assistance', '未選択')}
食事介助: {assist.get('meal_assistance', '未選択')}
歩行介助: {assist.get('walking_assistance', '未選択')}
"""
    elif form_data['service_type'] == 'その他':
        body += f"""
---- その他の希望内容 ----
{form_data.get('other_service', '未記入')}
"""

    body += f"""
==== 希望日時 ====
希望日: {form_data['preferred_date']}
希望時間: {form_data['preferred_time']}

==== 健康情報 ====
既往歴: {form_data.get('medical_history', '未入力')}
配慮事項: {form_data.get('special_notes', '未入力')}
"""

    # --- メールオブジェクトの作成 ---
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        # SMTPサーバーへ接続して送信
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print("SMTP設定:")
        print("HOST:", smtp_host)
        print("PORT:", smtp_port)
        print("USER:", smtp_user)
        print("PASS:", smtp_pass[:4] + "****")  # パスワードは一部だけ表示
        print("送信先:", recipient_email)
        print("メール送信成功")
        return True
    except Exception as e:
        print(f"メール送信エラー: {e}")
        return False
