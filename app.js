const clubs = [
  { id: 1, name: "Robotics", category: "Technology", schedule: "Tuesday · 15:30", capacity: 2 },
  { id: 2, name: "Debate", category: "Communication", schedule: "Wednesday · 16:00", capacity: 3 },
  { id: 3, name: "Drawing", category: "Creative arts", schedule: "Thursday · 15:30", capacity: 1 }
];
const sampleEnrollments = [
  { studentId: 102, clubId: 1 },
  { studentId: 103, clubId: 2 },
  { studentId: 104, clubId: 3 }
];
const storageKey = "school-club-enrollment-demo-v1";
const studentIds = new Set([101, 102, 103, 104]);
const cards = document.querySelector("#clubs");
const notice = document.querySelector("#notice");

function loadEnrollments() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey));
    return Array.isArray(saved) ? saved : sampleEnrollments;
  } catch {
    return sampleEnrollments;
  }
}

let enrollments = loadEnrollments();

function saveEnrollments() {
  localStorage.setItem(storageKey, JSON.stringify(enrollments));
}

function placesLeft(club) {
  return club.capacity - enrollments.filter(item => item.clubId === club.id).length;
}

function showNotice(message, isError = false) {
  notice.textContent = message;
  notice.classList.toggle("error", isError);
  notice.hidden = false;
}

function renderClubs() {
  cards.innerHTML = clubs.map((club, index) => {
    const available = placesLeft(club);
    const full = available <= 0;
    return '<article>' +
      '<div class="card-top"><p class="category">' + club.category + '</p><span class="club-number">0' + (index + 1) + '</span></div>' +
      '<h2>' + club.name + '</h2>' +
      '<p class="schedule">' + club.schedule + '</p>' +
      '<p class="places"><span>Available places</span><strong>' + available + ' of ' + club.capacity + '</strong></p>' +
      '<form data-club-id="' + club.id + '">' +
      '<label for="student-' + club.id + '">Student ID</label>' +
      '<div class="form-row">' +
      '<input id="student-' + club.id + '" name="studentId" type="number" min="1" required placeholder="e.g. 101" ' + (full ? "disabled" : "") + '>' +
      '<button type="submit" ' + (full ? "disabled" : "") + '>' + (full ? "Club full" : "Enroll") + '</button>' +
      '</div></form></article>';
  }).join("");
}

cards.addEventListener("submit", event => {
  event.preventDefault();
  const form = event.target;
  const studentId = Number(new FormData(form).get("studentId"));
  const clubId = Number(form.dataset.clubId);
  const club = clubs.find(item => item.id === clubId);

  if (!studentIds.has(studentId)) {
    showNotice("Please enter a valid demo student ID: 101, 102, 103 or 104.", true);
    return;
  }
  if (enrollments.some(item => item.studentId === studentId && item.clubId === clubId)) {
    showNotice("This student is already enrolled in this club.", true);
    return;
  }
  if (placesLeft(club) <= 0) {
    showNotice("This club is full. Please choose another club.", true);
    renderClubs();
    return;
  }

  enrollments.push({ studentId: studentId, clubId: clubId });
  saveEnrollments();
  renderClubs();
  showNotice("Enrollment confirmed: " + club.name + " · " + club.schedule + ".");
});

document.querySelector("#reset-demo").addEventListener("click", () => {
  enrollments = sampleEnrollments.map(item => ({ studentId: item.studentId, clubId: item.clubId }));
  saveEnrollments();
  renderClubs();
  showNotice("Demo data has been reset.");
});

renderClubs();
