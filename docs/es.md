# ChatGPT Companion

Por Fernando de Paula Zamboni. Versión 0.1.3 (beta).

Complemento de NVDA para leer nuevos mensajes en el sitio web y la aplicación Windows de ChatGPT. Puede leer respuestas automáticamente, leer o confirmar mensajes enviados y anunciar avisos accesibles de progreso sin mover el foco.

## Objetivo

Permite seguir la conversación sin volver constantemente desde el cuadro de escritura a la última respuesta. Utiliza tu cuenta e interfaz habituales, sin otro cliente, clave de API ni pago adicional de API. La voz y el braille usan la configuración de NVDA.

Otros complementos pueden ofrecer funciones similares. Este se centra en anuncios automáticos en la interfaz existente, con controles independientes para mensajes enviados, respuestas y progreso. Es una ayuda opcional; no sustituye las mejoras de accesibilidad del propio ChatGPT.

## Instalación y uso

Descarga ChatGPTCompanion-0.1.3.nvda-addon, ábrelo con NVDA funcionando, confirma la instalación y reinicia NVDA. Requiere NVDA 2026.2 o posterior; la versión de API declarada como probada es 2026.2. Versiones futuras pueden necesitar una revisión de compatibilidad.

Descargas: https://github.com/zambonif/ChatGPTCompanion/releases

Código fuente y problemas: https://github.com/zambonif/ChatGPTCompanion

Abre una conversación en Chrome o la aplicación Windows, espera un momento y envía una pregunta. El autor confirmó la lectura en ambos entornos con versiones anteriores. Las nuevas correcciones de 0.1.3 todavía requieren pruebas reales. Edge, Firefox y Brave son objetivos experimentales adicionales.

No se anuncia el historial al abrir una conversación. Solo se supervisa la conversación activa. Se recuerdan hasta ocho contextos durante la sesión de NVDA: si sales de una conversación reconocida y vuelves tras recibir una respuesta, esta puede anunciarse al regresar. No hay lectura en segundo plano. Reiniciar NVDA o alternar la supervisión mediante su atajo borra esa memoria.

## Opciones

Menú NVDA, Preferencias, Opciones, ChatGPT Companion. Las actualizaciones conservan los ajustes. Guarda la configuración si el guardado automático está desactivado.

- Activar lectura automática: activa o desactiva la supervisión.
- Leer mensajes enviados: lee el contenido tras aparecer en la conversación.
- Confirmar el envío: anuncia solo “Mensaje enviado” si la lectura anterior está desactivada. Desactiva ambas para un envío silencioso.
- Leer respuestas y Leer actualizaciones de progreso: controles independientes.
- Ignorar avisos y textos de la interfaz: activado por defecto; filtra bloques finales conocidos. Desactívalo si elimina un ejemplo literal del pie al final de una respuesta.
- Respuesta completa: espera un control de finalización reconocido y texto estable. Nuevos párrafos es una alternativa experimental durante la generación.
- Espera tras la finalización: 1–10 segundos; predeterminado 2.
- Alternativa por silencio: 0–60 segundos; predeterminado 3 para instalaciones nuevas. Se usa si no se reconoce el control de generación. Una pausa larga puede parecer el final; aumenta el valor si lee demasiado pronto. 0 desactiva esta alternativa.

## Atajos

NVDA es Insert o Bloq Mayús según la configuración. Reasigna los comandos en Gestos de entrada, ChatGPT Companion.

- NVDA+Control+Shift+G: activar o desactivar la lectura automática.
- NVDA+Control+Shift+R: leer la última respuesta disponible, posiblemente parcial. Si una pregunta nueva espera respuesta, no se sustituye por la anterior.
- NVDA+Control+Shift+P: leer el último aviso accesible de progreso.
- NVDA+Control+Shift+D: actualizar el diagnóstico de los mensajes recientes y del control de generación.
- Control: detener la voz actual. Usa el atajo G para evitar anuncios automáticos posteriores.

## Problemas y límites

Si no lee, comprueba Leer respuestas, prueba R y D y revisa la alternativa por silencio. El diagnóstico cuenta el tramo reciente, no todo el historial. Prueba el modo exploración con NVDA+Espacio si no reconoce la conversación.

Solo puede leer texto y encabezados de autor expuestos a NVDA. Si no obtiene la respuesta actual, informa que no hay respuesta disponible en vez de usar deliberadamente una anterior guardada. Los cambios de interfaz pueden afectar a la detección. No interpreta imágenes, adjuntos ni fórmulas de forma especial. Progreso significa avisos accesibles, no razonamiento interno.

La versión 0.1.3 busca desde el final y ya no descarta historiales de más de 250.000 caracteres. Las respuestas individuales enormes o proveedores sin navegación por encabezados aún pueden causar lentitud o lecturas incompletas. La búsqueda alternativa alcanza 2.560 líneas desde el final.

Los anuncios nativos pueden duplicar la voz; desactiva la lectura de progreso si hace falta. Informa de versiones de NVDA y navegador/aplicación, idioma, diagnóstico y pasos de reproducción. No necesitas compartir conversaciones privadas.

## Novedades y privacidad

0.1.3 mejora conversaciones largas e historiales con campos editables, actualiza el texto al repetir y conserva el estado al cambiar temporalmente el foco. Se reorganizó la documentación para usuarios y se actualizó el manifiesto con el repositorio y NVDA 2026.2 como mínimo.

No hace conexiones de red ni accede a contraseñas, cookies o portapapeles. Mantiene texto accesible temporalmente en memoria, sin guardarlo ni enviarlo. NVDA guarda los ajustes. No funciona en pantallas seguras.

GNU GPL versión 2 o posterior, sin garantía. Proyecto independiente, sin afiliación con OpenAI ni NV Access. Interfaz y ayuda en inglés, portugués brasileño, español, francés e italiano.
