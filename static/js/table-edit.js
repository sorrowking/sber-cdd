const container = document.querySelector(".table-container");
const seats = document.querySelectorAll(".row .table-seat:not(.occupied)");

populateUI();

updateSelectedCount = () => {
  const selectedSeats = document.querySelectorAll(".row .table-seat.selected");

  const seatsIndex = [...selectedSeats].map((seat) => {
    return [...seats].indexOf(seat);
  });

  localStorage.setItem("selectedSeats", JSON.stringify(seatsIndex));
};

function populateUI() {
  const selectedSeats = JSON.parse(localStorage.getItem("selectedSeats"));

  if (selectedSeats !== null && selectedSeats.length > 0) {
    seats.forEach((seat, index) => {
      if (selectedSeats.indexOf(index) > -1) {
        seat.classList.add("selected");
      }
    });
  }
}


container.addEventListener("click", (e) => {
  if (
    e.target.classList.contains("table-seat") &&
    !e.target.classList.contains("occupied")
  ) {
    e.target.classList.toggle("selected");
  }
  document.getElementById("selectedTableNum").value = e.target.dataset.value
});