from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, FileResponse, Http404
from .forms import CustomUserCreationForm, UserProfileForm, DocumentForm
from .models import SafetyDocument, UserProfile, SafetyMonitoring, Violation
from .decorators import admin_required
from django import forms
from django.contrib.auth.models import User
import os
from django.http import JsonResponse
from .services.yolo_service import safety_analyzer
from django.core.files.base import ContentFile
from PIL import Image
import json

def home(request):
    return render(request, 'myapp/home.html')

def about(request):
    return render(request, 'myapp/about.html')

def documents(request):
    docs = SafetyDocument.objects.all().order_by('-created_at')
    return render(request, 'myapp/documents.html', {'documents': docs})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Сохраняем пользователя через форму
                user = form.save()
                
                # Создаем профиль пользователя
                UserProfile.objects.create(
                    user=user,
                    phone=form.cleaned_data['phone'],
                    company='',
                    position='',
                    access_level='viewer'
                )
                
                # АВТОМАТИЧЕСКИ ВХОДИМ В СИСТЕМУ
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Регистрация прошла успешно! Добро пожаловать, {user.username}!')
                    return redirect('home')  # Перенаправляем на главную страницу
                else:
                    # Если что-то пошло не так с аутентификацией
                    messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти в систему.')
                    return redirect('login')
                
            except Exception as e:
                messages.error(request, f'Ошибка при регистрации: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'myapp/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        # Обычные пользователи не могут менять уровень доступа
        form_data = request.POST.copy()
        if not request.user.userprofile.is_admin():
            form_data['access_level'] = request.user.userprofile.access_level
        
        form = UserProfileForm(form_data, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
        # Скрываем поле уровня доступа для обычных пользователей
        if not request.user.userprofile.is_admin():
            form.fields['access_level'].widget = forms.HiddenInput()
    
    return render(request, 'myapp/profile.html', {'form': form})

@admin_required
def manage_users(request):
    """Управление пользователями"""
    users = User.objects.all().select_related('userprofile').order_by('-date_joined')
    return render(request, 'myapp/manage_users.html', {'users': users})

@admin_required
def edit_user(request, user_id):
    """Редактирование пользователя"""
    try:
        user = User.objects.get(id=user_id)
        user_profile = user.userprofile
        
        if request.method == 'POST':
            # Обновляем данные пользователя
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()
            
            # Обновляем профиль
            user_profile.phone = request.POST.get('phone')
            user_profile.company = request.POST.get('company')
            user_profile.position = request.POST.get('position')
            user_profile.access_level = request.POST.get('access_level')
            user_profile.save()
            
            messages.success(request, f'Данные пользователя {user.username} обновлены!')
            return redirect('manage_users')
        
        context = {
            'edit_user': user,
            'user_profile': user_profile
        }
        return render(request, 'myapp/edit_user.html', context)
        
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден')
        return redirect('manage_users')

@admin_required
def delete_user(request, user_id):
    """Удаление пользователя"""
    try:
        user = User.objects.get(id=user_id)
        username = user.username
        
        # Нельзя удалить самого себя
        if user == request.user:
            messages.error(request, 'Вы не можете удалить свой собственный аккаунт!')
        else:
            user.delete()
            messages.success(request, f'Пользователь {username} удален!')
            
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден')
    
    return redirect('manage_users')

@admin_required
def change_user_access(request, user_id):
    """Изменение уровня доступа пользователя"""
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            new_access_level = request.POST.get('access_level')
            if new_access_level in ['viewer', 'admin']:
                user.userprofile.access_level = new_access_level
                user.userprofile.save()
                messages.success(request, f'Уровень доступа пользователя {user.username} изменен')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь не найден')
    
    return redirect('manage_users')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Ваш аккаунт неактивен.')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    
    return render(request, 'myapp/login.html')

def custom_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')

def documents(request):
    # Получаем все активные документы
    docs = SafetyDocument.objects.filter(is_active=True).order_by('-created_at')
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        docs = docs.filter(category=category)
    
    # Поиск по названию
    search_query = request.GET.get('search')
    if search_query:
        docs = docs.filter(title__icontains=search_query)
    
    context = {
        'documents': docs,
        'categories': SafetyDocument.CATEGORY_CHOICES,
    }
    return render(request, 'myapp/documents.html', context)

def document_view(request, document_id):
    """Просмотр документа (для PDF)"""
    document = get_object_or_404(SafetyDocument, id=document_id, is_active=True)
    
    if document.is_pdf() and document.file:
        # Для PDF показываем в браузере
        response = FileResponse(document.file.open(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{document.file.name}"'
        return response
    else:
        # Для других типов файлов перенаправляем на скачивание
        return redirect('document_download', document_id=document_id)

def document_download(request, document_id):
    """Скачивание документа"""
    document = get_object_or_404(SafetyDocument, id=document_id, is_active=True)
    
    if document.file:
        response = FileResponse(document.file.open(), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
        return response
    else:
        raise Http404("Файл не найден")

@admin_required
@login_required
def document_create(request):
    """Создание нового документа"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            messages.success(request, f'Документ "{document.title}" успешно добавлен!')
            return redirect('documents')
    else:
        form = DocumentForm()
    
    return render(request, 'myapp/document_form.html', {'form': form, 'title': 'Добавить документ'})

@admin_required
@login_required
def document_edit(request, document_id):
    """Редактирование документа"""
    document = get_object_or_404(SafetyDocument, id=document_id)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, f'Документ "{document.title}" успешно обновлен!')
            return redirect('documents')
    else:
        form = DocumentForm(instance=document)
    
    return render(request, 'myapp/document_form.html', {'form': form, 'title': 'Редактировать документ', 'document': document})

@admin_required
@login_required
def document_delete(request, document_id):
    """Удаление документа с подтверждением"""
    document = get_object_or_404(SafetyDocument, id=document_id)
    
    if request.method == 'POST':
        title = document.title
        try:
            # Удаляем документ (файл удалится автоматически благодаря переопределенному методу delete)
            document.delete()
            messages.success(request, f'Документ "{title}" успешно удален!')
            return redirect('documents')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении документа: {str(e)}')
            return redirect('documents')
    
    return render(request, 'myapp/document_confirm_delete.html', {'document': document})

@login_required
def monitoring(request):
    """Страница мониторинга"""
    recent_analyses = SafetyMonitoring.objects.filter(uploaded_by=request.user).order_by('-created_at')[:5]
    return render(request, 'myapp/monitoring.html', {'recent_analyses': recent_analyses})

@login_required
def upload_monitoring_image(request):
    """Загрузка и анализ изображения"""
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            
            # Сохраняем оригинальное изображение
            monitoring_session = SafetyMonitoring.objects.create(
                uploaded_by=request.user,
                status='processing'
            )
            monitoring_session.original_image.save(
                image_file.name,
                ContentFile(image_file.read())
            )
            
            # Анализируем изображение
            analysis_result = safety_analyzer.analyze_image(
                monitoring_session.original_image.path
            )
            
            if analysis_result.get('success'):
                stats = analysis_result['statistics']
                
                # Обновляем сессию мониторинга
                monitoring_session.total_people = stats['total_people']
                monitoring_session.people_with_helmets = stats['people_with_helmets']
                monitoring_session.people_without_helmets = stats['people_without_helmets']
                monitoring_session.violations_detected = stats['violations_count']
                monitoring_session.compliance_rate = stats['compliance_rate']
                monitoring_session.helmet_detections = analysis_result['detections']['helmets']
                monitoring_session.head_detections = analysis_result['detections']['heads']
                monitoring_session.person_detections = analysis_result['detections']['persons']
                monitoring_session.status = 'completed'
                
                # Сохраняем аннотированное изображение
                if os.path.exists(analysis_result['annotated_image']):
                    with open(analysis_result['annotated_image'], 'rb') as f:
                        monitoring_session.analyzed_image.save(
                            f"analyzed_{image_file.name}",
                            ContentFile(f.read())
                        )
                    # Удаляем временный файл
                    os.remove(analysis_result['annotated_image'])
                
                monitoring_session.save()
                
                # Создаем записи о нарушениях
                if stats['people_without_helmets'] > 0:
                    Violation.objects.create(
                        monitoring_session=monitoring_session,
                        violation_type='no_helmet',
                        description=f"Обнаружено {stats['people_without_helmets']} человек без касок",
                        coordinates={"count": stats['people_without_helmets']},
                        confidence=0.95
                    )
                
                return JsonResponse({
                    'success': True,
                    'session_id': monitoring_session.id,
                    'statistics': stats,
                    'debug_info': analysis_result.get('debug_info', {}),
                    'annotated_image_url': monitoring_session.analyzed_image.url if monitoring_session.analyzed_image else None
                })
            else:
                monitoring_session.status = 'failed'
                monitoring_session.save()
                return JsonResponse({
                    'success': False,
                    'error': analysis_result.get('error', 'Неизвестная ошибка')
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Ошибка обработки: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': 'Неверный запрос'})

@login_required
def get_analysis_results(request, session_id):
    """Получение результатов анализа"""
    try:
        session = SafetyMonitoring.objects.get(id=session_id, uploaded_by=request.user)
        
        return JsonResponse({
            'success': True,
            'statistics': {
                'total_people': session.total_people,
                'people_with_helmets': session.people_with_helmets,
                'people_without_helmets': session.people_without_helmets,
                'compliance_rate': session.compliance_rate,
                'violations_count': session.violations_detected,
                'helmets_detected': len(session.helmet_detections) if session.helmet_detections else 0,
                'heads_detected': len(session.head_detections) if session.head_detections else 0,
                'persons_detected': len(session.person_detections) if session.person_detections else 0,
            },
            'detections': {
                'helmets': session.helmet_detections,
                'heads': session.head_detections,
                'persons': session.person_detections
            },
            'annotated_image_url': session.analyzed_image.url if session.analyzed_image else None,
            'created_at': session.created_at.strftime('%d.%m.%Y %H:%M')
        })
    except SafetyMonitoring.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Сессия не найдена'})