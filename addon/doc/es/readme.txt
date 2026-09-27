# ChatGPT Companion 0.1.2 — versión experimental

Por Fernando de Paula Zamboni. https://www.blog.fernandozamboni.com

Lee mensajes enviados, respuestas y avisos de progreso accesibles en la conversación activa de ChatGPT, sin mover el foco. Utiliza la voz y el braille de NVDA. Interfaz y documentación en portugués brasileño, inglés, español, francés e italiano.

## Cambios en la versión 0.1.2

Ignorar avisos y textos de la interfaz está activado por defecto. Elimina el bloque final conocido de advertencia de errores seguido de “Respuesta más reciente”, tanto en la lectura automática como en el comando de repetición. No realiza una sustitución global: conserva frases aisladas, ejemplos entre comillas y referencias dentro de la respuesta. El reconocimiento es textual; si una respuesta termina literalmente con ese bloque completo, desactiva la opción para escucharlo. Otros pies no reconocidos pueden permanecer.

Una respuesta antigua ya no vuelve a la cola al aparecer un nuevo envío ni al desaparecer y reaparecer una respuesta ya anunciada en el árbol de accesibilidad. Las instalaciones nuevas usan 3 segundos de alternativa por silencio; se conservan los ajustes existentes. El usuario confirmó la lectura automática con esta alternativa en Chrome y en la aplicación Windows con 0.1.1. Esta actualización aún debe probarse en ambos entornos antes de publicarla.

## Cambio en la versión 0.1.1

Corregida la repetición del mensaje enviado durante las actualizaciones de la página. Cada nuevo envío se anuncia una vez; los cambios del mismo texto o su desaparición temporal no generan otro anuncio. Un nuevo envío con texto idéntico sigue reconociéndose. Para un envío silencioso, desactiva Leer mensajes enviados y Confirmar el envío. Editar un mensaje existente sin añadir otro no provoca una nueva lectura automática del envío.

## Instalación y primera prueba
Abre fzChatGPTCompanion-0.1.2.nvda-addon, confirma la instalación y reinicia NVDA cuando se solicite. Compatibilidad declarada: NVDA 2025.1 a 2026.2; aún necesita pruebas reales en Windows. lastTestedNVDAVersion indica el objetivo de compatibilidad de este paquete experimental, no una prueba de ejecución realizada.

Empieza con una conversación corta en Chrome, en https://chatgpt.com. Espera unos dos segundos y envía una pregunta sencilla. Deben leerse tu mensaje, los avisos reconocidos y la respuesta terminada. No se anuncia el historial existente. Al cambiar de pestaña, conversación o aplicación se establece una nueva referencia; no se anuncian al volver los cambios recibidos durante tu ausencia. Mantén la conversación activa durante la prueba.

Edge, Firefox, Brave y la aplicación ChatGPT para Windows son objetivos experimentales. La aplicación debe exponer un documento con texto accesible estructurado. Hay que validar cada entorno. No requiere clave ni pago adicional de API de ChatGPT.

## Configuración
Abre el menú NVDA, Preferencias, Opciones, ChatGPT Companion. Usa Tab, Espacio y las flechas, y confirma con Aceptar. Guarda la configuración de NVDA si el guardado al salir está desactivado.

- Activar lectura automática: activa o desactiva la supervisión.
- Leer mensajes enviados: lee el contenido cuando aparece en la conversación, no solo al pulsar Intro.
- Confirmar el envío: si no se leen los mensajes enviados, anuncia únicamente “Mensaje enviado”. Desactiva ambas opciones para no anunciar el envío.
- Leer respuestas y Leer actualizaciones de progreso: opciones independientes.
- Respuesta completa: predeterminada; espera un control de envío reconocido y dos segundos sin cambios de texto.
- Nuevos párrafos: experimental; lee párrafos completos durante la generación. Las revisiones del sitio pueden causar repeticiones. Sin saltos de párrafo puede esperar hasta el final.
- Espera tras la finalización: de 1 a 10 segundos; valor predeterminado 2.
- Alternativa por silencio: de 0 a 60 segundos; 0 la desactiva y el valor predeterminado para nuevas instalaciones es 3. Si no se reconoce el control de generación, un valor como 8 permite deducir el final tras un silencio. Una pausa puede provocar una lectura anticipada; no garantiza la finalización.

## Atajos
NVDA corresponde a Insert o Bloq Mayús según tu configuración. Puedes cambiar los atajos en Preferencias, Gestos de entrada, ChatGPT Companion.

- NVDA+Control+Shift+G: activar o desactivar la lectura automática.
- NVDA+Control+Shift+R: leer la última respuesta disponible, que puede ser parcial. Funciona con la lectura automática desactivada.
- NVDA+Control+Shift+P: leer el último aviso de progreso disponible.
- NVDA+Control+Shift+D: anunciar el número de mensajes reconocidos y el estado del control de generación.
- Control: detener la voz actual según el comportamiento normal de NVDA. Usa el atajo G para impedir los siguientes anuncios.

## Limitaciones y solución de problemas
“Pensamiento” se refiere únicamente a un aviso o resumen expuesto por la interfaz. No recupera razonamiento interno, texto oculto ni contenido que NVDA no pueda acceder. Reconoce encabezados de autor y controles en cinco idiomas; los cambios de interfaz pueden requerir actualizaciones. No interpreta especialmente imágenes, adjuntos ni fórmulas.

Si el diagnóstico indica cero mensajes, comprueba que has enviado uno y prueba el modo exploración con NVDA+Espacio. Si es necesario, prueba Chrome o Edge. Si reconoce mensajes pero no el control de generación, usa la lectura manual o la alternativa por silencio. Se omiten conversaciones de más de 250 000 caracteres para limitar el procesamiento; otras conversaciones largas también pueden afectar al rendimiento.

Los anuncios de regiones dinámicas del sitio o de NVDA pueden duplicar la voz. Desactiva la lectura de progreso del complemento si hace falta. No suprime globalmente los anuncios nativos. Para informar de problemas, indica versión de navegador o aplicación, versión de NVDA, idioma de interfaz y diagnóstico; no hace falta compartir la conversación. Antes de publicar, prueba cambios de pestaña, instalación, desinstalación, guardado de opciones y los cuatro atajos.

## Privacidad, licencia y distribución
No accede a la red, cookies, contraseñas, portapapeles ni archivos de conversaciones. Procesa el texto accesible en memoria mientras la conversación está activa, sin guardarlo ni enviarlo. No funciona en pantallas seguras de Windows. NVDA guarda las opciones.

GNU GPL versión 2 o posterior, sin garantía; consulta COPYING.txt. Proyecto independiente, sin afiliación con OpenAI ni NV Access. El manifest.ini de la raíz está en inglés; las traducciones están en locale. Antes de enviarlo a la Store, prueba Windows, verifica la compatibilidad declarada y publica el código fuente y un enlace HTTPS directo al paquete. La estructura del paquete no garantiza la aprobación.
