#!/bin/bash

# Crear directorios para reportes
mkdir -p reports/allure-results reports/screenshots

echo "Ejecutando pruebas y generando reporte HTML..."
pytest \
    --browser=firefox \
    --headless \
    --html=reports/report.html \
    --self-contained-html \
    --alluredir=reports/allure-results \
    --reruns 2

# Verificar si las pruebas se ejecutaron correctamente
if [ $? -eq 0 ]; then
  echo "Pruebas ejecutadas correctamente. Resultados en reports/allure-results."
else
  echo "Error al ejecutar las pruebas."
  exit 1
fi

echo "Reporte HTML generado en reports/report.html"
echo "Para generar el reporte Allure, ejecuta el siguiente comando en el host:"
echo "docker run --rm -v \$(pwd)/reports/allure-results:/app/allure-results -v \$(pwd)/reports/allure-report:/app/allure-report frankescobar/allure-docker-service"