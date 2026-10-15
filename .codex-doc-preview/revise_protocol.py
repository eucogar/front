from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement

path = Path(r'C:\Users\euco\Desktop\PROYECTO\front\deliverables\PROTOCOLO_Proyecto_Grado_2026_actualizado_con_evidencia.docx')
doc = Document(path)

replacements = {
    'Actualmente, la gestión  de ingreso y salida   motocicletas en la Universidad Popular del Cesar se lleva acabo de forma manual, mediante el registro visual de placas y la entrega de tickets físicos, frente a un flujo diario de entre 5.000 y 6.000 motocicletas. Esta situación genera congestión, tiempos de espera elevados, errores humanos en el registro y baja trazabilidad de la información. La propuesta contempla el desarrollo de un sistema destinado  a gestionar acceso de motocicletas mediante reconocimiento automático de placas con redes neuronales YOLO, que permita optimizar el control de ingreso y salida de motocicletas dentro del parqueadero del campus universitario. Para el desarrollo de la investigación se adopta un enfoque cuantitativo de tipo aplicado, con un diseño no experimental de campo, y la construcción del software se realiza mediante la metodología de desarrollo ágil Scrum en cinco fases: diagnóstico, diseño de la arquitectura, desarrollo e integración, pruebas y validación, y ajustes finales.':
        'El proyecto desarrolla un prototipo para apoyar el control de ingreso y salida de motocicletas en la Universidad Popular del Cesar mediante detección de placas con YOLO y un aplicativo web. El documento base describe un procedimiento manual y reporta un flujo diario estimado de 5.000 a 6.000 motocicletas; no se adjuntó un registro institucional para verificar esas cifras, por lo que son antecedentes por confirmar y no resultados medidos. El desarrollo se organiza con Scrum. Como evidencia disponible, el detector ajustado se evaluó sobre 101 imágenes del conjunto test reservado. La evaluación de campo, el OCR exacto y la comparación de tiempos y errores siguen pendientes de autorización y recolección de datos.',
    'La solución se soporta en un backend desarrollado con Microsoft.AspNetCore y el patrón Endpoint/REPR de Ardalis, persistencia de datos en SQL Server mediante Dapper, documentación de la API con Swagger, e infraestructura en la nube de Microsoft Azure. Se espera que el sistema reduzca de manera significativa los tiempos de ingreso y salida, disminuya los errores de registro y fortalezca la seguridad y trazabilidad institucional, validando estas metas mediante indicadores de precisión de reconocimiento, tiempos de atención y reducción de errores frente al procedimiento manual actual.':
        'La solución contempla un backend Microsoft ASP.NET Core con patrón Endpoint/REPR de Ardalis, persistencia prevista en SQL Server mediante Dapper y documentación con Swagger; Azure es la infraestructura propuesta. La evidencia reunida corresponde a un prototipo y una prueba temporal local del servicio de visión; no acredita despliegue en Azure ni una prueba integral sostenida entre interfaz, backend y base de datos. La reducción de tiempos y errores y cualquier mejora de seguridad son efectos esperados que requieren medición en un piloto autorizado.',
    'Actualmente, el proceso de control de acceso se realiza de forma manual mediante el registro visual de placas y la entrega de tiquetes físicos por parte del personal de vigilancia. Este procedimiento genera múltiples dificultades operativas: congestión vehicular, aumento en los tiempos de espera, errores humanos en el registro, pérdida de información, falta de trazabilidad y debilidades en la validación de la identidad del conductor.':
        'Según la descripción consignada en el protocolo, el control se realiza manualmente mediante observación de placas y tiquetes físicos. La congestión, los tiempos de espera, los errores y las pérdidas de información se plantean como problemas por medir; no se dispone de una línea base cuantitativa que establezca su frecuencia o magnitud.',
    'La Universidad Popular del Cesar presenta diariamente un alto flujo de estudiantes, docentes, personal administrativo y visitantes, donde el 70% utiliza la motocicleta como principal medio de transporte. Esta situación genera una alta demanda en los puntos de acceso vehicular, especialmente durante las horas pico de ingreso y salida académica.':
        'El borrador describe una demanda significativa en horas pico y afirma que el 70 % de la comunidad utiliza motocicleta. En la evidencia revisada no se encontró la fuente primaria, periodo ni método de cálculo de ese porcentaje. La afirmación debe verificarse con registros institucionales antes de presentarse como dato observado.',
    'Ante esta situación , se plantea la implementación de  un sistema inteligente basado en reconocimiento automático de placas mediante redes neuronales YOLO, que permita automatizar el ingreso y salida de motocicletas, reducir los tiempos de atención, mejorar la trazabilidad de los registros y fortalecer el control de acceso vehicular dentro de la Universidad Popular del Cesar.':
        'Ante esta situación, se desarrolla un prototipo basado en detección de placas con YOLO para apoyar el registro de ingreso y salida. La automatización, la reducción de tiempos y la mejora de trazabilidad son objetivos, no efectos confirmados mientras no se complete la evaluación operativa.',
    'La incorporación de un sistema automatizado mediante la identificación de placas  utilizando redes neuronales YOLO permitirá transformar este proceso en una solución más ágil, confiable y tecnológicamente robusta. Este tipo de sistemas de reconocimiento automático de placas vehiculares (ANPR), respaldados en YOLO han demostrado tener una excelente precisión en diversas condiciones climáticas, en ambientes de baja iluminación, o captura de la imagen de la matricula en condiciones diurnas o nocturnas [2].':
        'La detección de placas con YOLO ofrece una alternativa técnica que debe evaluarse en el contexto específico de la UPC. El desempeño en lluvia, baja iluminación, noche, distancia y cámaras del campus no está demostrado por el test disponible y deberá medirse con un protocolo que documente esas condiciones.',
    'La detección automática de matrículas reducirá considerablemente los tiempos de ingreso y salida, disminuirá la carga operativa del personal de vigilancia y mejorará la experiencia de los usuarios dentro de la institución.':
        'La detección automática podría reducir tareas de digitación y apoyar al operador; el efecto sobre tiempos de ingreso y salida y la experiencia de los usuarios requiere medición antes de afirmarse como resultado.',
    'Analizar la problemática actual del acceso vehicular en la Universidad Popular del Cesar, identificando sus principales impactos en la movilidad, la seguridad y la eficiencia operativa de la comunidad universitaria, mediante la revisión de registros históricos de ingreso y la realización de encuestas dirigidas a  estudiantes, docentes y administrativos.':
        'Caracterizar el control de acceso mediante revisión documental y observación autorizada; documentar la fuente y periodo de cualquier dato institucional usado como línea base. Las entrevistas sobre operación del aplicativo se dirigirán al personal de vigilancia autorizado. Los estudiantes no son operadores del sistema.',
    'Investigar tecnologías de reconocimiento automático de placas vehiculares, evaluando modelos de inteligencia artificial como YOLOv5, YOLOv8, YOLOv11 y otras variantes aplicables al contexto institucional, comparando su rendimiento en términos de precisión (mAP), velocidad de inferencia y requisitos computacionales para seleccionar el modelo más adecuado.':
        'Implementar y documentar el detector YOLOv8n ajustado y evaluar la localización de placas en un conjunto de prueba reservado, informando precisión, recall, mAP y configuración; diferenciar estos indicadores de la exactitud OCR.',
    'Diseñar la arquitectura tecnológica del sistema de reconocimiento automático de placas, así como la interfaz gráfica (GUI) y el panel administrativo para la gestión, monitoreo y consulta de los registros de acceso vehicular, adaptado a las necesidades operativas y de seguridad de la universidad.':
        'Diseñar la arquitectura del prototipo, la interfaz para operadores y los módulos de gestión de acceso, identificando por separado las integraciones que requieren verificación con el backend y la base de datos institucional.',
    'Desarrollar el sistema de acceso vehicular inteligente, integrando los componentes de software, hardware y visión artificial necesarios para su correcto funcionamiento, mediante pruebas unitarias y de integración sobre cada uno de los módulos':
        'Desarrollar el prototipo web y sus componentes de software y visión artificial, y documentar las pruebas funcionales e integrales ejecutadas con sus resultados y límites.',
    'Implementar el sistema en condiciones reales de operación, midiendo la reducción en los tiempos de ingreso, la precisión del reconocimiento de placas y la aprobación por parte  de los usuarios.':
        'Definir un protocolo para una eventual prueba piloto con operadores autorizados y, tras obtener las aprobaciones institucionales, medir OCR exacto, tiempos y errores frente al proceso manual. Esta actividad sigue propuesta y no se reporta como ejecutada.',
    'El diseño será no experimental de campo, ya que se observará la problemática en su entorno natural sin manipular variables externas, realizando la recolección de datos directamente dentro del campus universitario.':
        'La evaluación ejecutada del detector se realizó sobre imágenes etiquetadas, no mediante recolección en el campus. La observación de campo y la comparación operativa se harán solo si se obtiene autorización institucional y se aprueba el tratamiento de datos correspondiente.',
    'Hipótesis de investigación (Hi): la implementación de un sistema de acceso vehicular para motocicletas basado en reconocimiento automático de placas con redes neuronales YOLO reduce de manera significativa el tiempo promedio de ingreso y salida y los errores de registro en la Universidad Popular del Cesar.':
        'Hipótesis de investigación (Hi), pendiente de contraste: durante un piloto autorizado, el sistema reducirá el tiempo promedio de registro y la proporción de errores frente al procedimiento manual, medidos en observaciones comparables. La evidencia actual no permite aceptarla ni rechazarla.',
    'Hipótesis nula (H0): la implementación del sistema de reconocimiento automático de placas no presenta diferencias estadísticamente relevantes en el tiempo promedio de ingreso y salida ni en los errores de registro frente al procedimiento manual actual.':
        'Hipótesis nula (H0), pendiente de contraste: durante el piloto no habrá diferencias estadísticamente significativas entre el procedimiento manual y el sistema en tiempo de registro y proporción de errores. No se ha realizado la comparación necesaria.',
    'H1: el sistema alcanza una precisión de reconocimiento de placas igual o superior al 90 % en condiciones reales de operación.':
        'H1a, detector: la precisión de detección de cajas de placa será al menos 90 % en una evaluación definida. En el test disponible se reportó 95,6 %; esto respalda el umbral solo para ese conjunto y configuración, no para cámaras del campus. H1b, OCR: la coincidencia exacta del texto completo será al menos 90 % en una muestra independiente y representativa. Está pendiente porque el test carece de transcripciones y el piloto de dos fotos no permite estimarla.',
    'H2: el tiempo promedio de registro por motocicleta disminuye al menos un 50 % respecto al procedimiento manual.':
        'H2: el tiempo promedio de registro por motocicleta disminuirá al menos 50 % frente al proceso manual. Pendiente: se requieren muestras comparables y una definición común del inicio y fin del cronometraje.',
    'H3: la tasa de errores de digitación en el registro de placas se reduce en más del 80 % frente al registro manual.':
        'H3: la proporción de registros con error disminuirá más de 80 % frente al proceso manual. Pendiente: se deben definir los errores, verificar la placa verdadera y recolectar datos de ambos procesos.',
    'La población estará conformada por estudiantes, docentes, personal administrativo y visitantes que ingresan motocicletas al campus universitario.':
        'Para el piloto futuro, la unidad de análisis será cada movimiento de ingreso o salida de motocicleta en un periodo y porterías definidos. Estudiantes, docentes, personal administrativo y visitantes son usuarios del acceso, no la unidad muestral si se estudian movimientos. El total poblacional debe obtenerse de registros institucionales del periodo. El personal operador constituye un grupo aparte para entrevistas.',
    'La muestra estará representada por los usuarios frecuentes del acceso vehicular durante jornadas académicas de alta circulación el flujo diario de motocicletas que ingresan al campus de la Universidad Popular del Cesar, estimado entre 5.000 y 6.000 ingresos por día, junto con el personal de vigilancia asignado a las porterías, responsable de operar el procedimiento de registro.':
        'El borrador consigna 5.000–6.000 ingresos diarios, pero no se adjuntó fuente institucional que verifique ese flujo. No se tratará como población observada. La muestra de campo aún no se ha recolectado. El número de guardas operadores elegibles deberá confirmarse con la institución.',
    'Para el componente cuantitativo se toma como referencia un promedio de 5.500 ingresos diarios (N = 5.500). El tamaño de la muestra se calcula con la fórmula para poblaciones finitas, con un nivel de confianza del 95 % (Z = 1,96), una proporción esperada p = 0,5 (máxima varianza, al no existir estudios previos en la institución) y un margen de error del 5 %:':
        'Cálculo preliminar, no muestra ejecutada: si un registro institucional confirma N = 5.500 movimientos en el periodo de referencia y la unidad es cada movimiento, con 95 % de confianza, p = 0,5 y error e = 5 %, la fórmula para población finita produce aproximadamente n = 359. N, periodo, unidad, independencia de observaciones y marco muestral deben verificarse antes de usar este tamaño. Si N no se confirma, se recalculará n.',
    'En consecuencia, la muestra estará conformada por 359 registros de ingreso y salida de motocicletas. El criterio de selección corresponde a un muestreo probabilístico aleatorio estratificado por franjas horarias, distribuyendo los registros entre las horas de mayor circulación (6:00–9:00, 11:00–14:00 y 17:00–20:00) y las de menor afluencia, de modo que la muestra refleje el comportamiento real del acceso durante la jornada académica.':
        'Los 359 registros son una muestra objetivo de planificación, no datos recolectados. El muestreo estratificado por franja solo se aplicará si existe un marco muestral o procedimiento reproducible y se conoce el flujo por portería y horario. Debe definirse si se observan ingresos, salidas o movimientos y controlar observaciones repetidas del mismo vehículo.',
    'Para el componente cualitativo se aplica un muestreo no probabilístico intencional: se entrevistará a la totalidad del personal de vigilancia que opera las porterías, al ser los informantes clave que conocen directamente el procedimiento actual de control de acceso.':
        'Para el componente cualitativo se propone un muestreo intencional del personal operador. El número y disponibilidad se confirmarán con la institución; no se afirma que se haya entrevistado a todo el personal.',
    'El desarrollo del proyecto se organiza mediante la metodología ágil Scrum, en cinco fases iterativas alineadas con el cronograma de actividades y los objetivos específicos del proyecto:':
        'El prototipo se organizó con Scrum en cinco fases. El cronograma de marzo a julio de 2026 fue la planificación inicial; léase junto con el estado real de cada actividad y no como evidencia de que todas se completaron en esas fechas:',
    'Fase 1. Diagnóstico y levantamiento de información (marzo): corresponde al primer Sprint y responde al objetivo de analizar la problemática actual del acceso vehicular. Incluye la observación directa del proceso manual de registro en las porterías, la aplicación de encuestas y entrevistas al personal de vigilancia, y la cuantificación del flujo diario de motocicletas (entre 5.000 y 6.000 ingresos por día), lo cual define la línea base de tiempos y errores frente a la cual se medirá el desempeño del software.':
        'Fase 1. Diagnóstico y levantamiento: la caracterización del borrador requiere respaldarse con actas, formatos de observación, entrevistas autorizadas y registros de afluencia. No se adjuntó evidencia de encuestas, tiempos, errores o flujo diario; esta línea base está pendiente de verificación.',
    'Fase 2. Diseño de la arquitectura del sistema (marzo): responde al objetivo de diseñar la arquitectura tecnológica, la interfaz gráfica y el panel administrativo. En este Sprint se define la arquitectura backend bajo el patrón Endpoint/REPR con Ardalis sobre Microsoft.AspNetCore, el modelo de datos en SQL Server, y el diseño de la interfaz de captura y validación de placas mediante el modelo YOLO.':
        'Fase 2. Diseño de arquitectura: el protocolo describe frontend React, API ASP.NET Core, SQL Server y servicio de visión. La configuración de endpoints, autenticación, conexión a base de datos y despliegue debe verificarse con pruebas de integración; listar tecnologías no prueba que el flujo completo opere.',
    'Fase 3. Desarrollo e integración del sistema (abril–mayo): responde al objetivo de desarrollar el sistema de acceso vehicular inteligente. Comprende la implementación de los endpoints de la API, la integración de AutoMapper entre los modelos de dominio y los DTOs, la persistencia de datos con Dapper sobre SQL Server, la documentación de la API con Swagger y la integración del modelo YOLO para el reconocimiento automático de placas. Cada componente se valida mediante pruebas unitarias e de integración al cierre del Sprint.':
        'Fase 3. Desarrollo e integración: se cuenta con un prototipo frontend, API backend y servicio de visión; hay evidencia de un smoke test local del servicio, pero no de un ciclo integral sostenido desde la interfaz hasta persistencia y consulta en SQL Server. Enumérense pruebas unitarias e integrales solo cuando existan sus reportes.',
    'El análisis distingue los resultados técnicos ya obtenidos de las mediciones de campo que siguen pendientes. La evaluación ejecutada del detector se presenta a continuación; las metas operativas del campus solo podrán contrastarse cuando se complete el piloto autorizado y se recolecten sus datos.':
        'El análisis separa detección de cajas, lectura OCR exacta, integración técnica y operación en campo. Solo la detección tiene métricas sobre test reservado. El smoke test local no demuestra persistencia en SQL ni disponibilidad de producción. Las metas del campus siguen pendientes.',
    'Desempeño del detector (relacionado con H1): la meta propuesta es alcanzar al menos 90 % de precisión en condiciones reales. El test técnico ejecutado mide cajas de detección y se informa por separado; no acredita por sí solo la meta de lectura exacta de caracteres ni el rendimiento en el campus.':
        'Desempeño del detector (H1a): el test reservado obtuvo precisión de detección de 95,6 %. Corresponde a cajas de placa y respalda el umbral propuesto solo para ese conjunto; no acredita OCR exacto ni generalización al campus. H1b requiere coincidencia exacta del texto por placa en imágenes con verdad-terreno verificada.',
    'Percepción del personal operador: se analizarán entrevistas al personal de vigilancia que utilizará el aplicativo. Los estudiantes no operan el sistema; cualquier encuesta a estudiantes debe limitarse a su experiencia como usuarios del acceso, si se conserva ese objetivo de investigación.':
        'Percepción del operador: no se adjuntaron entrevistas ni pruebas de usabilidad. En una evaluación futura participará personal operador autorizado. Los estudiantes no operan el aplicativo y no se les atribuirán resultados de usabilidad del panel.',
    'La discusión reportará por separado la localización de placas en el conjunto test, la lectura OCR exacta y el desempeño operativo en campo. No se afirmará reducción de tiempos, errores o congestión hasta medirlos con datos comparables y una muestra de campo documentada.':
        'La discusión reporta la localización de placas en test y el OCR exploratorio por separado. No hay evidencia para afirmar exactitud OCR general, reducción de tiempos o errores, disminución de congestión ni desempeño de cámaras del campus. Esos resultados requieren datos comparables, autorización institucional aplicable y un plan de muestreo documentado.',
    'Lectura OCR: en una prueba exploratoria previa de dos fotografías se obtuvieron 0/2 lecturas exactas (0/10 repeticiones). Esta prueba corresponde al flujo OCR inicial, no al test del detector ajustado, y no permite estimar el desempeño general del OCR. Se requiere validarlo con placas etiquetadas con su texto real.':
        'Prueba OCR exploratoria: dos fotografías distintas produjeron 0/2 coincidencias exactas; las diez ejecuciones (0/10) son repeticiones de esas mismas dos imágenes, no diez casos independientes. El resultado describe ese piloto pequeño y no estima el desempeño general del OCR ni del detector ajustado.',
    'La captura del aplicativo muestra el mensaje “Entrada registrada exitosamente” en la interfaz del operador. La imagen documenta la respuesta visual del prototipo; por sí sola no verifica la persistencia en la base de datos ni sustituye una prueba de campo.':
        'La captura documenta el mensaje visual de registro exitoso en la interfaz. Por sí sola no prueba persistencia correcta en SQL Server, lectura OCR correcta, autorización del usuario ni operación en el campus.',
    'Construir un conjunto de prueba OCR con transcripciones verificadas y placas distintas de las usadas para ajustar el modelo; reportar coincidencia exacta por placa y tasa de error por carácter, además de conservar la matriz de confusión del detector.':
        'Construir un conjunto OCR independiente con transcripciones verificadas; informar coincidencia exacta por placa, error por carácter y número de casos. Para el detector, conservar predicciones por imagen, umbrales y matriz de confusión con conteos enteros TP, FP y FN.',
    'Realizar el piloto únicamente con operadores autorizados y, antes de usar cámaras en el campus, gestionar la autorización institucional y definir información, retención y acceso conforme a las reglas de protección de datos.':
        'Antes de capturar imágenes en campus, solicitar autorización institucional y definir con el responsable de datos la finalidad, aviso, minimización, acceso, seguridad, retención, eliminación y atención de solicitudes. Limitar cualquier piloto a operadores autorizados.',
    'Medir latencia integral desde la captura hasta la respuesta del aplicativo por separado del tiempo de inferencia del modelo; registrar dispositivo, condiciones de luz, distancia y fallos de lectura.':
        'Medir latencia de captura, detector, OCR, API y respuesta completa; registrar dispositivo/GPU, resolución, luz, distancia, ángulo, conectividad y fallos, e informar p50/p95. Los milisegundos del detector no son tiempo de atención.',
    'Completar la comparación de tiempos y errores entre el proceso manual y el automatizado con la muestra de campo definida en la metodología. No presentar como resultados obtenidos los valores proyectados hasta terminar esa medición.':
        'Verificar N, periodo y unidad de análisis con fuente institucional; recalcular muestra y aprobar la selección por portería y horario. Comparar tiempos y errores con criterios idénticos, incluir fallos y no presentar metas o cálculos de planificación como resultados.',
}

