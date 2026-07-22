// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// API helper functions
const API = {
    getTickets: async (params = {}) => {
        const query = new URLSearchParams(params).toString();
        const response = await fetch(`/api/tickets${query ? '?' + query : ''}`);
        return response.json();
    },
    
    getTicket: async (ticketId) => {
        const response = await fetch(`/api/tickets/${ticketId}`);
        return response.json();
    },
    
    createTicket: async (data) => {
        const response = await fetch('/api/tickets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    },
    
    updateTicket: async (ticketId, data) => {
        const response = await fetch(`/api/tickets/${ticketId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    }
};