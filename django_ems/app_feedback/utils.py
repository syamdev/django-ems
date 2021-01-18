def mark_feedback_as_read(modeladmin, request, queryset):
    for employeeFeedback in queryset:
        employeeFeedback.is_read = True
        employeeFeedback.save()
    modeladmin.message_user(request, "%s successfully marked as read" % len(queryset))


mark_feedback_as_read.short_description = 'Mark selected feedback as read'
