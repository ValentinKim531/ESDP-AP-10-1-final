document.addEventListener('DOMContentLoaded', function () {
    const dates = document.getElementsByClassName('date');
    const query = new URLSearchParams(window.location.search);
    const currentMonth = Object.fromEntries(query.entries()).month
    const [year, month] = currentMonth.split("-");
    for (let i = 0; i < dates.length; i++) {
        dates[i].addEventListener('click', function () {
            const date = dates[i].innerHTML;
            const url = `/get_events/?date=${date}&year=${year}&month=${month}`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    const eventsContainer = document.getElementsByClassName('events-today')[0];
                    eventsContainer.innerHTML = '';  // Очистить предыдущие результаты поиска

                    if (data.length === 0) {
                        const noEventsMsg = document.createElement('p');
                        noEventsMsg.className = 'no_events_for_today';
                        noEventsMsg.textContent = 'События не найдены';
                        eventsContainer.appendChild(noEventsMsg);
                    } else {
                        for (let j = 0; j < data.length; j++) {
                            const eventLink = document.createElement('a');
                            const calendarUrl = data[j].url;
                            const eventUrl = calendarUrl.split('/calendar').join(''); // Remove "calendar" from the URL

                            eventLink.href = eventUrl;
                            eventLink.className = 'event_card_mini_link';

                            const eventCard = document.createElement('div');
                            eventCard.className = 'event_card_mini';

                            const eventName = document.createElement('p');
                            eventName.className = 'event_name_calendar';
                            eventName.textContent = data[j].name;

                            eventCard.appendChild(eventName);
                            eventLink.appendChild(eventCard);
                            eventsContainer.appendChild(eventLink);
                        }
                    }
                })
                .catch(error => console.log(error));
        });
    }
});
