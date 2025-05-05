document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded');
    const today = new Date();

    // Formatear y mostrar el mes actual
    const monthNames = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    
    const currentMonthElement = document.getElementById('currentMonth');
    if (currentMonthElement) {
        currentMonthElement.textContent = monthNames[today.getMonth()] + ' ' + today.getFullYear();
    } else {
        console.error('Element with ID "currentMonth" not found');
    }

    // Verificamos si el elemento calendarDays existe
    if (!document.getElementById('calendarDays')) {
        console.error('Element with ID "calendarDays" not found');
        return;
    }

    // Primero obtenemos los medicamentos y luego generamos el calendario
    console.log('Fetching medications...');
    fetch('/get_medication')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(medications => {
            console.log('Medications loaded successfully:', medications);
            // Generar el calendario con los medicamentos
            generateCalendarWithMedications(today, medications);
        })
        .catch(error => {
            console.error('Error fetching medications:', error);
            // Si hay un error, generar el calendario normal
            generateCalendar(today);
        });
});

function generateCalendarWithMedications(date, medications) {
    const year = date.getFullYear();
    const month = date.getMonth();
    const today = new Date();

    // Obtener el primer día del mes
    const firstDay = new Date(year, month, 1);

    // Obtener el día de la semana del primer día (0 = Domingo, 1 = Lunes, etc.)
    let firstDayOfWeek = firstDay.getDay();
    // Convertir de 0-6 (Dom-Sáb) a 1-7 (Lun-Dom)
    firstDayOfWeek = firstDayOfWeek === 0 ? 7 : firstDayOfWeek;

    // Obtener el último día del mes
    const lastDay = new Date(year, month + 1, 0).getDate();

    // Contenedor de días
    const calendarDays = document.getElementById('calendarDays');
    calendarDays.innerHTML = '';

    // Añadir celdas vacías para los días antes del primer día del mes
    for (let i = 1; i < firstDayOfWeek; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day empty';
        calendarDays.appendChild(emptyDay);
    }

    // Añadir días del mes
    for (let day = 1; day <= lastDay; day++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day text-center py-2 text-sm relative cursor-pointer w-full h-12 flex items-center justify-center';
        dayElement.style.zIndex = -0

        // Comprobar si es el día actual
        if (today.getDate() === day && today.getMonth() === month && today.getFullYear() === year) {
            dayElement.classList.add('bg-blue-100', 'rounded');
        }

        // Fecha actual para comparar con los medicamentos
        const currentDate = new Date(year, month, day);
        // Día de la semana (1-7, donde 1 es lunes)
        const dayOfWeek = currentDate.getDay() === 0 ? 7 : currentDate.getDay();

        // Array para almacenar los medicamentos de este día
        let dayMedications = [];

        // Comprobar si hay medicamentos para este día
        medications.forEach(med => {
            let shouldShow = false;

            // Comprobar según la frecuencia
            if (med.frecuencia === 'diario') {
                shouldShow = true;
            } else if (med.frecuencia === 'semanal') {
                // Para frecuencia semanal, mostramos todos ya que no tenemos el dia en los datos
                // Si tuviéramos el día específico, usaríamos: parseInt(med.dia) === dayOfWeek
                shouldShow = true;
            } else if (med.frecuencia === 'mensual') {
                // Para frecuencia mensual, mostramos todos ya que no tenemos el dia en los datos
                // Si tuviéramos el día específico, usaríamos: parseInt(med.dia) === day
                shouldShow = true;
            } else if (med.frecuencia === 'varias_veces') {
                shouldShow = true;
            }

            if (shouldShow) {
                dayMedications.push(med);
            }
        });

        // Si hay medicamentos para este día, añadir indicador
        if (dayMedications.length > 0) {
            dayElement.classList.add('has-medications');

            // Añadir punto indicador de medicamento
            const indicatorElement = document.createElement('div');
            indicatorElement.className = 'medication-indicator bg-red-500 w-3 h-3 rounded-full absolute bottom-1 left-1/2 transform -translate-x-1/2';
            dayElement.appendChild(indicatorElement);
            
            // Añadir estilo visual para días con medicamentos
            dayElement.classList.add('border-red-300', 'border');

            // Crear tooltip para mostrar los medicamentos
            const tooltipElement = document.createElement('div');
            tooltipElement.className = 'medication-tooltip hidden absolute z-20 bg-white shadow-lg rounded p-2 text-left w-48 bottom-full left-1/2 transform -translate-x-1/2 mb-2';
            
            // Añadir flecha del tooltip
            const tooltipArrow = document.createElement('div');
            tooltipArrow.className = 'absolute w-3 h-3 bg-white transform rotate-45 left-1/2 -ml-1.5 -bottom-1.5';
            tooltipElement.appendChild(tooltipArrow);

            // Añadir contenido al tooltip
            const tooltipContent = document.createElement('div');
            tooltipContent.className = 'relative z-10';
            tooltipContent.innerHTML = '<p class="font-bold text-sm mb-1">Medicamentos:</p>';

            // Añadir cada medicamento al tooltip
            dayMedications.forEach(med => {
                tooltipContent.innerHTML += `
                    <div class="mb-1 pb-1 border-b border-gray-200 last:border-0">
                        <p class="text-sm font-semibold">${med.nombre}</p>
                        <p class="text-xs text-gray-600">Dosis: ${med.dosis}</p>
                        <p class="text-xs text-gray-600">Hora: ${med.hora}</p>
                    </div>
                `;
            });

            tooltipElement.appendChild(tooltipContent);
            dayElement.appendChild(tooltipElement);

            // Mostrar/ocultar tooltip al hacer hover
            dayElement.addEventListener('mouseenter', function () {
                tooltipElement.classList.remove('hidden');
            });

            dayElement.addEventListener('mouseleave', function () {
                tooltipElement.classList.add('hidden');
            });
        }

        // Asegurarse de que el número del día sea visible a pesar del indicador
const dayNumber = document.createElement('span');
dayNumber.textContent = day;
dayNumber.className = 'z-10 relative';
dayElement.appendChild(dayNumber);

calendarDays.appendChild(dayElement);
    }
}

