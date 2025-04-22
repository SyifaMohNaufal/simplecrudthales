from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from utils.thales import thales_decrypt, thales_encrypt, thales_decrypt_masking
from .forms import UserForm
import uuid

def user_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, full_name, email, phone, gender, ktp, address, city, province, birth_day, birth_place, nationality 
            FROM users_user
            WHERE deleted_date IS NULL
        """)
        columns = [col[0] for col in cursor.description]
        rows = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    # Decrypt KTP after fetching from DB
    for row in rows:
        if row['ktp']:
            try:
                row['ktp'] = thales_decrypt_masking(row['ktp'])
            except Exception as e:
                row['ktp'] = f"DECRYPT_ERR: {e}"  # Optional: fallback or logging

    return render(request, 'users/user_list.html', {'users': rows})


def user_create(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        encrypted_ktp = thales_encrypt(data['ktp'])
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users_user (
                    id, full_name, email, phone, gender,
                    ktp, address, city, province, birth_day, birth_place, nationality,
                    create_date
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    GETDATE()
                )
            """, [
                str(uuid.uuid4()).lower(), data['full_name'], data['email'], data['phone'], data['gender'],
                encrypted_ktp, data['address'], data['city'], data['province'],
                data['birth_day'], data['birth_place'], data['nationality']
            ])
        return redirect('user_list')

    return render(request, 'users/user_form.html', {'form': form})


def user_update(request, pk):
    form = UserForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        encrypted_ktp = thales_encrypt(data['ktp'])
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE users_user SET
                    full_name=%s, email=%s, phone=%s, gender=%s, ktp=%s,
                    address=%s, province=%s, city=%s, birth_day=%s,
                    birth_place=%s, nationality=%s, update_date=GETDATE()
                WHERE id=%s
            """, [
                data['full_name'], data['email'], data['phone'], data['gender'],
                encrypted_ktp, data['address'], data['province'], data['city'],
                data['birth_day'], data['birth_place'], data['nationality'], pk
            ])
        return redirect('user_list')
    else:
        # Fetch the data to pre-fill the form
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users_user WHERE id=%s", [pk])
            row = cursor.fetchone()
            if row:
                columns = [col[0] for col in cursor.description]
                user_dict = dict(zip(columns, row))

                # Decrypt KTP before sending to form
                if user_dict.get('ktp'):
                    try:
                        user_dict['ktp'] = thales_decrypt(user_dict['ktp'])
                    except Exception as e:
                        user_dict['ktp'] = ''  # or handle/log the error gracefully

                form = UserForm(initial=user_dict)

    return render(request, 'users/user_form.html', {'form': form})


def user_delete(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users_user SET deleted_date=GETDATE() WHERE id=%s", [pk])
        return redirect('user_list')
    else:
        # Fetch user for confirmation
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users_user WHERE id=%s", [pk])
            row = cursor.fetchone()
            user = dict(zip([col[0] for col in cursor.description], row)) if row else None
        return render(request, 'users/user_confirm_delete.html', {'user': user})

