# 📄 Documentación Técnica - TKinder Reloj

Esta documentación está dirigida a desarrolladores que deseen comprender, mantener o extender el proyecto **TKinder Reloj**. Aquí se detallan los aspectos técnicos clave del sistema.

---

## 🧠 Descripción General del Sistema

**TKinder Reloj** es una aplicación de escritorio con interfaz gráfica desarrollada en Python utilizando el módulo `tkinter`. Incorpora tres funcionalidades principales:

* Reloj digital en tiempo real
* Cronómetro con laps
* Despertador con configuración de alarmas

Cada módulo fue diseñado de forma independiente para facilitar la mantenibilidad y modularidad.

---

## 🏗️ Arquitectura y Estructura del Proyecto

```
tkinder-reloj/
│
├── main.py             # Punto de entrada principal del sistema
├── interfaz.py         # Clase Interfaz: organiza la GUI principal y pestañas
├── cronometro.py       # Clase Cronometro: lógica del cronómetro
├── despertador.py      # Clase Despertador: lógica del despertador y alarmas
├── assets/             # Capturas de pantalla y recursos visuales
├── requirements.txt    # Lista de dependencias mínimas
└── README.md           # Documentación principal del proyecto
```

---

## 🔌 Dependencias Técnicas

* `tkinter`: para la interfaz gráfica de usuario (incluido por defecto en Python)
* `datetime`: para manejo de tiempo y formato
* `pytz`: para manejo de zonas horarias

Archivo `requirements.txt`:

```txt
pytz>=2024.1
```

---

## 🧱 Diseño y Decisiones Técnicas

* Se utilizó **Programación Orientada a Objetos (POO)** para encapsular el comportamiento de cada módulo (reloj, cronómetro y despertador).
* El método `after()` de `tkinter` permite actualizaciones en tiempo real sin bloquear la interfaz.
* Uso de `StringVar` y `BooleanVar` para sincronizar widgets y lógica interna.
* El cronómetro usa control de tiempo con `datetime.now()` para precisión.

---

## 🔄 Flujo de Ejecución

1. `main.py` inicializa la interfaz principal.
2. `interfaz.py` crea las pestañas del reloj, cronómetro y despertador.
3. Cada módulo se renderiza en su propio `Frame` dentro del contenedor principal.
4. Los eventos del usuario (botones, spinbox, etc.) disparan funciones que actualizan estado interno y visual.

---

## 🧪 Pruebas Funcionales

Se realizaron pruebas manuales en:

* Windows 10
* Ubuntu 22.04

Se verificaron:

* Actualización en tiempo real del reloj
* Precisión y reinicio del cronómetro
* Alarmas activadas y desactivadas en el despertador
* Comportamiento al cambiar zona horaria

---

## 🧬 Posibles Extensiones

* Soporte para múltiples alarmas simultáneas
* Exportación de laps a CSV
* Sonidos personalizables
* Tema claro/oscuro
* Generación de ejecutables (`pyinstaller`, `cx_Freeze`)

---

## 📫 Contacto y Mantenimiento

Para colaboración o mantenimiento:

* Ver repositorio oficial en GitHub
* Utilizar issues para reportar errores o sugerencias
* Documentar toda nueva funcionalidad implementada

---

© 2025 TechKinder Dev Team
