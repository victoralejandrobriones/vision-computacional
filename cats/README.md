Detección de rostros de gatos
=

Detección de rostros de gatos por: Víctor Briones.

Blog: http://vic-en-fime.blogspot.mx

Instalación
=

Para poder utilizar este software solo se necesita descargar y ejecutar el script de Python, siempre y cuando se tengan las librerias necesarias (Ver archivo INSTALL).

Ejecución:
=

El archivo contiene todos los filtros y algoritmos que se desarrollaron a lo largo del semestre, y están disponibles para su uso, pero para el proyecto solo se ocupa un comando en terminal:
    
    python filtro.py <nombre de la imagen> CAT
    
De esa manera el script solo ejecutará las funciones requeridas para la detección de rostros.

Funcionamiento
=

Actualmente el script soporta solo imagenes de gatos con caras viendo de frente y con fondos nitidos, si el fondo no es del todo claro o si el gato esta inclinado o viendo hacia otro lugar, lo más probable es que no se detecte nada o se generen caras "fantasmas" puesto que el script funciona mediante la búsqueda de características faciales.

Las características faciales se detectan mediante el uso de line edge maps; un mapa de puntos que describen ciertas zonas del rostro muy destacadas. Se aplican varios filtros para generar el mapeado y despues se aplican dilataciones para adelgazar los puntos menos visibles, quedando por lo general los ojos, la nariz, etc.

Acerca del proyecto
=
Proyecto de la materia Visión Computacional impartida por la Doctora Elisa Schaeffer en la Facultad de Ingeniería Mecánica y Eléctrica de la Universidad Autónoma de Nuevo León.

Página del curso: http://elisa.dyndns-web.com/~elisa/teaching/comp/vision/2013.html
