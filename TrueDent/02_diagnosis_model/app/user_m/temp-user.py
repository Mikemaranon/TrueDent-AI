from werkzeug.security import generate_password_hash
import json

# Solicitar la contraseña al usuario
password = input("Introduce la contraseña: ")

# Generar el hash de la contraseña
hashed_password = generate_password_hash(password)

# Cargar los usuarios existentes del archivo JSON
with open('../data_m/users.json', 'r') as f:
    users = json.load(f)

# Solicitar el nombre de usuario
username = input("Introduce el nombre de usuario: ")

# Añadir el nuevo usuario con la contraseña hasheada al diccionario de usuarios
# Estructura: el nombre del usuario será la clave y el valor será un diccionario con la clave "password"
users[username] = {"password": hashed_password}

# Guardar el archivo JSON con el nuevo usuario
with open('../data_m/users.json', 'w') as f:
    json.dump(users, f, indent=4)

print(f"Usuario {username} añadido con la contraseña hasheada.")
