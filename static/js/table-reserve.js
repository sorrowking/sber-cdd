const container = document.querySelector(".table-container");
const seats = document.querySelectorAll(".row .table-seat:not(.occupied)");

populateUI();

updateSelectedCount = () => {
  const selectedSeat = document.querySelector(".row .table-seat.selected");
  let selectedId = -1;

  if (selectedSeat) {
    selectedId = selectedSeat.dataset.id; // Assuming the id is stored in a 'data-id' attribute
    selectedValue = selectedSeat.dataset.value;
  }

  localStorage.setItem("selectedSeatId", selectedId);

  document.getElementById("selectedTableId").value = selectedId;
  document.getElementById("selectedTableNum").value = selectedValue;

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
    if (e.target.classList.contains("selected")) {
      e.target.classList.remove("selected"); // Remove "selected" class from previously selected table
    } else {
      const selectedSeats = document.querySelectorAll(".row .table-seat.selected");
      if (selectedSeats.length > 0) {
        selectedSeats[0].classList.remove("selected"); // Remove "selected" class from previously selected table
      }
      e.target.classList.add("selected"); // Add "selected" class to the newly selected table
    }
    updateSelectedCount(); // Update the selected seats in localStorage
  }
});

