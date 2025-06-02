function getZodiacSign(day, month) {
    const zodiacSigns = [
        "Козерог", "Водолей", "Рыбы", "Овен", "Телец", "Близнецы",
        "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец"
    ];

    const lastDayOfSign = [20, 19, 20, 20, 21, 21, 22, 23, 23, 23, 22, 21];
    return (day <= lastDayOfSign[month - 1]) ? zodiacSigns[month - 1] : zodiacSigns[month % 12];
}

document.getElementById('zodiacForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const day = parseInt(document.getElementById('day').value);
    const month = parseInt(document.getElementById('month').value);
    const zodiacSign = getZodiacSign(day, month);
    document.getElementById('result').innerHTML = "Знак зодиака: " + zodiacSign;
});