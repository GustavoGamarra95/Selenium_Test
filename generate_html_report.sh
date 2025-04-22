#!/bin/bash
mkdir -p reports

# Ejecutar pruebas con pytest para generar el reporte HTML
echo "Ejecutando pruebas y generando reporte HTML..."
pytest --html=reports/report.html --self-contained-html

# Verificar si el reporte se generó
if [ -f reports/report.html ]; then
    echo "Reporte HTML generado en reports/report.html"
    
    # Abrir el reporte en el navegador por defecto
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open reports/report.html  # Mac
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open reports/report.html  # Linux
    elif [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "cygwin"* ]]; then
        start reports/report.html  # Windows
    else
        echo "Por favor, abre reports/report.html manualmente en tu navegador."
    fi
else
    echo "Error: No se pudo generar el reporte HTML."
    exit 1
fi