import os
import io
import csv
import json
import datetime
from flask import render_template, request, redirect, url_for, session, flash, send_file
from app import app, db
from forms import CareServiceForm
from models import CareServiceRequest, AdminUser  # ← 追加
from utils import send_form_data_email
from werkzeug.security import generate_password_hash, check_password_hash

# ====================
# ユーザー入力・登録処理
# ====================

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CareServiceForm()
    if request.method == 'POST' and form.validate_on_submit():
        assistance_data = {}
        medication_data = {}

        if form.service_type.data == 'daily':
            assistance_data = {
                'toilet_assistance': dict(form.toilet_assistance.choices).get(form.toilet_assistance.data),
                'meal_assistance': dict(form.meal_assistance.choices).get(form.meal_assistance.data),
                'walking_assistance': dict(form.walking_assistance.choices).get(form.walking_assistance.data)
            }

        if form.service_type.data == 'medical':
            medication_data = {
                'has_medication': dict(form.has_medication.choices).get(form.has_medication.data) if form.has_medication.data else None,
                'medication_details': form.medication_details.data
            }

        session['form_data'] = {
            'name': form.name.data,
            'gender': dict(form.gender.choices).get(form.gender.data),
            'birthdate': form.birthdate.data.strftime('%Y年%m月%d日'),
            'phone': form.phone.data,
            'email': form.email.data,
            'referrer_name': form.referrer_name.data,
            'referrer_contact': form.referrer_contact.data,
            'care_level': dict(form.care_level.choices).get(form.care_level.data),
            'support_level': dict(form.support_level.choices).get(form.support_level.data),
            'service_type': dict(form.service_type.choices).get(form.service_type.data),
            'other_service': form.other_service.data,
            'preferred_date': form.preferred_date.data.strftime('%Y年%m月%d日'),
            'preferred_time': f"{form.preferred_time.data}:00" if form.preferred_time.data else '',
            'medical_history': form.medical_history.data,
            'special_notes': form.special_notes.data,
            'assistance_data': assistance_data,
            'medication_data': medication_data
        }
        return redirect(url_for('confirm'))

    return render_template('form.html', form=form)


