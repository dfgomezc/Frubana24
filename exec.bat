@echo off
REM Establecer la ubicación del directorio base
SET BASE_DIR=C:\Frubana24

REM Establecer la ubicación del ejecutable de Python en el ambiente virtual
SET PYTHON_EXEC=%BASE_DIR%\frubana-env\Scripts\python.exe

REM Establecer la ubicación del script a ejecutar
SET SCRIPT=%BASE_DIR%\SCRIPTS\etl_sql.py

REM Cambiar al directorio base
cd /d %BASE_DIR%

REM Ejecutar el script con el ambiente virtual de Python
%PYTHON_EXEC% %SCRIPT%

SET SCRIPT2=%BASE_DIR%\SCRIPTS\recomendador_apriori.py
%PYTHON_EXEC% %SCRIPT2%

SET SCRIPT3=%BASE_DIR%\SCRIPTS\mod_elasticidades.py
%PYTHON_EXEC% %SCRIPT3%

REM Pausa para mantener la ventana abierta y ver cualquier salida
pause
