const sheetURL =
  "https://docs.google.com/spreadsheets/d/e/2PACX-1vTMUQiKrsd5pS1Tq7V1Qghgr6E0pCVhQvF7JiHiOgnJ_C_uuxCNljnCMBXWwzHK7WKBbo_x4aopyuJ1/pub?gid=924645803&single=true&output=csv";


// Converts dates like 07/26/2026 into Sunday, July 26
function formatDate(dateString) {

    const date = new Date(dateString);

    return date.toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric"
    });

}


function loadMatches() {

    fetch(sheetURL)
        .then(response => response.text())
        .then(data => {

            const matches = parseCSV(data);

            console.log(matches);

            const includedMatches = matches.filter(match => match.include === "Yes");

            const competition = document.getElementById("competitionFilter").value;

const filteredMatches = competition === "All"
    ? includedMatches
    : competition === "NCAA D1 Men"
        ? includedMatches.filter(match =>
            match.level === "NCAA D1" &&
            match.gender === "Men"
        )
        : includedMatches.filter(match =>
            match.level === "NCAA D1" &&
            match.gender === "Women"
        );

const timeFilter = document.getElementById("timeFilter").value;

const upcomingMatches = filterByTime(filteredMatches, timeFilter);

const html = renderMatches(upcomingMatches);

            document.getElementById("matches").innerHTML = html;

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
    endDate.setDate(today.getDate() + days);

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

                        <div class="teams">${match.home} vs ${match.away}</div>

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

});
