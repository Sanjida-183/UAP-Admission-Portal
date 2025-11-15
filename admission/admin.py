from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Sum
from .models import Department, Teacher, Application, ApplicationFile, Payment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'seats', 'total_credits', 'per_credit_fee', 'application_count')
    list_filter = ('seats', 'total_credits')
    search_fields = ('code', 'name')
    ordering = ('code',)
    
    def application_count(self, obj):
        count = obj.application_set.count()
        url = (
            reverse("admin:appname_application_changelist")
            + f"?department__id__exact={obj.id}"
        )
        return format_html('<a href="{}">{}</a>', url, count)
    application_count.short_description = 'Applications'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'position', 'email', 'phone', 'is_active')
    list_filter = ('department', 'position', 'is_active')
    search_fields = ('name', 'email', 'department__name')
    list_editable = ('is_active',)
    ordering = ('department', 'name')

class ApplicationFileInline(admin.TabularInline):
    model = ApplicationFile
    readonly_fields = ('uploaded_at', 'file_preview')
    extra = 0
    fields = ('file', 'file_preview', 'uploaded_at')
    
    def file_preview(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "-"
    file_preview.short_description = "Preview"

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'department', 'program', 'status', 
        'applied_at', 'has_payment', 'file_count'
    )
    list_filter = ('department', 'program', 'status', 'applied_at')
    search_fields = ('full_name', 'email', 'phone', 'department__name')
    readonly_fields = ('applied_at', 'updated_at')
    inlines = [ApplicationFileInline]
    actions = ['mark_as_pending', 'mark_as_under_review', 'mark_as_approved', 'mark_as_rejected']
    list_editable = ('status',)
    date_hierarchy = 'applied_at'
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone', 'address')
        }),
        ('Academic Information', {
            'fields': ('department', 'program', 'previous_education', 'cgpa')
        }),
        ('Application Status', {
            'fields': ('status', 'applied_at', 'updated_at', 'notes')
        }),
    )
    
    def has_payment(self, obj):
        payments = obj.payment_set.filter(status='completed')
        if payments.exists():
            total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0
            return format_html(
                '<span style="color: green;">✓ (${})</span>', 
                total_paid
            )
        return format_html('<span style="color: red;">✗</span>')
    has_payment.short_description = 'Payment'
    
    def file_count(self, obj):
        return obj.applicationfile_set.count()
    file_count.short_description = 'Files'
    
    def mark_as_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_as_pending.short_description = "Mark selected applications as Pending"
    
    def mark_as_under_review(self, request, queryset):
        queryset.update(status='under_review')
    mark_as_under_review.short_description = "Mark selected applications as Under Review"
    
    def mark_as_approved(self, request, queryset):
        queryset.update(status='approved')
    mark_as_approved.short_description = "Mark selected applications as Approved"
    
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_as_rejected.short_description = "Mark selected applications as Rejected"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'application_link', 'amount', 'status', 
        'payment_method', 'paid_at', 'transaction_id'
    )
    list_filter = ('status', 'payment_method', 'paid_at')
    search_fields = (
        'application__full_name', 
        'transaction_id', 
        'application__department__name'
    )
    readonly_fields = ('paid_at', 'created_at')
    list_editable = ('status',)
    date_hierarchy = 'paid_at'
    
    def application_link(self, obj):
        link = reverse("admin:appname_application_change", args=[obj.application.id])
        return format_html('<a href="{}">{}</a>', link, obj.application.full_name)
    application_link.short_description = 'Application'
    
    fieldsets = (
        ('Payment Information', {
            'fields': (
                'application', 'amount', 'currency', 'status', 
                'payment_method', 'transaction_id'
            )
        }),
        ('Timestamps', {
            'fields': ('paid_at', 'created_at')
        }),
    )

# Optional: Add a dashboard view
class ApplicationDashboard(admin.ModelAdmin):
    # This would require additional setup for a custom admin view
    pass