function calculateContractEnd(contractDate, years) {
    const endDate = new Date(contractDate);
    endDate.setFullYear(endDate.getFullYear() + years);
    return endDate;
}

function findEmployeesByYear() {
    const year = parseInt(document.getElementById('yearInput').value);
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = "";

    const employees = document.getElementsByClassName('employee');
    for (let employee of employees) {
        const surname = employee.dataset.surname;
        const contractDate = new Date(employee.dataset.contractDate);
        const contractYears = parseInt(employee.dataset.contractYears);

        const endDate = calculateContractEnd(contractDate, contractYears);
        if (endDate.getFullYear() == year) {
            resultsDiv.innerHTML += `<p>${surname}, контракт заканчивается ${endDate.toLocaleDateString()}, ${endDate.toLocaleString('default', { month: 'long' })}, ${endDate.toLocaleString('default', { weekday: 'long' })}</p>`;
        }
    }
}

document.getElementById('employeeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const surname = document.getElementById('surname').value;
    const contractDate = document.getElementById('contractDate').value;
    const contractYears = parseInt(document.getElementById('contractYears').value);

    const newEmployeeDiv = document.createElement('div');
    newEmployeeDiv.classList.add('employee');
    newEmployeeDiv.dataset.surname = surname;
    newEmployeeDiv.dataset.contractDate = contractDate;
    newEmployeeDiv.dataset.contractYears = contractYears;
    document.body.appendChild(newEmployeeDiv);
});