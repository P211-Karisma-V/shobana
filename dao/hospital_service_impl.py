# hospital_service_impl.py
from dao.ihospital_service  import IHospitalService
from entity.appointment import Appointment
from util import db_conn_util
from util.db_conn_util import DBConnection
from exception.custom_exceptions import PatientNumberNotFoundException


class HospitalServiceImpl(IHospitalService):

    def get_appointment_by_id(self, appointment_id):
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Appointment WHERE appointmentId = ?", (appointment_id,))
        row = cursor.fetchone()
        if row:
            appointment = Appointment(row[0], row[1], row[2], row[3], row[4])
            return appointment
        else:
            raise Exception("Appointment not found")

    def get_appointments_for_patient(self, patient_id):
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Appointment WHERE patientId = ?", (patient_id,))
        appointments = []
        for row in cursor.fetchall():
            appointment = Appointment(row[0], row[1], row[2], row[3], row[4])
            appointments.append(appointment)
        if not appointments:
            raise PatientNumberNotFoundException(patient_id)
        return appointments

    def get_appointments_for_doctor(self, doctor_id):
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Appointment WHERE doctorId = ?", (doctor_id,))
        appointments = []
        for row in cursor.fetchall():
            appointment = Appointment(row[0], row[1], row[2], row[3], row[4])
            appointments.append(appointment)
        return appointments

    def schedule_appointment(self, appointment):
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(appointmentId) FROM Appointment")
        max_id_row = cursor.fetchone()
        if max_id_row[0] is not None:
            next_id = max_id_row[0] + 1
        else:
            next_id = 1
        appointment.appointment_id = next_id
        cursor.execute(
            "INSERT INTO Appointment (appointmentId, patientId, doctorId, appointmentDate, description) VALUES (?, ?, ?, ?, ?)",
            (appointment.appointment_id, appointment.patient_id, appointment.doctor_id, appointment.appointment_date,
             appointment.description)
        )
        connection.commit()
        return True

    def update_appointment(self, appointment):
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Appointment SET patientId = ?, doctorId = ?, appointmentDate = ?, description = ? WHERE appointmentId = ?",
            (appointment.patient_id, appointment.doctor_id, appointment.appointment_date, appointment.description,
             appointment.appointment_id)
        )
        connection.commit()
        return True

    def cancel_appointment(self, appointment_id):
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Appointment WHERE appointmentId = ?", (appointment_id,))
        connection.commit()
        return True

