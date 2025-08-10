document.addEventListener('DOMContentLoaded', function() {
    const masterSelect = document.querySelector('#id_master');
    const servicesContainer = document.querySelector('#services-container');

    function updateServices(masterId) {
        if (masterId) {
            fetch(`/ajax/get-master-services/?master_id=${masterId}`)
                .then(response => response.json())
                .then(data => {
                    servicesContainer.innerHTML = '';

                    if (data.services && data.services.length) {
                        data.services.forEach(service => {
                            const div = document.createElement('div');
                            div.className = 'form-check';

                            const input = document.createElement('input');
                            input.className = 'form-check-input';
                            input.type = 'checkbox';
                            input.name = 'services';
                            input.value = service.id;
                            input.id = `id_services_${service.id}`;

                            const label = document.createElement('label');
                            label.className = 'form-check-label';
                            label.htmlFor = input.id;
                            label.textContent = service.name;

                            div.appendChild(input);
                            div.appendChild(label);
                            servicesContainer.appendChild(div);
                        });
                    } else {
                        servicesContainer.innerHTML = '<p class="text-muted">Нет доступных услуг</p>';
                    }
                });
        }
    }

    if (masterSelect) {
        masterSelect.addEventListener('change', function() {
            updateServices(this.value);
        });

        if (masterSelect.value) {
            updateServices(masterSelect.value);
        }
    }
});
