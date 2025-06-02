        function loadEmployees() {
            const employees = localStorage.getItem('employees');
            return employees ? JSON.parse(employees) : [];
        }

        function saveEmployees(employees) {
            localStorage.setItem('employees', JSON.stringify(employees));
        }

        function calculateContractEnd(contractDate, years) {
            const endDate = new Date(contractDate);
            endDate.setFullYear(endDate.getFullYear() + years);
            return endDate;
        }

        function findEmployeesByYear() {
            const year = parseInt(document.getElementById('yearInput').value);
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = "";

            const employees = loadEmployees();
            for (let employee of employees) {
                const endDate = calculateContractEnd(employee.contractDate, employee.contractYears);
                if (endDate.getFullYear() == year) {
                    resultsDiv.innerHTML += `<p>${employee.surname}, контракт заканчивается ${endDate.toLocaleDateString()}, ${endDate.toLocaleString('default', { month: 'long' })}, ${endDate.toLocaleString('default', { weekday: 'long' })}</p>`;
                }
            }
        }

        document.getElementById('employeeForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const surname = document.getElementById('surname').value;
            const contractDate = document.getElementById('contractDate').value;
            const contractYears = parseInt(document.getElementById('contractYears').value);

            const employees = loadEmployees();
            
            employees.push({
                surname: surname,
                contractDate: contractDate,
                contractYears: contractYears
            });
            
            saveEmployees(employees);
            
            document.getElementById('employeeForm').reset();
        });