changed = 0
for p in doc.paragraphs:
    old = p.text.strip()
    if old in replacements:
        p.text = replacements[old]
        changed += 1
    elif p.text.startswith('The fine-tuned YOLOv8n detector was evaluated'):
        p.text = 'As available technical evidence, the fine-tuned YOLOv8n detector was evaluated on the reserved 101-image test split. The reported metrics measure plate-box localization, not exact OCR transcription or performance on campus cameras. Field evaluation and comparisons of access time and recording errors remain pending.'
    elif p.text.startswith('n = (N · Z² · p · q)'):
        p.text = 'n = (N · Z² · p · q) / (e² · (N – 1) + Z² · p · q). Con N = 5.500, Z = 1,96, p = q = 0,5 y e = 0,05, n ≈ 359. El cálculo está condicionado a confirmar N y la unidad de muestreo; es una meta de planificación, no una muestra recolectada.'
    elif p.text.startswith('Variable independiente: sistema de reconocimiento automático'):
        p.text = 'Variable independiente: uso del prototipo de acceso vehicular. Indicadores técnicos separados: precisión, recall y mAP para cajas de placa; coincidencia exacta y error por carácter para OCR; latencia por etapa y completa. Instrumentos: reporte de evaluación, conjunto etiquetado, logs y formatos de prueba.'
    elif p.text.startswith('Variable dependiente: eficiencia del control de acceso vehicular'):
        p.text = 'Variables dependientes del piloto futuro: tiempo por movimiento, proporción de registros con error y porcentaje de movimientos trazables. Instrumentos: cronometraje uniforme, auditoría frente a verdad-terreno y consulta de registros. La percepción del operador se analizará por separado. Estas variables no tienen resultados en la evidencia disponible.'
    elif p.text.startswith('Registros de tiempos de ingreso y salida:'):
        p.text = 'Registros de tiempos (piloto futuro): presentar n, media, mediana, desviación estándar e intervalos/percentiles por proceso y franja. Definir observaciones emparejadas o independientes; elegir prueba según diseño y supuestos, e informar diferencia e intervalo de confianza con α = 0,05. No contrastar hipótesis sin datos y protocolo aprobado.'
    elif p.text.startswith('Desempeño del reconocimiento de placas:'):
        p.text = 'Detección: reportar precisión, recall y mAP con versión del modelo, umbrales, IoU y split; añadir TP/FP/FN enteros a partir de predicciones por imagen si se conservan. OCR: medir coincidencia exacta y error por carácter sobre verdad-terreno textual independiente; mAP no mide transcripción.'
    elif p.text.startswith('Errores de registro:'):
        p.text = 'Errores de registro (piloto futuro): definir previamente el error y comparar proporciones con el método adecuado al diseño y tamaño de muestra; informar conteos, tamaño de efecto e intervalo de confianza. Los datos siguen pendientes.'

