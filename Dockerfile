FROM python:3.12

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requisitos
COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del proyecto en el contenedor
COPY . .

# Expone el puerto en el que la aplicación correrá
EXPOSE 5002

# Comando para correr la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]