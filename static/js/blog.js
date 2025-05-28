document.addEventListener('DOMContentLoaded', function() {
    // Inicializar elementos
    const messagesContainer = document.getElementById('chat-messages');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const charCounter = document.getElementById('char-counter');
    const currentUserId = document.getElementById('user_id').textContent;
    const connectionStatus = document.getElementById('connection-status');
    const statusText = document.getElementById('status-text');
    const scrollToBottomBtn = document.getElementById('scroll-to-bottom');
    
    // Inicializar SocketIO
    const socket = io('https://medical-zuhb.onrender.com');
    
    // Función mejorada para scroll automático
    function scrollToBottom(smooth = true) {
        const scrollHeight = messagesContainer.scrollHeight;
        const height = messagesContainer.clientHeight;
        const maxScrollTop = scrollHeight - height;
        
        if (smooth) {
            messagesContainer.scrollTo({
                top: maxScrollTop,
                behavior: 'smooth'
            });
        } else {
            messagesContainer.scrollTop = maxScrollTop;
        }
    }
    
    // Función para mostrar/ocultar botón de scroll
    function toggleScrollButton() {
        const scrollTop = messagesContainer.scrollTop;
        const scrollHeight = messagesContainer.scrollHeight;
        const clientHeight = messagesContainer.clientHeight;
        const isNearBottom = scrollTop + clientHeight >= scrollHeight - 100;
        
        if (isNearBottom) {
            scrollToBottomBtn.classList.add('hidden');
        } else {
            scrollToBottomBtn.classList.remove('hidden');
        }
    }
    
    // Event listener para el scroll
    messagesContainer.addEventListener('scroll', toggleScrollButton);
    
    // Event listener para el botón de scroll
    scrollToBottomBtn.addEventListener('click', function() {
        scrollToBottom(true);
    });
    
    // Auto-resize del textarea
    function autoResizeTextarea() {
        messageInput.style.height = 'auto';
        const newHeight = Math.min(messageInput.scrollHeight, 120);
        messageInput.style.height = newHeight + 'px';
    }
    
    // Función para crear elemento de mensaje con Tailwind
    function createMessageElement(messageData) {
        const isMyMessage = messageData.usuario_id == currentUserId;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-4 flex ${isMyMessage ? 'justify-end' : 'justify-start'}`;
        
        let userHeader = '';
        let messageClasses = '';
        let textClasses = '';
        let timeClasses = '';
        
        if (isMyMessage) {
            messageClasses = 'bg-blue-600 text-white';
            timeClasses = 'text-blue-100';
        } else {
            const userType = messageData.tipo_usuario.toLowerCase();
            let borderColor = '';
            let badgeColor = '';
            
            switch(userType) {
                case 'paciente':
                    borderColor = 'border-blue-500';
                    badgeColor = 'bg-blue-500';
                    break;
                case 'doctor':
                    borderColor = 'border-purple-500';
                    badgeColor = 'bg-purple-500';
                    break;
                default:
                    borderColor = 'border-green-500';
                    badgeColor = 'bg-green-500';
            }
            
            messageClasses = `bg-white text-gray-800 border-l-4 ${borderColor}`;
            textClasses = 'text-gray-800';
            timeClasses = 'text-gray-500';
            
            userHeader = `
                <div class="flex items-center gap-2 mb-1">
                    <span class="text-sm font-semibold text-gray-700">${messageData.username}</span>
                    <span class="px-2 py-1 text-xs rounded-full ${badgeColor} text-white">
                        ${messageData.tipo_usuario.charAt(0).toUpperCase() + messageData.tipo_usuario.slice(1)}
                    </span>
                </div>
            `;
        }
        
        messageDiv.innerHTML = `
            <div class="max-w-xs lg:max-w-md">
                ${userHeader}
                <div class="p-3 rounded-lg shadow ${messageClasses}">
                    <p class="${textClasses}">${messageData.contenido}</p>
                    <p class="text-xs mt-1 text-right ${timeClasses}">
                        ${messageData.hora_envio}
                    </p>
                </div>
            </div>
        `;
        
        return messageDiv;
    }
    
    // Función para mostrar/ocultar mensaje vacío
    function toggleEmptyMessage() {
        const emptyMessage = messagesContainer.querySelector('.empty-chat');
        const hasMessages = messagesContainer.querySelectorAll('[class*="mb-4 flex"]').length > 0;
        
        if (emptyMessage) {
            emptyMessage.style.display = hasMessages ? 'none' : 'block';
        }
    }
    
    // Escuchar nuevos mensajes
    socket.on('new_message', function(messageData) {
        const messageElement = createMessageElement(messageData);
        messagesContainer.appendChild(messageElement);
        toggleEmptyMessage();
        
        // Auto-scroll si el usuario está cerca del final
        const isNearBottom = messagesContainer.scrollTop + messagesContainer.clientHeight >= messagesContainer.scrollHeight - 100;
        if (isNearBottom) {
            setTimeout(() => scrollToBottom(true), 100);
        }
        
        toggleScrollButton();
    });
    
    // Enviar mensaje
    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const content = messageInput.value.trim();
        if (!content) return;
        
        const submitButton = messageForm.querySelector('button[type="submit"]');
        const buttonText = submitButton.querySelector('span');
        const buttonIcon = submitButton.querySelector('i');
        
        // Deshabilitar botón
        submitButton.disabled = true;
        submitButton.classList.add('opacity-50', 'cursor-not-allowed');
        buttonText.textContent = 'Enviando...';
        buttonIcon.className = 'fas fa-spinner fa-spin';
        
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contenido: content
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                messageInput.value = '';
                autoResizeTextarea();
                updateCharCounter();
                // Scroll automático después de enviar
                setTimeout(() => scrollToBottom(true), 100);
            } else {
                showNotification('Error al enviar el mensaje: ' + (data.error || 'Error desconocido'), 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error al enviar el mensaje. Verifica tu conexión.', 'error');
        })
        .finally(() => {
            // Rehabilitar botón
            submitButton.disabled = false;
            submitButton.classList.remove('opacity-50', 'cursor-not-allowed');
            buttonText.textContent = 'Enviar';
            buttonIcon.className = 'fas fa-paper-plane';
        });
    });
    
    // Contador de caracteres mejorado
    function updateCharCounter() {
        const length = messageInput.value.length;
        charCounter.textContent = `${length}/500 caracteres`;
        
        if (length > 450) {
            charCounter.classList.add('text-red-500');
            charCounter.classList.remove('text-gray-500');
        } else {
            charCounter.classList.remove('text-red-500');
            charCounter.classList.add('text-gray-500');
        }
    }
    
    // Event listeners
    messageInput.addEventListener('input', function() {
        updateCharCounter();
        autoResizeTextarea();
    });
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            messageForm.dispatchEvent(new Event('submit'));
        }
    });
    
    // Función para mostrar estado de conexión
    function showConnectionStatus(connected) {
        connectionStatus.classList.remove('hidden');
        
        if (connected) {
            connectionStatus.className = 'fixed top-4 right-4 px-4 py-2 rounded-full text-sm font-medium bg-green-500 text-white';
            statusText.textContent = 'Conectado';
            setTimeout(() => {
                connectionStatus.classList.add('hidden');
            }, 3000);
        } else {
            connectionStatus.className = 'fixed top-4 right-4 px-4 py-2 rounded-full text-sm font-medium bg-red-500 text-white';
            statusText.textContent = 'Desconectado';
        }
    }
    
    // Función para mostrar notificaciones con Tailwind
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        const bgColor = type === 'error' ? 'bg-red-500' : 'bg-green-500';
        
        notification.className = `fixed top-5 left-1/2 transform -translate-x-1/2 ${bgColor} text-white px-6 py-3 rounded-full font-semibold z-50 shadow-lg transition-all duration-300 opacity-0 -translate-y-2`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Mostrar con animación
        setTimeout(() => {
            notification.classList.remove('opacity-0', '-translate-y-2');
            notification.classList.add('opacity-100', 'translate-y-0');
        }, 10);
        
        // Ocultar después de 3 segundos
        setTimeout(() => {
            notification.classList.add('opacity-0', '-translate-y-2');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    // Función para mostrar ayuda
    window.showHelp = function() {
        showNotification('Chat en tiempo real - Usa Enter para enviar, Shift+Enter para nueva línea', 'info');
    }
    
    // Eventos de Socket.IO
    socket.on('connect', function() {
        console.log('Conectado al servidor');
        showConnectionStatus(true);
    });
    
    socket.on('disconnect', function() {
        console.log('Desconectado del servidor');
        showConnectionStatus(false);
    });
    
    socket.on('connect_error', function(error) {
        console.error('Error de conexión:', error);
        showConnectionStatus(false);
    });
    
    // Inicialización
    toggleEmptyMessage();
    updateCharCounter();
    
    // Scroll inicial
    setTimeout(() => {
        scrollToBottom(false);
        toggleScrollButton();
    }, 100);
});