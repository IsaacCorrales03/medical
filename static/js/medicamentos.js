        class CalendarApp {
            constructor() {
                this.currentDate = new Date();
                this.selectedDate = null;
                this.medications = {}; // Almacenará los medicamentos por fecha
                this.init();
            }

            init() {
                this.renderCalendar();
                this.setupEventListeners();
                this.loadMedications();
            }

            setupEventListeners() {
                document.getElementById('prevMonth').addEventListener('click', () => {
                    this.currentDate.setMonth(this.currentDate.getMonth() - 1);
                    this.renderCalendar();
                });

                document.getElementById('nextMonth').addEventListener('click', () => {
                    this.currentDate.setMonth(this.currentDate.getMonth() + 1);
                    this.renderCalendar();
                });

                document.getElementById('closePanelBtn').addEventListener('click', () => {
                    this.closeDayPanel();
                });

                document.getElementById('addMedicationBtn').addEventListener('click', () => {
                    this.addMedication();
                });
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
                    
                    // Marcar día actual
                    if (year === today.getFullYear() && 
                        month === today.getMonth() && 
                        day === today.getDate()) {
                        dayElement.classList.add('current-day');
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
                panel.classList.add('show');
            }

            closeDayPanel() {
                const panel = document.getElementById('dayPanel');
                panel.classList.remove('show');
                
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
                    medications.forEach((med, index) => {
                        const medElement = document.createElement('div');
                        medElement.className = 'medication-item flex items-center justify-between p-3 border rounded-lg';
                        medElement.innerHTML = `
                            <div>
                                <div class="font-medium text-gray-800">${med.nombre}</div>
                                <div class="text-sm text-gray-500">${med.hora}</div>
                            </div>
                            <button onclick="calendar.removeMedication('${dateKey}', ${index})" 
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
                            fecha: fecha,
                            hora: hora,
                            nombre: nombre
                        })
                    });
                    
                    if (response.ok) {
                        // Agregar a la lista local
                        if (!this.medications[fecha]) {
                            this.medications[fecha] = [];
                        }
                        
                        this.medications[fecha].push({
                            nombre: nombre,
                            hora: hora
                        });
                        
                        // Limpiar formulario
                        nameInput.value = '';
                        timeInput.value = '';
                        
                        // Actualizar vista
                        this.loadDayMedications();
                        
                        alert('Medicamento agregado correctamente.');
                    } else {
                        throw new Error('Error al agregar el medicamento');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error al agregar el medicamento. Por favor, inténtalo de nuevo.');
                }
            }

            removeMedication(dateKey, index) {
                if (this.medications[dateKey]) {
                    this.medications[dateKey].splice(index, 1);
                    this.loadDayMedications();
                }
            }

            getDateKey(date) {
                return date.toISOString().split('T')[0];
            }

            loadMedications() {
                // Aquí puedes cargar los medicamentos existentes desde el servidor
                // Por ahora, algunos datos de ejemplo:
                const today = new Date();
                const todayKey = this.getDateKey(today);
                
                this.medications[todayKey] = [
                    { nombre: 'Paracetamol', hora: '08:00' },
                    { nombre: 'Ibuprofeno', hora: '14:00' }
                ];
            }
        }

        // Inicializar la aplicación
        const calendar = new CalendarApp();