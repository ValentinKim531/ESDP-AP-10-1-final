const formWrap = document.getElementById('role_transfer_form_wrap');
const roleResetButton = document.getElementById('user_role_reset');
formWrap.style = `
    display: none;
`;
roleResetButton.style = `
    display: none;
`;
const roleUpdateButton = document.getElementById('user_role_update');
const roleName = document.getElementById('user_role_info');
roleUpdateButton.onclick = function() {
    roleResetButton.style = `
        display: block;
    `;
    formWrap.style = `
        display: block;
    `;
    roleUpdateButton.style = `
        display: none;
    `
}
roleResetButton.onclick = function() {
    roleResetButton.style = `
        display: none;
    `;
    formWrap.style = `
        display: none;
    `;
    roleUpdateButton.style = `
        display: block;
    `
}