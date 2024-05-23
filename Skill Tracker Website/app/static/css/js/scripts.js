// Function to show/hide password
const togglePassword = () => {
    const passwordField = document.getElementById('password-field');
    const passwordToggle = document.getElementById('password-toggle');
    
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);
    passwordToggle.innerText = type === 'password' ? 'Show Password' : 'Hide Password';
};

// Function to confirm password match
const confirmPassword = () => {
    const password = document.getElementById('password-field').value;
    const confirmPassword = document.getElementById('confirm-password-field').value;
    const message = document.getElementById('confirm-password-message');

    if (password !== confirmPassword) {
        message.innerText = 'Passwords do not match';
        message.classList.add('text-danger');
    } else {
        message.innerText = '';
        message.classList.remove('text-danger');
    }
};

// Function to handle AJAX request for adding a skill
const addSkill = () => {
    const skillName = document.getElementById('skill-name').value;
    
    if (skillName.trim() === '') {
        alert('Skill name cannot be empty.');
        return;
    }

    // Send skillName to server using AJAX
    fetch('/add_skill', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: skillName }),
    })
    .then(response => response.json())
    .then(data => {
        // Assuming the server responds with the newly created skill object
        console.log('Skill added:', data);
        const skillList = document.getElementById('skill-list');
        const skillItem = document.createElement('li');
        skillItem.textContent = data.name;
        skillList.appendChild(skillItem);
    })
    .catch(error => {
        console.error('Error adding skill:', error);
        // Handle error, display error message, etc.
    });
};

// Function to handle AJAX request for logging skill hours
const logSkillHours = () => {
    const skillId = document.getElementById('skill-id').value;
    const hoursLogged = document.getElementById('hours-logged').value;

    if (skillId.trim() === '' || hoursLogged.trim() === '') {
        alert('Skill ID and hours logged cannot be empty.');
        return;
    }

    // Send skillId and hoursLogged to server using AJAX
    fetch('/log_hours', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ skillId: skillId, hoursLogged: hoursLogged }),
    })
    .then(response => response.json())
    .then(data => {
        // Assuming the server responds with updated skill log data
        console.log('Skill hours logged:', data);
    })
    .catch(error => {
        console.error('Error logging skill hours:', error);
        // Handle error, display error message, etc.
    });
};

// Event listeners
document.getElementById('password-toggle').addEventListener('click', togglePassword);
document.getElementById('password-field').addEventListener('input', confirmPassword);
document.getElementById('confirm-password-field').addEventListener('input', confirmPassword);
document.getElementById('add-skill-btn').addEventListener('click', addSkill);
document.getElementById('log-hours-btn').addEventListener('click', logSkillHours);
