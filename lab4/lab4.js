function processForm() {
    const scores = [];
    for (let i = 1; i <= 6; i++) {
        const selected = document.querySelector('input[name="task' + i + '"]:checked');
        scores.push(selected ? parseInt(selected.value) : 0);
    }

    let totalScore = 0;
    for (let score of scores) {
        totalScore += score;
    }

    let place = "Не призовое место";
    if (scores[0] == 30 && scores[1] == 30 && scores[2] == 30 && scores[3] == 30 && scores[4] == 30 && scores[5] == 30) {
        place = "Первое место";
    } else if ((scores[0] >= 20 && scores[1] >= 20 && scores[2] >= 20 && scores[3] >= 20 && scores[4] >= 20 && scores[5] >= 20) && (scores.includes(30))) {
        place = "Второе место";
    } else if (scores[0] == 20 && scores[1] == 20 && scores[2] == 20 && scores[3] == 20 && scores[4] == 20 && scores[5] == 20) {
        place = "Третье место";
    }

    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = "<strong>Сумма баллов:</strong> " + totalScore + "<br><strong>Место:</strong> " + place;
}