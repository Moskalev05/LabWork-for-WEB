from django.contrib import admin
from .models import UserProfile, SafetyDocument

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'position', 'access_level', 'created_at')
    list_filter = ('access_level', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'company')

@admin.register(SafetyDocument)
class SafetyDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

# Создаем демо-документы через админку при первом запуске
def create_demo_documents():
    if not SafetyDocument.objects.exists():
        documents = [
            {
                'title': 'Инструкции по охране труда',
                'description': 'Основные инструкции и правила по охране труда для строительных работ'
            },
            {
                'title': 'Требования к средствам индивидуальной защиты',
                'description': 'Нормативы и правила использования СИЗ на строительной площадке'
            },
            # Добавьте остальные документы по аналогии
        ]
        for doc_data in documents:
            SafetyDocument.objects.create(**doc_data)

# Вызываем при загрузке админки
create_demo_documents()