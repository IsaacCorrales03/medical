       class CalendarApp {
    constructor() {
        this.currentDate = new Date();
        this.selectedDate = null;
        this.medications = {}; // Solo para cache temporal
        this.medicationDays = new Set(); // Solo para cache temporal
        this.init();
    }

    init() {
        this.loadAllMedications().then(() => {
            this.renderCalendar();
        });
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.getElementById('prevMonth').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.loadAllMedications().then(() => {
                this.renderCalendar();
            });
        });

        document.getElementById('nextMonth').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.loadAllMedications().then(() => {
                this.renderCalendar();
            });
        });

        document.getElementById('closePanelBtn').addEventListener('click', () => {
            this.closeDayPanel();
        });

        document.getElementById('addMedicationBtn').addEventListener('click', () => {
            this.addMedication();
        });
    }

    async loadAllMedications() {
        try {
            const userId = document.getElementById('id_paciente').value;
            
            const response = await fetch('/get_recordatorios', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    paciente_id: userId
                })
            });
            
            if (response.ok) {
                const recordatoriosData = await response.json();
                this.medications = {};
                this.medicationDays.clear();
                
                // Manejar el formato de tuplas: [('2025-05-26', '13:00', 'chambas'), ...]
                if (Array.isArray(recordatoriosData)) {
                    console.log(recordatoriosData)
                    recordatoriosData.forEach((tupla, index) => {
                        // tupla = [fecha, hora, nombre]
                        const fecha = tupla[0];  // '2025-05-26'
                        const hora = tupla[1];   // '13:00'
                        const nombre = tupla[2]; // 'chambas'
                        const id = tupla[3]
                        // Organizar medicamentos por fecha
                        if (!this.medications[fecha]) {
                            this.medications[fecha] = [];
                        }
                        
                        this.medications[fecha].push({
                            id: id, // Usar índice como ID temporal
                            nombre: nombre,
                            hora: hora
                        });
                        
                        this.medicationDays.add(fecha);
                    });
                }
            } else {
                console.error('Error al cargar medicamentos');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    renderCalendar() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        // Actualizar título del mes
        const monthNames = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
        document.getElementById('currentMonth').textContent = `${monthNames[month]} ${year}`;

        // Obtener primer día del mes y días en el mes
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        const calendarDays = document.getElementById('calendarDays');
        calendarDays.innerHTML = '';

        // Días vacíos al inicio
        for (let i = 0; i < firstDay; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day empty';
            calendarDays.appendChild(emptyDay);
        }

        // Días del mes
        const today = new Date();
        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.textContent = day;
            
            // Crear fecha para este día
            const dayDate = new Date(year, month, day);
            const dateKey = this.getDateKey(dayDate);
            
            // Marcar día actual
            if (year === today.getFullYear() && 
                month === today.getMonth() && 
                day === today.getDate()) {
                dayElement.classList.add('current-day');
            }

            // EVALUAR SI LA FECHA COINCIDE CON RECORDATORIOS Y APLICAR BORDE ROJO
            if (this.medicationDays.has(dateKey)) {
                dayElement.classList.add('has-medications');
                // Aplicar borde rojo cuando hay recordatorios
                dayElement.style.border = '2px solid red';
                dayElement.style.borderRadius = '4px';
            }

            // Agregar evento click
            dayElement.addEventListener('click', () => {
                this.selectDay(year, month, day);
            });

            calendarDays.appendChild(dayElement);
        }
    }

    selectDay(year, month, day) {
        // Remover selección anterior
        document.querySelectorAll('.selected-day').forEach(el => {
            el.classList.remove('selected-day');
        });

        // Marcar día seleccionado
        event.target.classList.add('selected-day');
        
        this.selectedDate = new Date(year, month, day);
        
        // Imprimir la fecha en formato ISO
        const fechaISO = this.getDateKey(this.selectedDate);
        console.log('Fecha seleccionada (ISO):', fechaISO);
        
        this.showDayPanel();
    }

    showDayPanel() {
        const panel = document.getElementById('dayPanel');
        const title = document.getElementById('selectedDayTitle');
        
        const dayNames = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
        const monthNames = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
        
        const dayName = dayNames[this.selectedDate.getDay()];
        const day = this.selectedDate.getDate();
        const monthName = monthNames[this.selectedDate.getMonth()];
        
        title.textContent = `${dayName} ${day} de ${monthName}`;
        
        this.loadDayMedications();
        panel.classList.remove('hidden');
        panel.classList.add('show');
    }

    closeDayPanel() {
        const panel = document.getElementById('dayPanel');
        panel.classList.remove('show');
        panel.classList.add('hidden');
        
        // Remover selección
        document.querySelectorAll('.selected-day').forEach(el => {
            el.classList.remove('selected-day');
        });
        
        this.selectedDate = null;
    }

    loadDayMedications() {
        const dateKey = this.getDateKey(this.selectedDate);
        const medications = this.medications[dateKey] || [];
        
        const medicationsList = document.getElementById('medicationsList');
        medicationsList.innerHTML = '';
        
        if (medications.length === 0) {
            medicationsList.innerHTML = '<p class="text-gray-500 text-sm">No hay medicamentos programados para este día.</p>';
        } else {
            medications.forEach((med) => {
                console.log(med)
                const medElement = document.createElement('div');
                medElement.className = 'medication-item flex items-center justify-between p-3 border rounded-lg';
                medElement.innerHTML = `
                    <div>
                        <div class="font-medium text-gray-800">${med.nombre}</div>
                        <div class="text-sm text-gray-500">${med.hora}</div>
                    </div>
                    <button onclick="calendar.removeMedication(${med.id})" 
                            class="text-red-500 hover:text-red-700 p-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                        </svg>
                    </button>
                `;
                medicationsList.appendChild(medElement);
            });
        }
    }

    async addMedication() {
        const nameInput = document.getElementById('medicationName');
        const timeInput = document.getElementById('medicationTime');

        const id_paciente = document.getElementById('id_paciente').value;
        const user_email = document.getElementById('user_email').value;
        const nombre = nameInput.value.trim();
        const hora = timeInput.value;
        
        if (!nombre || !hora) {
            alert('Por favor, completa todos los campos.');
            return;
        }
        
        const fecha = this.getDateKey(this.selectedDate);
        
        try {
            const response = await fetch('/add_recordatorio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    paciente_id: id_paciente,
                    user_email: user_email,
                    dia: fecha,
                    hora: hora,
                    nombre: nombre
                })
            });
            
            if (response.ok) {
                // Limpiar formulario
                nameInput.value = '';
                timeInput.value = '';
                
                // RECARGAR TODOS LOS DATOS DEL SERVIDOR
                await this.loadAllMedications();
                
                // Actualizar vista
                this.loadDayMedications();
                this.renderCalendar();
                
                alert('Medicamento agregado correctamente.');
            } else {
                throw new Error('Error al agregar el medicamento');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al agregar el medicamento. Por favor, inténtalo de nuevo.');
        }
    }

   async removeMedication(medicationId) {

    try {
        const response = await fetch('/delete_recordatorio_by_id', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: medicationId })
        });
        console.log(medicationId)
        if (!response.ok) throw new Error('Error al eliminar el medicamento');

        // Carga principal
        await this.loadAllMedications();

        // Cargas secundarias, optimizadas
        requestAnimationFrame(() => {
            this.loadDayMedications();
            this.renderCalendar();
        });

        alert('Medicamento eliminado correctamente.');
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar el medicamento. Por favor, inténtalo de nuevo.');
    }
}

    getDateKey(date) {
        return date.toISOString().split('T')[0];
    }
}

// Inicializar la aplicación
const calendar = new CalendarApp();