# User-confirmed scope: technical prototype only, without an institutional field pilot.
for p in doc.paragraphs:
    s = p.text.strip()
    if s.startswith('Resumen –'):
        p.text = 'Resumen – El proyecto desarrolla un prototipo web para apoyar el control de ingreso y salida de motocicletas en la Universidad Popular del Cesar mediante detección de placas con YOLO. El alcance de esta versión es técnico y no incluye un piloto de campo. El documento base menciona un flujo de 5.000 a 6.000 motocicletas por día; como no se dispone de fuente institucional, esa cifra queda pendiente de verificación y no se usa para calcular una muestra. El detector YOLOv8n ajustado se evaluó en el split test reservado de un conjunto externo: 101 imágenes, con 67 placas anotadas y 34 imágenes de fondo. Se reportan precisión de detección de 95,6 %, recall de 96,8 %, mAP@50 de 99,0 % y mAP@50–95 de 88,8 %. Estas métricas miden localización de cajas, no transcripción OCR. La evaluación OCR exacta, la integración completa frontend–backend–SQL y el despliegue institucional no se consideran demostrados por la evidencia disponible.'
    elif s.startswith('Abstract –'):
        p.text = 'The project develops a web prototype to support motorcycle access control at Universidad Popular del Cesar using YOLO plate detection. This version has a technical scope and does not include a campus field pilot. The draft mentions 5,000–6,000 motorcycles per day, but no institutional source was provided; the figure remains unverified and is not used to calculate a study sample. The fine-tuned YOLOv8n detector was evaluated on the reserved test split of an external dataset: 101 images, including 67 annotated plates and 34 background images. It achieved 95.6% detection precision, 96.8% recall, 99.0% mAP@50, and 88.8% mAP@50–95. These metrics measure box localization, not OCR transcription. Exact OCR evaluation, end-to-end frontend–backend–SQL integration, and institutional deployment are not established by the available evidence.'
    elif s.startswith('The solution is built on a backend'):
        p.text = 'The prototype uses a backend developed with Microsoft ASP.NET Core and the Ardalis Endpoint/REPR pattern, with SQL Server persistence via Dapper and API documentation through Swagger. Azure is a proposed deployment option, not a verified deployment. The available evidence includes a temporary local vision-service test; it does not establish sustained end-to-end operation among the interface, API, and database.'
    elif s.startswith('The system is expected to significantly reduce entry'):
        p.text = 'Reductions in access time and recording errors, along with improvements in security and traceability, are potential benefits for future evaluation. They are outside the measured results and outside the field scope of this technical prototype.'
    elif s.startswith('El presente proyecto implementa un enfoque metodológico'):
        p.text = 'El proyecto es aplicado y de desarrollo tecnológico. Esta versión comprende la construcción del prototipo y su evaluación técnica con imágenes etiquetadas; no incluye piloto ni recolección de datos en el campus.'
    elif s.startswith('Finalmente, la implementación piloto dentro del entorno universitario'):
        p.text = 'Una eventual evaluación en el entorno universitario sería una etapa posterior e independiente, sujeta a autorización institucional, protocolo de datos y recursos. No hace parte de los resultados ni entregables medidos en esta versión.'
    elif s.startswith('Hipótesis de investigación (Hi), pendiente de contraste:'):
        p.text = 'Hipótesis de investigación (Hi), criterio técnico: la precisión de detección de cajas de placa del YOLOv8n ajustado será igual o superior al 90 % en el split test reservado. El resultado de 95,6 % supera ese umbral en el conjunto evaluado; no se generaliza al campus ni a OCR.'
    elif s.startswith('Hipótesis nula (H0), pendiente de contraste:'):
        p.text = 'Hipótesis nula (H0), criterio técnico: la precisión de detección de cajas de placa del modelo en el split test reservado será inferior al 90 %. El reporte disponible no respalda H0 para ese test; esta comparación descriptiva no equivale a una prueba de significancia ni a inferencia sobre cámaras del campus.'
    elif s == 'Se utilizarán las siguientes técnicas:':
        p.text = 'Para la evaluación técnica se utilizan las siguientes técnicas:'
    elif s == 'Observación directa del proceso actual de acceso vehicular':
        p.text = 'Evaluación del split test etiquetado del conjunto de imágenes externo'
    elif s == 'Entrevistas al personal de vigilancia':
        p.text = 'Pruebas funcionales del prototipo en entorno local'
    elif s == 'Registro de tiempos de ingreso y salida':
        p.text = 'Revisión de reportes técnicos y logs disponibles'
    elif s == 'Los instrumentos utilizados serán:':
        p.text = 'Los instrumentos de evaluación técnica son:'
    elif s == 'Formatos de observación':
        p.text = 'Dataset con anotaciones del split test y reporte de métricas'
    elif s == 'Guías de entrevista':
        p.text = 'Registro de configuración del modelo y entorno de ejecución'
    elif s == 'Registros de tiempos operativos':
        p.text = 'Reportes del servicio de visión y pruebas locales disponibles'
    elif s.startswith('Entrevistas al personal de vigilancia:'):
        p.text = 'Entrevistas y encuestas: no se aplicaron en esta versión del prototipo y no se presentan resultados cualitativos.'
    elif s.startswith('El procesamiento se realizará con Microsoft Excel'):
        p.text = 'Las métricas del detector se procesaron con el reporte técnico exportado por Ultralytics y se presentan descriptivamente. No se aplicaron pruebas inferenciales a tiempos, errores o percepción porque no se recolectaron esas variables.'
    elif s.startswith('El sistema será desarrollado mediante tecnologías orientadas'):
        p.text = 'El prototipo web integra una interfaz para el operador, componentes backend, persistencia prevista y un servicio de visión. La disponibilidad de cada integración debe leerse conforme a sus pruebas documentadas; no se afirma operación institucional.'
    elif s.startswith('Para la validación del modelo se realizarán pruebas funcionales'):
        p.text = 'La evaluación ejecutada reporta métricas de detección en imágenes reservadas para test y pruebas locales de software disponibles. OCR exacto, cámaras del campus, tiempos de atención y reducción de errores no fueron medidos en esta versión.'
    elif s.startswith('Asimismo, se emplearán métricas de evaluación propias'):
        p.text = 'En la evaluación técnica se reportaron precisión, recall y mAP para detección de objetos sobre el split test. Estas métricas describen localización de placas; no miden lectura OCR exacta ni desempeño en condiciones reales del campus.'
    elif s.startswith('Desde el enfoque tecnológico, el uso de modelos de visión artificial como YOLO representa'):
        p.text = 'Desde el enfoque tecnológico, YOLO permite explorar la detección de objetos en imágenes. Velocidad y precisión dependen del modelo, hardware y condiciones de captura; las métricas de este proyecto se limitan al conjunto test y no acreditan operación en cámaras del campus.'
    elif s.startswith('La presente investigación se desarrollará bajo un enfoque cuantitativo'):
        p.text = 'La investigación es aplicada y de desarrollo tecnológico. El alcance de esta versión es la construcción del prototipo y su evaluación técnica con un conjunto de imágenes etiquetadas; no contempla un piloto dentro del campus.'
    elif s.startswith('El diseño metodológico corresponde a un proyecto de desarrollo tecnológico'):
        p.text = 'El diseño corresponde a desarrollo tecnológico con evaluación cuantitativa retrospectiva del split test reservado para detección. No se realizó intervención ni recolección de movimientos vehiculares en el campus.'
    elif s.startswith('Se adopta un enfoque cuantitativo porque'):
        p.text = 'El componente cuantitativo ejecutado analiza métricas de localización de cajas de placa en imágenes de prueba. Tiempos de acceso, errores operativos, usabilidad y efectos sobre la seguridad no se midieron y quedan fuera del alcance actual.'
    elif s.startswith('Objetivo general'):
        pass
    elif s.startswith('Implementar un sistema de acceso vehicular mediante el reconocimiento de placas'):
        p.text = 'Desarrollar y evaluar técnicamente un prototipo de acceso vehicular para motocicletas mediante detección de placas con redes neuronales YOLO, utilizando un conjunto de prueba reservado y delimitando sus resultados al entorno evaluado.'
    elif s.startswith('H1a, detector:'):
        p.text = 'H1, detector: en el split test reservado, la precisión de detección de cajas de placa será igual o superior al 90 %. Resultado observado: 95,6 % en el reporte disponible. Este criterio se refiere únicamente al conjunto y a la configuración de evaluación descritos; no demuestra desempeño en campus. La exactitud OCR no forma parte de esta hipótesis porque no existe verdad-terreno textual para el test.'
    elif s.startswith('H2: el tiempo promedio de registro'):
        p.text = 'H2, fuera del alcance de esta versión: no se plantea contrastar reducción de tiempos porque no se realizará un piloto de campo ni se recolectará una línea base.'
    elif s.startswith('H3: la proporción de registros'):
        p.text = 'H3, fuera del alcance de esta versión: no se plantea contrastar reducción de errores operativos porque no se realizará un piloto ni existe una muestra de movimientos de campus.'
    elif s.startswith('Para el piloto futuro, la unidad de análisis'):
        p.text = 'La unidad de análisis de la evaluación técnica es la imagen del split test reservado del dataset de placas versión 15. Se analizaron 101 imágenes: el reporte de métricas consigna 67 placas anotadas y 34 fondos. La muestra corresponde al benchmark de imágenes, no a movimientos, motociclistas ni usuarios de la UPC; no permite inferir desempeño en cámaras del campus. El dataset incluye imágenes de entrenamiento y validación separadas del test; únicamente el split test sustenta las métricas reportadas.'
    elif s.startswith('La población de vehículos y el flujo de ingreso al campus'):
        p.text = 'La población de vehículos y el flujo de ingreso al campus no se estiman en este estudio porque no se ejecuta trabajo de campo y no se aportó un registro institucional que sustente las cifras del borrador. Los 359 registros no constituyen una muestra de esta investigación y se eliminó su cálculo. Si un trabajo posterior realiza un piloto, deberá definir población, periodo, unidad, marco muestral y tamaño con datos verificables.'
    elif s.startswith('Cálculo preliminar, no muestra ejecutada:'):
        p.text = 'No aplica cálculo de muestra de movimientos vehiculares en esta versión: no se recolectan datos de acceso en el campus. La muestra de evaluación técnica ya definida corresponde a 101 imágenes del split test reservado.'
    elif s.startswith('n = (N · Z² · p · q)'):
        p.text = 'No se aplica fórmula de población finita a este benchmark. El tamaño evaluado es n = 101 imágenes del split test reservado del dataset externo; las métricas describen dicho conjunto y no una población de movimientos vehiculares de la UPC.'
    elif s.startswith('Los 359 registros son una muestra objetivo'):
        p.text = 'No se seleccionó muestra de estudiantes, guardas, motocicletas ni movimientos del campus. El estudio actual no incluye encuestas, entrevistas ni muestreo estratificado por horas.'
    elif s.startswith('Para el componente cualitativo se propone'):
        p.text = 'No se desarrolló un componente cualitativo en esta versión: no se aplicaron entrevistas ni encuestas. La percepción de los operadores podría investigarse en una fase posterior, previa autorización institucional.'
    elif s.startswith('H2:') and 'tiempo promedio' in s:
        p.text = 'H2, fuera del alcance de esta versión: no se contrasta el tiempo de atención. La latencia de inferencia del detector no equivale al tiempo de ingreso o salida.'
    elif s.startswith('Variable dependiente:') or s.startswith('Variables dependientes del piloto futuro:'):
        p.text = 'Variables técnicas evaluadas: desempeño de detección de cajas de placa, medido con precisión, recall y mAP sobre el split test. El OCR exacto, el tiempo de acceso, la proporción de errores operativos y la usabilidad no se midieron en esta versión y no se presentan como variables con resultados.'
    elif s.startswith('Registros de tiempos (piloto futuro):'):
        p.text = 'Tiempos de acceso: fuera del análisis de esta versión, dado que no hay observaciones de campo. Los 4,93 ms informados corresponden a inferencia del modelo por imagen en la evaluación registrada, no al tiempo de captura, OCR, API, interfaz ni atención vehicular.'
    elif s.startswith('Errores de registro (piloto futuro):'):
        p.text = 'Errores operativos: no se analizaron porque no se recolectaron registros manuales ni automatizados de movimientos en el campus.'
    elif s.startswith('El prototipo se organizó con Scrum en cinco fases.'):
        p.text = 'El prototipo se organizó con Scrum en cinco fases. El cronograma de marzo a julio de 2026 fue la planificación inicial; la evaluación de esta versión es técnica y no incluye piloto de campo. Las fechas deben actualizarse con bitácoras o entregables verificables, no inferirse del plan original:'
    elif s.startswith('Fase 4. Pruebas y validación:'):
        p.text = 'Fase 4. Pruebas y validación: se evaluó técnicamente el detector YOLOv8n en el split test reservado (101 imágenes). La exactitud OCR general, la integración integral frontend–backend–SQL y el rendimiento en cámaras del campus no están demostrados por ese resultado.'
    elif s.startswith('Fase 5. Ajustes finales y documentación:'):
        p.text = 'Fase 5. Cierre técnico: documentar el test del detector, los límites del OCR y las evidencias disponibles de los componentes. Una evaluación con cámaras del campus y mediciones operativas sería una fase futura independiente que requeriría autorización y protocolo propios.'
    elif s.startswith('Tiempo de ingreso y salida (H2):'):
        p.text = 'Tiempo de atención: fuera del alcance medido. No se dispone de cronometrajes manuales ni automáticos; la latencia de inferencia por imagen no permite inferir reducción de tiempo de acceso.'
    elif s.startswith('Errores de registro (H3):'):
        p.text = 'Errores de registro: fuera del alcance medido. No hay registros comparables de proceso manual y prototipo para estimar tasas ni reducciones.'
    elif s.startswith('Percepción del operador:'):
        p.text = 'Percepción del usuario operador: no se realizaron encuestas, entrevistas ni pruebas de usabilidad en esta versión.'
    elif s.startswith('La discusión reporta la localización'):
        p.text = 'La discusión se limita a las métricas de detección de placas en el split test y a describir el pequeño smoke test OCR como exploratorio. No se afirman exactitud OCR general, reducción de tiempos o errores, congestión, aceptación de usuarios ni rendimiento en cámaras de campus. Esos asuntos requieren estudios posteriores con datos y permisos adecuados.'
    elif s.startswith('A partir de los resultados y límites documentados'):
        p.text = 'A partir de los resultados y límites documentados, se recomiendan estas mejoras técnicas y posibles líneas futuras:'
    elif s.startswith('Ejecutar una prueba integral reproducible:'):
        p.text = 'Completar, en entorno de desarrollo, una prueba integral reproducible: autenticación, captura/carga, respuesta del detector y OCR, confirmación del operador, endpoint, persistencia SQL y consulta posterior. Registrar versiones, entrada, resultado esperado/obtenido y evidencia. Esta prueba técnica no requiere ni sustituye un piloto de campus.'
    elif s.startswith('Antes de capturar imágenes en campus'):
        p.text = 'Como trabajo futuro separado, cualquier captura de imágenes o prueba en campus requerirá autorización institucional y definición previa de finalidad, aviso, minimización, acceso, seguridad, retención, eliminación y atención de solicitudes por el responsable de datos.'