@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    form_data = session.get('form_data')
    if not form_data:
        flash('フォームから情報を入力してください', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            service_request = CareServiceRequest(
                name=form_data['name'],
                gender=form_data['gender'],
                birthdate=datetime.datetime.strptime(form_data['birthdate'], '%Y年%m月%d日').date(),
                phone=form_data['phone'],
                email=form_data['email'],
                referrer_name=form_data['referrer_name'],
                referrer_contact=form_data['referrer_contact'],
                care_level=form_data['care_level'],
                support_level=form_data['support_level'],
                service_type=form_data['service_type'],
                other_service=form_data['other_service'],
                preferred_date=datetime.datetime.strptime(form_data['preferred_date'], '%Y年%m月%d日').date(),
                preferred_time=form_data['preferred_time'],
                medical_history=form_data['medical_history'],
                special_notes=form_data['special_notes']
            )
            if form_data['service_type'] == '生活支援':
                service_request.toilet_assistance = form_data['assistance_data'].get('toilet_assistance')
                service_request.meal_assistance = form_data['assistance_data'].get('meal_assistance')
                service_request.walking_assistance = form_data['assistance_data'].get('walking_assistance')
            if form_data['service_type'] == '受診同行':
                service_request.has_medication = form_data['medication_data'].get('has_medication')
                service_request.medication_details = form_data['medication_data'].get('medication_details')

            db.session.add(service_request)
            db.session.commit()
            session['saved_request_id'] = service_request.id
            flash('申込情報が保存されました', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"データベース保存エラー: {str(e)}")
            flash('申込情報の保存中にエラーが発生しました。', 'error')
        return redirect(url_for('complete'))

    return render_template('confirm.html', data=form_data)


@app.route('/complete')
def complete():
    form_data = session.get('form_data')
    if not form_data:
        flash('フォームから情報を入力してください', 'error')
        return redirect(url_for('index'))

    try:
        send_form_data_email(form_data, recipient_email="testtest09250529@gmail.com")
    except Exception as e:
        print(f"メール送信エラー: {str(e)}")

    return render_template('complete.html')


# ====================
# 管理者ログイン・管理ページ
# ====================

# ------------------------------
# 管理者アカウント 初期作成
# ------------------------------
@app.route('/admin/create', methods=['GET', 'POST'])
def create_admin():
    if AdminUser.query.first():
        flash("すでに管理者が登録されています", "warning")
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = AdminUser(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("管理者アカウントを作成しました", "success")
        return redirect(url_for('admin_login'))

    return render_template('create_admin.html')


# ------------------------------
# 管理者ログイン
# ------------------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = AdminUser.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['admin_logged_in'] = True
            session['admin_user'] = user.username
            flash('ログインしました', 'success')
            return redirect(url_for('admin_calendar'))
        flash('ログイン情報が正しくありません', 'danger')
    return render_template('admin_login.html')


# ------------------------------
# 管理者アカウントの編集
# ------------------------------
@app.route('/admin/edit', methods=['GET', 'POST'])
def edit_admin():
    if not session.get('admin_logged_in'):
        flash("管理者ログインが必要です", "warning")
        return redirect(url_for('admin_login'))

    user = AdminUser.query.first()

    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password = request.form.get('password')

        if new_username:
            user.username = new_username
        if new_password:
            user.set_password(new_password)

        db.session.commit()
        flash("管理者情報を更新しました", "success")
        return redirect(url_for('admin_calendar'))

    return render_template('edit_admin.html', user=user)


# ------------------------------
# ログアウト
# ------------------------------
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_user', None)
    flash("ログアウトしました", "info")
    return redirect(url_for('admin_login'))



@app.route('/admin')
@app.route('/admin/calendar')
def admin_calendar():
    if not session.get('admin_logged_in'):
        flash("管理者ログインが必要です", "warning")
        return redirect(url_for('admin_login'))

    requests = CareServiceRequest.query.order_by(CareServiceRequest.preferred_date).all()
    return render_template('admin_calendar.html', requests=requests)


@app.route('/admin/delete/<int:req_id>', methods=['POST'])
def admin_delete(req_id):
    if not session.get('admin_logged_in'):
        flash("管理者ログインが必要です", "warning")
        return redirect(url_for('admin_login'))

    request_data = CareServiceRequest.query.get(req_id)
    if not request_data:
        flash("該当の申込が見つかりませんでした", "danger")
        return redirect(url_for('admin_calendar'))

    try:
        db.session.delete(request_data)
        db.session.commit()
        flash("申込データを削除しました", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"削除中にエラーが発生しました: {str(e)}", "danger")

    return redirect(url_for('admin_calendar'))


# ====================
# CSVエクスポート（今後削除予定）
# ====================

@app.route('/export/csv')
def export_csv():
    try:
        requests = CareServiceRequest.query.all()
        if not requests:
            flash('エクスポートするデータがありません', 'warning')
            return redirect(url_for('index'))

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', '氏名', '性別', '生年月日', '電話番号', 'メールアドレス',
                         '紹介者名', '紹介者連絡先', '要介護度', '要支援度', 'サービスタイプ',
                         'その他のサービス内容', 'トイレ介助', '食事介助', '歩行介助',
                         '服薬の有無', '薬の詳細', '希望日', '希望時間',
                         '既往歴', '配慮事項', '申込日時'])

        for req in requests:
            writer.writerow([
                req.id, req.name, req.gender, req.birthdate.strftime('%Y-%m-%d') if req.birthdate else '',
                req.phone, req.email, req.referrer_name, req.referrer_contact,
                req.care_level, req.support_level, req.service_type, req.other_service,
                req.toilet_assistance, req.meal_assistance, req.walking_assistance,
                req.has_medication, req.medication_details,
                req.preferred_date.strftime('%Y-%m-%d') if req.preferred_date else '',
                req.preferred_time, req.medical_history, req.special_notes,
                req.created_at.strftime('%Y-%m-%d %H:%M:%S') if req.created_at else ''
            ])

        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'care_service_requests_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )

    except Exception as e:
        print(f"CSVエクスポートエラー: {str(e)}")
        flash('データのエクスポート中にエラーが発生しました', 'error')
        return redirect(url_for('index'))
