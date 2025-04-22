#!/bin/bash

echo "Ejecutando pruebas y generando reporte HTML..."
pytest \
    --html=reports/report.html \
    --self-contained-html \
    --alluredir=reports/allure-results \
    --reruns 2

echo "Reporte HTML generado en reports/report.html"

# Nota: El comando Allure debe ejecutarse en el host, no dentro del contenedor
echo "Para generar el reporte Allure, ejecuta el siguiente comando en el host:"
echo "docker run --rm -v \$(pwd)/reports/allure-results:/allure-results -v \$(pwd)/reports/allure-report:/allure-report frankescobar/allure generate /allure-results -o /allure-report"