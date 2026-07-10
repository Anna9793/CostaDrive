import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CostaDrive.settings')
django.setup()

from django.contrib.auth.models import User, Group

def create_roles_and_users():
    print("Iniciando configuración de roles y usuarios de CostaDrive...")
    
    # 1. Crear grupos
    groups = ['Manager', 'Receptionist', 'Maintenance', 'Client']
    created_groups = {}
    
    for g_name in groups:
        group, created = Group.objects.get_or_create(name=g_name)
        created_groups[g_name] = group
        if created:
            print(f"✅ Grupo '{g_name}' creado con éxito.")
        else:
            print(f"ℹ️ Grupo '{g_name}' ya existe.")
            
    # 2. Definir usuarios de prueba
    users_data = [
        ('manager', 'CostaDrive2026!', 'Manager', 'Luis', 'Gerente'),
        ('receptionist1', 'CostaDrive2026!', 'Receptionist', 'Elena', 'Recepcionista'),
        ('receptionist2', 'CostaDrive2026!', 'Receptionist', 'David', 'Recepcionista'),
        ('maintenance1', 'CostaDrive2026!', 'Maintenance', 'Carlos', 'Taller')
    ]
    
    # 3. Crear o actualizar usuarios e insertarlos en sus respectivos grupos
    for username, password, group_name, first_name, last_name in users_data:
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = True  # Permitir acceso al panel admin si fuera necesario
        user.save()
        
        # Asignar grupo
        group = created_groups[group_name]
        user.groups.clear()
        user.groups.add(group)
        
        status = "creado" if created else "actualizado"
        print(f"👤 Usuario '{username}' {status} e introducido en grupo '{group_name}'.")

    # 4. Sincronizar clientes existentes en Oracle como usuarios de Django
    try:
        from CostaDriveApp.models import Clientes
        all_clients = Clientes.objects.all()
        client_group = created_groups['Client']
        for c in all_clients:
            username = c.email
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=c.email,
                    password='CostaDrive2026!'
                )
                user.first_name = c.nombre
                user.last_name = c.apellidos
                user.save()
                user.groups.add(client_group)
                print(f"👤 Cliente de Oracle '{c.nombre} {c.apellidos}' sincronizado como usuario de Django.")
    except Exception as e:
        print(f"⚠️ No se pudieron sincronizar clientes: {e}")

    print("Configuración completada con éxito.")

if __name__ == '__main__':
    create_roles_and_users()