function generateCalendar(date) {
    const year = date.getFullYear();
    const month = date.getMonth();
    const today = new Date();

    // Obtener el primer día del mes
    const firstDay = new Date(year, month, 1);

    // Obtener el día de la semana del primer día (0 = Domingo, 1 = Lunes, etc.)
    let firstDayOfWeek = firstDay.getDay();
    // Convertir de 0-6 (Dom-Sáb) a 1-7 (Lun-Dom)
    firstDayOfWeek = firstDayOfWeek === 0 ? 7 : firstDayOfWeek;

    // Obtener el último día del mes
    const lastDay = new Date(year, month + 1, 0).getDate();

    // Contenedor de días
    const calendarDays = document.getElementById('calendarDays');
    calendarDays.innerHTML = '';

    // Añadir celdas vacías para los días antes del primer día del mes
    for (let i = 1; i < firstDayOfWeek; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day empty';
        calendarDays.appendChild(emptyDay);
    }

    // Añadir días del mes
    for (let day = 1; day <= lastDay; day++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day text-center py-2 text-sm ';

        // Comprobar si es el día actual
        if (today.getDate() === day && today.getMonth() === month && today.getFullYear() === year) {
            dayElement.classList.add('bg-blue-100', 'rounded');
        }

        dayElement.textContent = day;
        calendarDays.appendChild(dayElement);
    }
}

// Modal functionality
const addMedicationBtn = document.getElementById('addMedicationBtn');
const medicationModal = document.getElementById('medicationModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const cicloSelect = document.getElementById('ciclo');
const diaContainer = document.getElementById('diaContainer');

// Show modal when button is clicked
if (addMedicationBtn) {
    addMedicationBtn.addEventListener('click', function () {
        medicationModal.classList.remove('hidden');
    });
}

// Hide modal when close button is clicked
if (closeModalBtn) {
    closeModalBtn.addEventListener('click', function () {
        medicationModal.classList.add('hidden');
    });
}

// Hide modal when clicking outside
if (medicationModal) {
    medicationModal.addEventListener('click', function (e) {
        if (e.target === medicationModal) {
            medicationModal.classList.add('hidden');
        }
    });
}

// Show/hide day selector based on cycle type
if (cicloSelect) {
    cicloSelect.addEventListener('change', function () {
        if (this.value === 'semanal') {
            diaContainer.classList.remove('hidden');
        } else {
            diaContainer.classList.add('hidden');
        }
    });
}

// Form submission (using fetch API)
const medicationForm = document.getElementById('medicationForm');
if (medicationForm) {
    medicationForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(this);

        fetch('/add_medication', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Medicamento añadido correctamente');
                    medicationModal.classList.add('hidden');
                    // Reload the page or update the calendar
                    location.reload();
                } else {
                    alert('Error al añadir el medicamento: ' + (data.message || 'Error desconocido'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al procesar la solicitud');
            });
    });
}