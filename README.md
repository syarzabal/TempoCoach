# Cómo utilizar este repositorio

Después de clonar el repositorio es necesario configurar un intérprete de python y un entorno virtual.
En dicho entorno virtual será necesario instalar las dependencias indicadas en 
el archivo requirements.txt
``` powershell
pip install -r requirements.txt
```

Para generar las clases UML descargar pyreverse y Graphviz y ejecutar el siguiente comando:
``` powershell
pyreverse -o png -p TempoCoach .
```