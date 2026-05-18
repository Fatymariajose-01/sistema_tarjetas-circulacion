INSERT INTO Usuario (nombre_usuario, contrasena, rol) VALUES
('admin_central', 'hash1234', 'Administrador'),
('operador_01', 'hash5678', 'Operador'),
('operador_02', 'hash9012', 'Operador'),
('supervisor_xela', 'hash3456', 'Supervisor'),
('auditor_ext', 'hash7890', 'Auditor');

-- Propietarios (Con formato DPI como id_propietario)
INSERT INTO Propietario (id_propietario, nombre, direccion) VALUES
('2548796320101', 'Juan Carlos Pérez', 'Zona 1, Ciudad de Guatemala'),
('3021458740901', 'María Fernanda López', 'Zona 3, Quetzaltenango'),
('1023654780101', 'Carlos Estrada', 'Zona 10, Mixco'),
('4012589630901', 'Ana Lucía Morales', 'Zona 5, Villa Nueva'),
('2036987410101', 'Luis Felipe García', 'Zona 1, Antigua Guatemala');

-- 5 Vehículos
INSERT INTO Vehiculo (placa, vin, numero_motor, marca, modelo, linea, color, anio) VALUES
('P-123ABC', '1HGCM82633A004', 'MTR-987654321', 'Toyota', 'Corolla', 'Sedan', 'Rojo', 2020),
('P-456DEF', '2T1BR32E94C012', 'MTR-123456789', 'Honda', 'Civic', 'Hatchback', 'Azul', 2018),
('P-789GHI', '3HWEA16584A123', 'MTR-456123789', 'Mazda', '3', 'Sedan', 'Gris', 2022),
('P-321JKL', '4S3BR29E94C555', 'MTR-789456123', 'Nissan', 'Sentra', 'Sedan', 'Blanco', 2015),
('P-654MNO', '5N1AL08023C999', 'MTR-321654987', 'Ford', 'Escape', 'SUV', 'Negro', 2021);

-- Tarjetas de Circulación Iniciales
INSERT INTO Tarjeta_Circulacion (placa, id_propietario, fecha_emision, fecha_vencimiento, estado) VALUES
('P-123ABC', '2548796320101', '2026-01-10', '2027-01-10', 'Activa'),
('P-456DEF', '3021458740901', '2026-02-15', '2027-02-15', 'Activa');

