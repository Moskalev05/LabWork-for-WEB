$(document).ready(function () {
    //1.<li>, которые содержат <a>
    $("#my_links li:has(a)").addClass("highlight-green");

    //2.ссылки <a>, у которых href начинается с "documents"
    $("#my_links a[href^='documents']").addClass("highlight-blue");

    //3.последние ячейки в чётных строках таблицы
    $("#moto_table tr:even td:last-child").addClass("highlight-red");
});