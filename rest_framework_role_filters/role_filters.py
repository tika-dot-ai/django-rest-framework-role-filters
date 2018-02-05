class RoleFilter:
    role_id = None

    def trigger_filter(self, filter_name, *args, **kwargs):
        selected_filter = getattr(self, filter_name)
        return selected_filter(*args, **kwargs)

    def get_allowed_actions(self, request, view):
        return ['create', 'list', 'retrieve', 'update', 'partial_update', 'destroy']

    def get_queryset(self, request, view, queryset):
        return queryset


class RoleFilterGroup:
    def __init__(self, role_filters):
        self.role_filters = {role_filter.role_id: role_filter for role_filter in role_filters}

    def get_role_filter(self, role_id):
        return self.role_filters.get(role_id)

    def trigger_filter(self, filter_name, role_id, *args, **kwargs):
        role_filter = self.get_role_filter(role_id)
        if role_filter is None:
            return
        return role_filter.trigger_filter(filter_name, *args, **kwargs)

    def get_allowed_actions(self, role_id, request, view):
        return self.trigger_filter('get_allowed_actions', role_id, request, view)

    def get_queryset(self, role_id, request, view, queryset):
        return self.trigger_filter('get_queryset', role_id, request, view, queryset)