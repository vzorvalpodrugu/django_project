document.addEventListener('DOMContentLoaded', () => {
    console.log('Скрипт работает!');
   const countdownElement = document.getElementById('countdown');
  let seconds = 10;

  if (!countdownElement) {
      console.error('Элемент #countdown не найден!');
      return;
}
  function updateCountdown() {
    if (seconds > 0) {
      countdownElement.textContent = `Вы будете перенаправлены на главную через ${seconds} секунд...`;
      seconds--;
    } else {
      clearInterval(intervalId);
      const redirectUrl = countdownElement.getAttribute('data-redirect-url');
      window.location.href = redirectUrl;
    }
  }

  updateCountdown(); // initial call
  let intervalId = setInterval(updateCountdown, 1000);
});
