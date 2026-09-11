const teamLogos = {
    "UMBC": "images/UMBC.png",
    "Mount St. Mary's": "images/mount-st-marys.png",
    "Maryland": "images/maryland.png",
    "Loyola": "images/loyola.png",
    "Navy": "images/navy.png",
    "Towson": "images/towson.png",
    "Bowie State": "images/bowie-state.png",
    "Frostburg State": "images/frostburg-state.png",
    "Goucher": "images/goucher.png",
    "Hood": "images/hood.png",
    "Johns Hopkins": "images/johns-hopkins.png",
    "McDaniel": "images/mcdaniel.png",
    "Notre Dame (MD)": "images/notre-dame-md.png",
    "Salisbury": "images/salisbury.png",
    "St. Mary's": "images/st-marys.png",
    "Stevenson": "images/stevenson.png",
    "Washington College": "images/washington-college.png"
};


const sheetURL =
  "https://docs.google.com/spreadsheets/d/e/2PACX-1vTMUQiKrsd5pS1Tq7V1Qghgr6E0pCVhQvF7JiHiOgnJ_C_uuxCNljnCMBXWwzHK7WKBbo_x4aopyuJ1/pub?gid=924645803&single=true&output=csv";


// Converts dates like 07/26/2026 into Sunday, July 26
function formatDate(dateString) {

    const date = new Date(dateString);

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    date.setHours(0, 0, 0, 0);

    const formattedDate = date.toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric"
    });

    if (date.getTime() === today.getTime()) {
        return "Today — " + formattedDate;
    }

    return formattedDate;
}
function loadMatches() {

    fetch(sheetURL)
        .then(response => response.text())
        .then(data => {

            const matches = parseCSV(data);

            console.log(matches);

            const includedMatches = matches.filter(match => match.include === "Yes");

const teamFilter = document.getElementById("teamFilter");
const selectedTeam = teamFilter.value;

const teams = Object.keys(teamLogos).sort();

teamFilter.innerHTML = '<option value="All">All Teams</option>';

teams.forEach(team => {
    teamFilter.innerHTML += `<option value="${team}">${team}</option>`;
});

teamFilter.value = selectedTeam;

            const competition = document.getElementById("competitionFilter").value;

          const competitionDescription =
    document.getElementById("competitionDescription");

if (competition === "All") {
    competitionDescription.textContent =
        "Upcoming Maryland Soccer Matches";
} else if (competition === "NCAA D1 Men") {
    competitionDescription.textContent =
        "Upcoming NCAA D1 Men's Matches";
} else if (competition === "NCAA D1 Women") {
    competitionDescription.textContent =
        "Upcoming NCAA D1 Women's Matches";
} else if (competition === "NCAA D2 Men") {
    competitionDescription.textContent =
        "Upcoming NCAA D2 Men's Matches";
} else if (competition === "NCAA D2 Women") {
    competitionDescription.textContent =
        "Upcoming NCAA D2 Women's Matches";
} else if (competition === "NCAA D3 Men") {
    competitionDescription.textContent =
        "Upcoming NCAA D3 Men's Matches";
} else if (competition === "NCAA D3 Women") {
    competitionDescription.textContent =
        "Upcoming NCAA D3 Women's Matches";
}

let filteredMatches = includedMatches;

if (competition === "NCAA D1 Men") {
    filteredMatches = includedMatches.filter(match =>
        match.level === "NCAA D1" &&
        match.gender === "Men"
    );
}

if (competition === "NCAA D1 Women") {
    filteredMatches = includedMatches.filter(match =>
        match.level === "NCAA D1" &&
        match.gender === "Women"
    );
}

if (competition === "NCAA D2 Men") {
    filteredMatches = includedMatches.filter(match =>
        match.level === "NCAA D2" &&
        match.gender === "Men"
    );
}

if (competition === "NCAA D2 Women") {
    filteredMatches = includedMatches.filter(match =>
        match.level === "NCAA D2" &&
        match.gender === "Women"
    );
}

if (competition === "NCAA D3 Men") {
    filteredMatches = includedMatches.filter(match =>
        match.level === "NCAA D3" &&
        match.gender === "Men"
    );
}

if (competition === "NCAA D3 Women") {
    filteredMatches = includedMatches.filter(match =>
        match.level === "NCAA D3" &&
        match.gender === "Women"
    );
}

            const selectedTeam = document.getElementById("teamFilter").value;

if (selectedTeam !== "All") {
    filteredMatches = filteredMatches.filter(match =>
        match.home === selectedTeam ||
        match.away === selectedTeam
    );
}
            const timeFilter = document.getElementById("timeFilter").value;

          const timeDescription = document.getElementById("timeDescription");

if (timeFilter === "7") {
    timeDescription.textContent = "Next 7 days";
} else if (timeFilter === "30") {
    timeDescription.textContent = "Next 30 days";
} else {
    timeDescription.textContent = "All future games";
}

const upcomingMatches = filterByTime(filteredMatches, timeFilter);

if (upcomingMatches.length === 0) {
    document.getElementById("matches").innerHTML =
        "<p>No matches found for this selection.</p>";
} else {
    const html = renderMatches(upcomingMatches);

    document.getElementById("matches").innerHTML = html;
}
        })
        .catch(error => {

            document.getElementById("matches").innerHTML =
                "Unable to load matches.";

            console.error(error);

        });

}


