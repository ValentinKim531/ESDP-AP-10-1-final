if ("{{ type_form }}" == 'def_request') {
    const requestFormForm = document.createElement('form');
    requestFormForm.id = 'form_request'
    requestFormForm.method = 'post';
    requestFormForm.innerHTML = `{% include 'partial/request_form.html' %}`
    const requestButton = document.createElement('input');
    requestButton.type = "submit";
    requestButton.class = "btn btn-success";
    requestButton.value = "Создать";
    requestFormForm.append(requestButton);
    const divForm = document.getElementById("id_form");
    divForm.append(requestFormForm);
} else if ("{{ type_form }}" == 'sub_request') {
    const requestFormForm = document.createElement('form');
    requestFormForm.id = 'form_request'
    requestFormForm.method = 'post';
    requestFormForm.innerHTML = `{% include 'partial/sub_request_form.html' %}`
    const requestButton = document.createElement('input');
    requestButton.type = "submit";
    requestButton.class = "btn btn-success";
    requestButton.value = "Обновить";
    requestFormForm.append(requestButton);
    const divForm = document.getElementById("id_form");
    divForm.append(requestFormForm);
} else if ("{{ type_form }}" == 'chat_request') {
    const requestFormForm = document.createElement('form');
    requestFormForm.id = 'form_request'
    requestFormForm.method = 'post';
    requestFormForm.innerHTML = `{% include 'partial/chat_request_form.html' %} {% include 'partial/request_form.html' %}`
    const requestButton = document.createElement('input');
    requestButton.type = "submit";
    requestButton.class = "btn btn-success";
    requestButton.value = "Обновить";
    requestFormForm.append(requestButton);
    const divForm = document.getElementById("id_form");
    divForm.append(requestFormForm);
};
const requestSelect = document.getElementById("request_select");
requestSelect.onchange = function() {
    const divForSelect = document.getElementById("id_form");
    const requestFormFormSelect = document.getElementById('form_request');
    const targetValue = requestSelect.value;
    divForSelect.removeChild(requestFormFormSelect);
    const requestFormForm = document.createElement('form');
    requestFormForm.id = 'form_request'
    requestFormForm.method = 'post'
    if (targetValue === 'chat_request') {
        requestFormForm.innerHTML = `{% include 'partial/chat_request_form.html' %} {% include 'partial/request_form.html' %}`
    } else if (targetValue === 'sub_request') {
        requestFormForm.innerHTML = `{% include 'partial/sub_request_form.html' %}`
    } else if (targetValue === 'request') {
        requestFormForm.innerHTML = `{% include 'partial/request_form.html' %}`
    };
    const requestButton = document.createElement('input');
    requestButton.type = "submit";
    requestButton.class = "btn btn-success";
    requestButton.value = "Обновить";
    requestFormForm.append(requestButton);
    const divForm = document.getElementById("id_form");
    divForm.append(requestFormForm);
};