# The test-set result is not a campus field sample; remove the obsolete n=359 wording from phase 4.

# Add reproducible integration and manual-fallback recommendation.
heading = next(p for p in doc.paragraphs if p.text.strip() == '3.5 RECOMENDACIONES')
extra = doc.add_paragraph('Ejecutar una prueba integral reproducible: autenticación, captura o carga de imagen, respuesta del detector/OCR, confirmación del operador, endpoint de movimiento, persistencia SQL y consulta posterior. Registrar versiones, caso esperado/obtenido y evidencia; disponer de un registro manual ante lecturas ambiguas o indisponibilidad del servicio.')
heading._p.addnext(extra._p)

# Add evidence status table before the detailed detector metrics.
anchor = next(p for p in doc.paragraphs if p.text.strip() == 'Evaluación ejecutada del detector de placas')
status = doc.add_paragraph('Estado de evidencia por componente')
status.paragraph_format.page_break_before = True
status.paragraph_format.keep_with_next = True
for run in status.runs:
    run.bold = True
    run.font.size = Pt(12)
anchor._p.addprevious(status._p)
table = doc.add_table(rows=1, cols=2)
table.style = 'Table Grid'
table.rows[0].cells[0].text = 'Componente'
table.rows[0].cells[1].text = 'Estado documentado'
for left, right in [
    ('Detector', 'Test de 101 imágenes: P 95,6 %, R 96,8 %, mAP50 99,0 %, mAP50–95 88,8 %.'),
    ('OCR exacto', 'Exploratorio: 0/2 imágenes distintas; 0/10 repeticiones no independientes.'),
    ('Servicio de visión/API', 'Smoke test local disponible; no demuestra operación estable ni latencia integral.'),
    ('Frontend–backend–SQL', 'Sin evidencia adjunta de integración completa, persistencia y consulta de extremo a extremo.'),
    ('Prueba de campo y tiempos', 'Fuera del alcance actual; posible trabajo futuro sujeto a autorización.'),
    ('Azure', 'Infraestructura propuesta; no hay evidencia de despliegue ejecutado.'),
]:
    cells = table.add_row().cells
    cells[0].text = left
    cells[1].text = right
for row in table.rows:
    trpr = row._tr.get_or_add_trPr()
    trpr.append(OxmlElement('w:cantSplit'))
anchor._p.addprevious(table._tbl)

doc.core_properties.title = 'Protocolo de proyecto de grado con alcance y evidencia revisados'
doc.core_properties.subject = 'Alineación de objetivos, metodología y resultados con evidencia técnica disponible'
doc.save(path)
print(f'Saved {path}; replacements={changed}; paragraphs={len(doc.paragraphs)} tables={len(doc.tables)} bytes={path.stat().st_size}')
