var sideA = parseFloat(prompt("Введите длину катета A:"));
var sideB = parseFloat(prompt("Введите длину катета B:"));

if (!isNaN(sideA) && !isNaN(sideB) && sideA > 0 && sideB > 0) {
    var hypotenuse = Math.sqrt(Math.pow(sideA, 2) + Math.pow(sideB, 2));
    var confirmation = confirm("Гипотенуза треугольника с катетами A = " + sideA + " и B = " + sideB + " равна: " + hypotenuse + "\n\nПодтвердите, чтобы продолжить.");

    if (confirmation) {
        alert("Продолжаем");
    } else {
        alert("Операция отменена.");
    }
} else {
    alert("Пожалуйста, проверьте ввод");
}