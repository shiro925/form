document.addEventListener('DOMContentLoaded', function() {
    // サービスタイプの選択によって関連フィールドの表示/非表示を切り替える
    const serviceTypeRadios = document.querySelectorAll('input[name="service_type"]');
    const otherServiceField = document.getElementById('other-service-field');
    const dailyAssistanceFields = document.getElementById('daily-assistance-fields');
    
    if (serviceTypeRadios.length > 0 && (otherServiceField || dailyAssistanceFields)) {
        // 初期状態の設定
        toggleServiceRelatedFields();
        
        // ラジオボタン変更時の処理
        serviceTypeRadios.forEach(radio => {
            radio.addEventListener('change', toggleServiceRelatedFields);
        });
    }
    
    function toggleServiceRelatedFields() {
        const otherRadio = document.querySelector('input[name="service_type"][value="other"]');
        const dailyRadio = document.querySelector('input[name="service_type"][value="daily"]');
        const medicalRadio = document.querySelector('input[name="service_type"][value="medical"]');
        
        // 「その他」の処理
        if (otherRadio && otherServiceField) {
            otherServiceField.style.display = otherRadio.checked ? 'block' : 'none';
        }
        
        // 「生活支援」の処理
        if (dailyRadio && dailyAssistanceFields) {
            dailyAssistanceFields.style.display = dailyRadio.checked ? 'block' : 'none';
        }
        
        // 「受診同行」の処理
        const medicalDetailsFields = document.getElementById('medical-details-fields');
        if (medicalRadio && medicalDetailsFields) {
            medicalDetailsFields.style.display = medicalRadio.checked ? 'block' : 'none';
            
            // 薬の詳細表示も確認
            toggleMedicationDetailsField();
        }
    }
    
    // 服薬情報の詳細フィールド表示切替
    function toggleMedicationDetailsField() {
        const hasMedicationYes = document.querySelector('input[name="has_medication"][value="yes"]');
        const medicationDetailsField = document.getElementById('medication-details-field');
        
        if (hasMedicationYes && medicationDetailsField) {
            medicationDetailsField.style.display = hasMedicationYes.checked ? 'block' : 'none';
        }
    }
    
    // 服薬情報のラジオボタン変更イベント
    const medicationRadios = document.querySelectorAll('input[name="has_medication"]');
    if (medicationRadios.length > 0) {
        medicationRadios.forEach(radio => {
            radio.addEventListener('change', toggleMedicationDetailsField);
        });
    }
    
    // 要介護度と要支援度の相互排他的な選択
    const careLevelSelect = document.getElementById('care_level');
    const supportLevelSelect = document.getElementById('support_level');
    
    if (careLevelSelect && supportLevelSelect) {
        careLevelSelect.addEventListener('change', function() {
            if (this.value !== '' && this.value !== 'none') {
                supportLevelSelect.value = '';
                supportLevelSelect.disabled = true;
            } else {
                supportLevelSelect.disabled = false;
            }
        });
        
        supportLevelSelect.addEventListener('change', function() {
            if (this.value !== '' && this.value !== 'none') {
                careLevelSelect.value = '';
                careLevelSelect.disabled = true;
            } else {
                careLevelSelect.disabled = false;
            }
        });
        
        // 初期状態の設定
        if (careLevelSelect.value !== '' && careLevelSelect.value !== 'none') {
            supportLevelSelect.disabled = true;
        }
        
        if (supportLevelSelect.value !== '' && supportLevelSelect.value !== 'none') {
            careLevelSelect.disabled = true;
        }
    }
    
    // 入力フォームのフォーカス時のエフェクト
    const formControls = document.querySelectorAll('.form-control, .form-select');
    formControls.forEach(element => {
        element.addEventListener('focus', function() {
            this.closest('.mb-3').classList.add('highlight');
        });
        
        element.addEventListener('blur', function() {
            this.closest('.mb-3').classList.remove('highlight');
        });
    });
    
    // 生年月日フィールドの設定
    const birthdateField = document.getElementById('birthdate');
    if (birthdateField) {
        // 100年前から今日までの範囲で設定
        const today = new Date();
        const hundredYearsAgo = new Date();
        hundredYearsAgo.setFullYear(today.getFullYear() - 100);
        
        flatpickr(birthdateField, {
            dateFormat: "Y-m-d",
            locale: "ja",
            maxDate: today,
            minDate: hundredYearsAgo,
            disableMobile: true,
            allowInput: true,
            static: true
        });
    }
    
    // 希望日フィールドの設定
    const preferredDateField = document.getElementById('preferred_date');
    if (preferredDateField) {
        // 今日から1年先までの範囲で設定
        const today = new Date();
        const oneYearLater = new Date();
        oneYearLater.setFullYear(today.getFullYear() + 1);
        
        // 最小値は明日から（当日は設定できないように）
        const tomorrow = new Date();
        tomorrow.setDate(today.getDate() + 1);
        
        flatpickr(preferredDateField, {
            dateFormat: "Y-m-d",
            locale: "ja",
            minDate: tomorrow,
            maxDate: oneYearLater,
            disableMobile: true,
            allowInput: true,
            static: true
        });
    }
    
    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        
        return `${year}-${month}-${day}`;
    }
    
    // フォームの送信前バリデーション
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            // サービスタイプが「その他」の場合、その他の希望内容が必須
            const otherRadio = document.querySelector('input[name="service_type"][value="other"]');
            const otherServiceInput = document.getElementById('other_service');
            
            if (otherRadio && otherRadio.checked && otherServiceInput && otherServiceInput.value.trim() === '') {
                event.preventDefault();
                const errorMsg = document.createElement('div');
                errorMsg.className = 'invalid-feedback';
                errorMsg.textContent = 'その他の希望内容を入力してください';
                errorMsg.style.display = 'block';
                
                // 既存のエラーメッセージがあれば削除
                const existingError = otherServiceInput.nextElementSibling;
                if (existingError && existingError.className === 'invalid-feedback') {
                    existingError.remove();
                }
                
                otherServiceInput.classList.add('is-invalid');
                otherServiceInput.parentNode.appendChild(errorMsg);
                otherServiceInput.focus();
            }
        });
    }
    
    // スムーズスクロール
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
            }
        });
    });
});
