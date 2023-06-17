class scopesObject:
    def __init__(self):
        self.all_scopes = {
            'notes': [
                {
                    'name': 'read',
                    'description': 'Permission to read all your notes.'
                },
                {
                    'name': 'manage',
                    'description': 'Permission to manage all your notes.'
                }
            ]
        }


    def validate_scope(self, scope):
        scope = scope.split('.')

        if len(scope) != 2:
            return False

        if scope[0] not in self.all_scopes.keys():
            return False
        elif scope[1] not in [s['name'] for s in self.all_scopes[scope[0]]]:
            return False

        return True

    def get_scope_description(self, scope):
        return [s['description'] for s in self.all_scopes[scope.split('.')[0]] if s['name'] == scope.split('.')[1]][0]