import threading
import time
from datetime import datetime, timedelta
from collections import defaultdict
from database import DataBaseManager
import requests
from zoneinfo import ZoneInfo

class Reminder:
    def __init__(self):
        """
        Inicializa la clase Reminder
        
        Args:
            database_manager: Instancia de DataBaseManager
        """
        self.my_db = DataBaseManager()
        self.service_url = "https://medical-zuhb.onrender.com/email?"
        self.timers = {} 
        self.zona = ZoneInfo("America/Costa_Rica")
        self.running = True
        
    def start_daily_reminder_system(self):
        """
        Inicia el sistema de recordatorios para el día actual
        """
        today = datetime.now(self.zona).strftime('%Y-%m-%d')
        print(f"Iniciando sistema de recordatorios para: {today}")
        
        # Obtener todos los recordatorios del día
        recordatorios_hoy = self.my_db.get_recordatorios_por_fecha(today)
        
        if not recordatorios_hoy:
            print("No hay recordatorios para hoy")
            return
        
        print(f"Encontrados {len(recordatorios_hoy)} recordatorios para hoy")
        
        # Dividir recordatorios en bloques de hora
        bloques_hora = self._dividir_en_bloques_hora(recordatorios_hoy)
        
        # Procesar cada bloque
        for hora_bloque, recordatorios_bloque in bloques_hora.items():
            self._procesar_bloque_hora(hora_bloque, recordatorios_bloque, today)
    
    def _dividir_en_bloques_hora(self, recordatorios):
        """
        Divide los recordatorios en bloques de una hora (00:00-23:00)
        
        Args:
            recordatorios: Lista de tuplas (hora, nombre, user_email)
            
        Returns:
            dict: Diccionario con bloques de hora como clave y lista de recordatorios como valor
        """
        bloques = defaultdict(list)
        
        for hora, nombre, user_email in recordatorios:
            try:
                # Convertir hora a objeto datetime para facilitar el manejo
                hora_obj = datetime.strptime(hora, '%H:%M').time()
                # Obtener la hora del bloque (ej: 10:25 -> bloque 10)
                bloque_hora = hora_obj.hour
                
                bloques[bloque_hora].append({
                    'hora': hora,
                    'nombre': nombre,
                    'user_email': user_email,
                    'hora_obj': hora_obj
                })
            except ValueError as e:
                print(f"Error al procesar hora {hora}: {e}")
                continue
        
        return dict(bloques)
    
    def _procesar_bloque_hora(self, hora_bloque, recordatorios_bloque, fecha):
        """
        Procesa un bloque de hora específico
        
        Args:
            hora_bloque: Hora del bloque (0-23)
            recordatorios_bloque: Lista de recordatorios en ese bloque
            fecha: Fecha en formato ISO (YYYY-MM-DD)
        """
        print(f"\n--- Procesando bloque de hora {hora_bloque:02d}:00 ---")
        print(f"Recordatorios en este bloque: {len(recordatorios_bloque)}")
        
        # Ordenar recordatorios por hora
        recordatorios_ordenados = sorted(recordatorios_bloque, 
                                       key=lambda x: x['hora_obj'])
        
        for recordatorio in recordatorios_ordenados:
            if self.running:
                self._crear_temporizador_recordatorio(recordatorio, fecha)
    
    def _crear_temporizador_recordatorio(self, recordatorio, fecha):
        """
        Crea un temporizador para un recordatorio específico

        Args:
            recordatorio: Dict con datos del recordatorio
            fecha: Fecha en formato ISO (YYYY-MM-DD)
        """

        now = datetime.now(self.zona)
        print("Son actualmente las:", now.strftime("%Y-%m-%d %H:%M:%S"))

        hora_recordatorio = recordatorio['hora']  # Ej: "15:30"

        try:
            # Parsear hora del recordatorio
            hora = datetime.strptime(hora_recordatorio, "%H:%M").time()

            # Combinar fecha y hora, y asignar zona horaria correctamente
            fecha_hora_recordatorio = datetime.combine(
                datetime.strptime(fecha, "%Y-%m-%d").date(),
                hora,
                tzinfo=self.zona
            )

            # Calcular tiempo restante
            tiempo_restante = fecha_hora_recordatorio - now

            # Solo crear timer si el recordatorio es en el futuro
            if tiempo_restante.total_seconds() > 0:
                segundos_restante = tiempo_restante.total_seconds()
                minutos_restante = int(segundos_restante / 60)

                print(f"Creando temporizador para '{recordatorio['nombre']}' a las {hora_recordatorio}")
                print(f"Tiempo restante: {minutos_restante} minutos")

                # Crear timer
                timer_key = f"{fecha}_{hora_recordatorio}_{recordatorio['nombre']}"
                timer = threading.Timer(
                    segundos_restante,
                    self._ejecutar_recordatorio,
                    args=(recordatorio, fecha, timer_key)
                )

                # Guardar referencia del timer
                self.timers[timer_key] = timer
                timer.start()
            else:
                print(f"Recordatorio '{recordatorio['nombre']}' a las {hora_recordatorio} ya pasó")

        except ValueError as e:
            print(f"Error al procesar tiempo del recordatorio: {e}")

    def _ejecutar_recordatorio(self, recordatorio, fecha, timer_key):
        """
        Ejecuta el recordatorio cuando el timer se activa
        
        Args:
            recordatorio: Dict con datos del recordatorio
            fecha: Fecha en formato ISO
            timer_key: Clave del timer para limpieza
        """
        requests.get(f"{self.service_url}tipo=recordatorio&nombre={recordatorio['nombre']}&hora={recordatorio['hora']}&correo={recordatorio['user_email']}")

        
        # Limpiar timer de la lista
        if timer_key in self.timers:
            del self.timers[timer_key]
    
    
    def stop_all_timers(self):
        """
        Detiene todos los timers activos
        """
        print("Deteniendo todos los timers...")
        self.running = False
        
        for timer_key, timer in self.timers.items():
            timer.cancel()
            print(f"Timer cancelado: {timer_key}")
        
        self.timers.clear()
        print("Todos los timers han sido detenidos")
    
    def get_active_timers_info(self):
        """
        Obtiene información sobre los timers activos
        
        Returns:
            dict: Información de timers activos
        """
        return {
            'total_timers': len(self.timers),
            'timer_keys': list(self.timers.keys()),
            'running': self.running
        }
    
    def restart_daily_system(self):
        """
        Reinicia el sistema de recordatorios del día
        """
        print("Reiniciando sistema de recordatorios...")
        self.stop_all_timers()
        time.sleep(1)  # Esperar un segundo antes de reiniciar
        self.running = True
        self.start_daily_reminder_system()


# Ejemplo de uso:


# Para detener todos los timers (opcional)
# reminder_system.stop_all_timers()

# Para reiniciar el sistema (opcional)
# reminder_system.restart_daily_system()

# Para obtener info de timers activos
# info = reminder_system.get_active_timers_info()
# print(info)
