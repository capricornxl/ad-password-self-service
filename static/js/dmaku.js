var scanCodeButton = document.getElementById('scanCode')
var modifyPwdButton = document.getElementById('modifyPwd')
var container = document.getElementById('middle-container')

if (scanCodeButton !== null) {
    scanCodeButton.addEventListener('click', function () {
        container.classList.add('right-panel-active')
    })
}
if (modifyPwdButton !== null) {
    modifyPwdButton.addEventListener('click', function () {
        container.classList.remove('right-panel-active')
    });
}
