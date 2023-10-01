let search_type = "restaurants";
$(document).ready(function () {
   
    $(".place").click(function () {
        $(".place").removeClass("bg-cyan-400");
        $(".place").addClass("bg-gray-300");
        $(this).removeClass("bg-gray-300");
        $(this).addClass("bg-cyan-400");
        search_type = $(this).text();
    });
});

function Send_request() {
    let city = document.getElementById("cityInput").value
    if (city == "" || search_type == "") {
        return alert("all fiel required!!")
    }
    window.location.href = `/explore?city=${city}&search_type=${search_type}`;
}