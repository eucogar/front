export const previewUsers = [
  { identificacion: '1067890123', nombres: 'Valentina', apellidos: 'Mendoza Ríos', correo: 'valentina.mendoza@unicesar.edu.co', telefono: '300 555 0142', estado: true, rolId: 'd8aa16f9-77cb-4810-8e49-22932f2a9195', rolNombre: 'Estudiante' },
  { identificacion: '77012345', nombres: 'Carlos', apellidos: 'Pérez Gómez', correo: 'carlos.perez@unicesar.edu.co', telefono: '310 555 0188', estado: true, rolId: '32f3a61c-41c6-4acf-a769-dbf149277d8a', rolNombre: 'Administrador' },
  { identificacion: '1002345678', nombres: 'Mariana', apellidos: 'López Díaz', correo: 'mariana.lopez@unicesar.edu.co', telefono: '315 555 0160', estado: false, rolId: 'd8aa16f9-77cb-4810-8e49-22932f2a9195', rolNombre: 'Estudiante' },
];

export const previewRoles = [
  { rolId: '32f3a61c-41c6-4acf-a769-dbf149277d8a', rolNombre: 'Administrador', rolEstado: true, rolDescripcion: 'Administra las cuentas y supervisa el sistema.' },
  { rolId: 'd8aa16f9-77cb-4810-8e49-22932f2a9195', rolNombre: 'Estudiante', rolEstado: true, rolDescripcion: 'Usuario autorizado para ingresar al campus.' },
];

export const previewAccesses = [
  { identificacion: '1067890123', nombreCompleto: 'Valentina Mendoza Ríos', placa: 'KLM42F', fechaHoraEntrada: '2026-10-09T08:12:00', fechaHoraSalida: null, estadoAcceso: 'ENTRADA' },
  { identificacion: '77012345', nombreCompleto: 'Carlos Pérez Gómez', placa: 'ABC19D', fechaHoraEntrada: '2026-10-09T07:45:00', fechaHoraSalida: '2026-10-09T09:10:00', estadoAcceso: 'SALIDA' },
  { identificacion: '1002345678', nombreCompleto: 'Mariana López Díaz', placa: 'QRS83A', fechaHoraEntrada: '2026-10-08T16:20:00', fechaHoraSalida: '2026-10-08T18:03:00', estadoAcceso: 'SALIDA' },
];
