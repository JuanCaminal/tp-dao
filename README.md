script BD

BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Habitacion" (
	"Numero"	INTEGER,
	"Tipo"	TEXT NOT NULL,
	"Estado"	TEXT NOT NULL CHECK("Estado" IN ('disponible', 'ocupada')),
	"Precio_por_noche"	REAL NOT NULL,
	PRIMARY KEY("Numero")
);
CREATE TABLE IF NOT EXISTS "Cliente" (
	"ID_Cliente"	INTEGER,
	"Nombre"	TEXT NOT NULL,
	"Apellido"	TEXT NOT NULL,
	"Direccion"	TEXT,
	"Telefono"	TEXT,
	"Email"	TEXT,
	PRIMARY KEY("ID_Cliente" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Reserva" (
	"ID_Reserva"	INTEGER,
	"ID_Cliente"	INTEGER NOT NULL,
	"Numero_Habitacion"	INTEGER NOT NULL,
	"Fecha_Entrada"	DATE NOT NULL,
	"Fecha_Salida"	DATE NOT NULL,
	"Cantidad_Personas"	INTEGER NOT NULL,
	PRIMARY KEY("ID_Reserva" AUTOINCREMENT),
	FOREIGN KEY("Numero_Habitacion") REFERENCES "Habitacion"("Numero"),
	FOREIGN KEY("ID_Cliente") REFERENCES "Cliente"("ID_Cliente")
);
CREATE TABLE IF NOT EXISTS "Factura" (
	"ID_Factura"	INTEGER,
	"ID_Cliente"	INTEGER NOT NULL,
	"ID_Reserva"	INTEGER NOT NULL,
	"Fecha_Emision"	DATE NOT NULL,
	"Total"	REAL NOT NULL,
	PRIMARY KEY("ID_Factura" AUTOINCREMENT),
	FOREIGN KEY("ID_Reserva") REFERENCES "Reserva"("ID_Reserva"),
	FOREIGN KEY("ID_Cliente") REFERENCES "Cliente"("ID_Cliente")
);
CREATE TABLE IF NOT EXISTS "Empleado" (
	"ID_Empleado"	INTEGER,
	"Nombre"	TEXT NOT NULL,
	"Apellido"	TEXT NOT NULL,
	"Cargo"	TEXT NOT NULL CHECK("Cargo" IN ('recepcionista', 'servicio de limpieza', 'otros')),
	"Sueldo"	REAL NOT NULL,
	PRIMARY KEY("ID_Empleado" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ServicioEmpleadoHabitacion" (
	"ID_Empleado"	INTEGER NOT NULL,
	"Numero_Habitacion"	INTEGER NOT NULL,
	"Fecha_Servicio"	DATE NOT NULL,
	PRIMARY KEY("ID_Empleado","Numero_Habitacion","Fecha_Servicio"),
	FOREIGN KEY("ID_Empleado") REFERENCES "Empleado"("ID_Empleado"),
	FOREIGN KEY("Numero_Habitacion") REFERENCES "Habitacion"("Numero")
);
COMMIT;
