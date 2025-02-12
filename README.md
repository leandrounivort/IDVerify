# **IDVerify**

**Descripción**  
Esta aplicación permite comprobar el titular de un documento digitalizado mediante el uso de OCR (Reconocimiento Óptico de Caracteres) utilizando la API de ChatGPT. Compara el nombre del titular extraído del documento con el nombre provisto, y sin necesidad de que coincidan los nombres completos. Basta con que todos los nombres provistos coincidan para que indique que el titular es el mismo.

La aplicación está diseñada con una interfaz gráfica basada en **Gradio**, lo que permite desarrollar rápidamente un prototipo sencillo para una demostración a un cliente.

---

## **Características**

- **OCR con API de ChatGPT**: La aplicación utiliza OCR para extraer el texto del documento y luego realiza la comparación con el nombre proporcionado a través de la API de ChatGPT.
  
- **Interfaz Gráfica**: La interfaz es sencilla y fácil de usar, diseñada para facilitar la interacción con la aplicación y permitir un flujo de trabajo eficiente.

- **Tres versiones de la aplicación**:
  1. **Versión Básica**: Admite un documento y compara el nombre provisto sin margen de error. El nombre debe coincidir exactamente con el del titular del documento.
  2. **Versión Batch**: Similar a la versión básica, pero admite la carga de un batch (lote) de documentos para realizar la comprobación de múltiples documentos a la vez.
  3. **Versión Tolerante**: Permite errores de tipeo al comparar el nombre del titular. Se puede configurar el número de errores permitidos, lo que hace que la comparación sea más flexible.

---

## **Instalación**

1. Clona este repositorio:
    ```bash
    git clone https://github.com/leandrounivort/IDVerify.git
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

3. Asegúrate de tener acceso a la API de **ChatGPT** y configura la clave de la API en el archivo `.env`.

4. Ejecuta la aplicación:
    ```bash
    jupyter notebook UI_gradio.ipynb
    ```

---

## **Uso**

1. **Versión Básica**:
    - Sube un documento (imagen).
    - Proporciona el nombre del titular que quieres verificar.
    - La aplicación devolverá si el nombre del titular del documento coincide exactamente con el nombre proporcionado.

2. **Versión Batch**:
    - Sube un lote de documentos.
    - Proporciona el nombre de los titulares a verificar para cada documento.
    - La aplicación devolverá los resultados para todos los documentos en el lote.

3. **Versión Tolerante**:
    - Sube un documento.
    - Proporciona el nombre del titular y ajusta el número de errores permitidos.
    - La aplicación será capaz de encontrar coincidencias incluso si hay pequeños errores de tipeo en el nombre.

---

## **Contribución**

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork de este repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y asegúrate de que las pruebas pasen.
4. Haz un commit de tus cambios (`git commit -am 'Agregada nueva funcionalidad'`).
5. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
6. Abre un Pull Request.

---

## **Licencia**

Este proyecto está bajo la licencia GPL. Consulta el archivo `LICENSE` para más detalles.

---

Si tienes alguna pregunta o necesitas ayuda, no dudes en contactar al autor o abrir un issue en GitHub.
