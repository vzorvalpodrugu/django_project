document.addEventListener('DOMContentLoaded', function() {
    const masterSelect = document.querySelector('#id_master');
    const servicesContainer = document.querySelector('#id_services');  // Это теперь контейнер чекбоксов

    if (masterSelect && servicesContainer) {
        masterSelect.addEventListener('change', function() {
            const masterId = this.value;

            if (masterId) {
                fetch(`/ajax/get-master-services/?master_id=${masterId}`)
                    .then(response => response.json())
                    .then(data => {
                        // Сохраняем выбранные значения
                        const selectedValues = Array.from(
                            servicesContainer.querySelectorAll('input:checked')
                        ).map(el => el.value);

                        // Очищаем контейнер
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

                                // Восстанавливаем выбранные значения
                                if (selectedValues.includes(service.id.toString())) {
                                    input.checked = true;
                                }

                                const label = document.createElement('label');
                                label.className = 'form-check-label';
                                label.htmlFor = input.id;
                                label.textContent = service.name;

                                div.appendChild(input);
                                div.appendChild(label);
                                servicesContainer.appendChild(div);
                            });
                        } else {
                            servicesContainer.innerHTML = '<p>Нет доступных услуг для выбранного мастера</p>';
                        }
                    })
                    .catch(error => console.error('Error:', error));
            }
        });

        // Инициализация при загрузке
        if (masterSelect.value) {
            masterSelect.dispatchEvent(new Event('change'));
        }
    }
});

 const toastElList = document.querySelectorAll(".toast");
  const toastList = [...toastElList].map((toastEl) => {
    const toast = new bootstrap.Toast(toastEl, {
      delay: 5000, // 5 секунд
    });
    toast.show();
    return toast;
  });