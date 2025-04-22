#!/bin/bash

echo "Ejecutando pruebas y generando reporte HTML..."
pytest --browser=chrome --headless \
    --html=reports/report.html \
    --self-contained-html \
    --alluredir=reports/allure-results \
    --reruns 2

echo "Reporte HTML generado en reports/report.html"

# Generar reporte Allure
docker run --rm \
    -v "$(pwd)/reports/allure-results:/allure-results" \
    -v "$(pwd)/reports/allure-report:/allure-report" \
    frankescobar/allure \
    generate /allure-results -o /allure-report

echo "Reporte Allure generado en reports/allure-report"