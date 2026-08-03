// --- 1. OUVERTURE ET FERMETURE DE LA FENÊTRE MODALE ---

function openModal() {
  const modal = document.getElementById('bookingModal');
  if (modal) {
    modal.style.display = 'flex';
  } else {
    console.error("L'élément avec l'ID 'bookingModal' n'a pas été trouvé.");
  }
}

function closeModal() {
  const modal = document.getElementById('bookingModal');
  if (modal) {
    modal.style.display = 'none';
    const responseDiv = document.getElementById('modalResponse');
    if (responseDiv) responseDiv.innerText = '';
  }
}

// Fermeture si l'utilisateur clique en dehors de la fenêtre
window.onclick = function(event) {
  const modal = document.getElementById('bookingModal');
  if (event.target === modal) {
    closeModal();
  }
};


// --- 2. GESTION DU FORMULAIRE ET DE LA RÉSERVATION ---

document.addEventListener('DOMContentLoaded', () => {
  const bookingForm = document.getElementById('bookingForm');

  if (bookingForm) {
    bookingForm.addEventListener('submit', async function(e) {
      e.preventDefault();

      const responseDiv = document.getElementById('modalResponse');
      if (responseDiv) {
        responseDiv.style.color = 'var(--accent-gold)';
        responseDiv.innerText = 'Enregistrement de votre réservation en cours...';
      }

      // Récupération des données du formulaire
      const formData = {
        fullname: document.getElementById('fullname').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        service: document.getElementById('service').value,
        date: document.getElementById('date').value,
        time: document.getElementById('time').value
      };

      try {
        // Envoi au serveur Flask
        const res = await fetch('/api/booking', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        });

        const result = await res.json();

        if (result.success) {
          if (responseDiv) {
            responseDiv.style.color = '#4CAF50';
            responseDiv.innerText = result.message;
          }
          bookingForm.reset();
          setTimeout(closeModal, 3500);
        } else {
          if (responseDiv) {
            responseDiv.style.color = '#f44336';
            responseDiv.innerText = result.message || "Erreur lors de la réservation.";
          }
        }
      } catch (error) {
        console.error("Erreur serveur/réseau :", error);
        
        // Mode de secours si le serveur ou les e-mails ne sont pas configurés
        if (responseDiv) {
          responseDiv.style.color = '#f44336';
          responseDiv.innerHTML = `
            Un problème est survenu avec le serveur d'e-mail.<br>
            <a href="tel:0983809008" style="color: var(--accent-gold); text-decoration: underline; margin-top: 5px; display: inline-block;">
              Cliquez ici pour réserver par téléphone au 09 83 80 90 08
            </a>
          `;
        }
      }
    });
  }
});