function parseCSV(data) {

    const rows = data.split("\n");

    const matches = [];

    rows.slice(1).forEach(row => {

        const columns = row.split(",");

        if (columns.length > 12) {

            matches.push({

                date: columns[0].trim(),
                time: columns[1].trim(),
                competition: columns[2].trim(),
                stage: columns[3].trim(),
                gender: columns[4].trim(),
                level: columns[5].trim(),
                home: columns[6].trim(),
                away: columns[7].trim(),
                venue: columns[8].trim(),
                broadcast: columns[9].trim(),
                notes: columns[10].trim(),
                status: columns[11].trim(),
                include: columns[12].trim()

            });

        }

    });

    return matches;

}


function filterByTime(matches, timeFilter) {

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    if (timeFilter === "all") {

        return matches.filter(match => {

            const parts = match.date.split("/");

            const matchDate = new Date(
                parts[2],
                parts[0] - 1,
                parts[1]
            );

            return matchDate >= today;

        });

    }

    const days = Number(timeFilter);

const endDate = new Date(today);
endDate.setDate(today.getDate() + days - 1);

    return matches.filter(match => {

        const parts = match.date.split("/");

        const matchDate = new Date(
            parts[2],
            parts[0] - 1,
            parts[1]
        );

        return matchDate >= today && matchDate <= endDate;

    });

}


function renderMatches(matches) {

    matches.sort((a, b) => {

        const dateA = new Date(a.date + " " + a.time);
        const dateB = new Date(b.date + " " + b.time);

        return dateA - dateB;

    });

    const grouped = {};

    matches.forEach(match => {

        if (!grouped[match.date]) {

            grouped[match.date] = {};

        }

        if (!grouped[match.date][match.competition]) {

            grouped[match.date][match.competition] = [];

        }

        grouped[match.date][match.competition].push(match);

    });

    let html = "";

    Object.keys(grouped).forEach(date => {

        html += `<div class="date">${formatDate(date)}</div>`;

        Object.keys(grouped[date]).forEach(competition => {

            html += `<div class="league">${competition}</div>`;

            grouped[date][competition].forEach(match => {

                html += `
                    <div class="match">

                    <div class="gender">${match.gender}</div>

                    <div class="stage">${match.stage}</div>
  
                    <div class="time">${match.time}</div>

                   <div class="teams">
    ${teamLogos[match.home]
        ? `<img src="${teamLogos[match.home]}" class="team-logo">`
        : ""}
    ${match.home}
    vs
    ${match.away}
    ${teamLogos[match.away]
        ? `<img src="${teamLogos[match.away]}" class="team-logo">`
        : ""}
</div>

${match.status !== "Scheduled"
    ? `<div class="status">${match.status}</div>`
    : ""}

                        <div class="details">
                            ${match.venue}
                            ${match.broadcast ? " | " + match.broadcast : ""}
                        </div>

                    </div>
                `;

            });

        });

    });

    return html;

}


document.addEventListener("DOMContentLoaded", function () {

    loadMatches();

    document
        .getElementById("competitionFilter")
        .addEventListener("change", loadMatches);

    document
        .getElementById("timeFilter")
        .addEventListener("change", loadMatches);

    document
    .getElementById("teamFilter")
    .addEventListener("change", loadMatches);

});
