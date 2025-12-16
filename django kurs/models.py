from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class UserProfile(models.Model):
    ACCESS_LEVELS = [
        ('viewer', 'Обычный пользователь'),
        ('admin', 'Администратор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    company = models.CharField(max_length=100, verbose_name='Компания', blank=True, default='')
    position = models.CharField(max_length=100, verbose_name='Должность', blank=True, default='')
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVELS, default='viewer')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_access_level_display()}"
    
    def is_admin(self):
        return self.access_level == 'admin'
    
class SafetyDocument(models.Model):
    CATEGORY_CHOICES = [
        ('Охрана труда', 'Охрана труда'),
        ('Пожарная безопасность', 'Пожарная безопасность'),
        ('Работа на высоте', 'Работа на высоте'),
        ('Эксплуатация техники', 'Эксплуатация техники'),
        ('СИЗ', 'Средства индивидуальной защиты'),
        ('Электробезопасность', 'Электробезопасность'),
        ('Общие', 'Общие требования'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название документа')
    description = models.TextField(verbose_name='Описание', blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Общие', verbose_name="Категория")
    file = models.FileField(upload_to='documents/%Y/%m/%d/', verbose_name='Файл')
    file_size = models.CharField(max_length=20, blank=True, verbose_name="Размер файла")
    file_type = models.CharField(max_length=10, blank=True, verbose_name="Тип файла")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Автоматически определяем размер и тип файла при сохранении
        if self.file:
            # Размер файла
            size = self.file.size
            if size < 1024:
                self.file_size = f"{size} B"
            elif size < 1024 * 1024:
                self.file_size = f"{size/1024:.1f} KB"
            else:
                self.file_size = f"{size/(1024*1024):.1f} MB"
            
            # Тип файла
            filename = self.file.name
            ext = filename.split('.')[-1].lower() if '.' in filename else ''
            self.file_type = ext.upper()
        
        super().save(*args, **kwargs)

    def get_file_extension(self):
        """Получить расширение файла"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ''

    def is_pdf(self):
        """Проверить, является ли файл PDF"""
        return self.get_file_extension() == '.pdf'

    def delete(self, *args, **kwargs):
        """Переопределяем метод delete для удаления файла"""
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
    
@receiver(pre_delete, sender=SafetyDocument)
def delete_document_file(sender, instance, **kwargs):
    """Удаляет файл при удалении объекта"""
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

class SafetyMonitoring(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('processing', 'Обрабатывается'),
        ('completed', 'Завершено'),
        ('failed', 'Ошибка'),
    ]
    
    VIOLATION_TYPES = [
        ('no_helmet', 'Отсутствие каски'),
        ('no_vest', 'Отсутствие жилета'),
        ('improper_ppe', 'Неправильное использование СИЗ'),
        ('unsafe_conditions', 'Небезопасные условия'),
    ]

    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    original_image = models.ImageField(upload_to='monitoring/original/%Y/%m/%d/', verbose_name="Исходное изображение")
    analyzed_image = models.ImageField(upload_to='monitoring/analyzed/%Y/%m/%d/', verbose_name="Проанализированное изображение", blank=True, null=True)
    
    # Статистика
    total_people = models.IntegerField(default=0, verbose_name="Всего людей")
    people_with_helmets = models.IntegerField(default=0, verbose_name="Людей в касках")
    people_without_helmets = models.IntegerField(default=0, verbose_name="Людей без касок")
    violations_detected = models.IntegerField(default=0, verbose_name="Нарушений обнаружено")
    
    # Детекции
    helmet_detections = models.JSONField(default=dict, verbose_name="Обнаруженные каски")
    head_detections = models.JSONField(default=dict, verbose_name="Обнаруженные головы")
    person_detections = models.JSONField(default=dict, verbose_name="Обнаруженные люди")
    
    compliance_rate = models.FloatField(default=0.0, verbose_name="Уровень соблюдения")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    
    created_at = models.DateTimeField(auto_now_add=True)
    analyzed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Мониторинг безопасности"
        verbose_name_plural = "Мониторинг безопасности"
        ordering = ['-created_at']

    def __str__(self):
        return f"Анализ от {self.created_at.strftime('%d.%m.%Y %H:%M')}"

class Violation(models.Model):
    monitoring_session = models.ForeignKey(SafetyMonitoring, on_delete=models.CASCADE, related_name='violations')
    violation_type = models.CharField(max_length=50, choices=SafetyMonitoring.VIOLATION_TYPES, verbose_name="Тип нарушения")
    description = models.TextField(verbose_name="Описание нарушения")
    coordinates = models.JSONField(verbose_name="Координаты нарушения")
    confidence = models.FloatField(verbose_name="Уверенность")
    
    class Meta:
        verbose_name = "Нарушение"
        verbose_name_plural = "Нарушения"