const sheetURL =
  "https://docs.google.com/spreadsheets/d/e/2PACX-1vTMUQiKrsd5pS1Tq7V1Qghgr6E0pCVhQvF7JiHiOgnJ_C_uuxCNljnCMBXWwzHK7WKBbo_x4aopyuJ1/pub?gid=0&single=true&output=csv";


// Converts dates like 07/26/2026 into Sunday, July 26
function formatDate(dateString) {

    const date = new Date(dateString);

    return date.toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric"
    });

}


loadMatches();

function loadMatches() {

    fetch(sheetURL)
        .then(response => response.text())
        .then(data => {

          const matches = parseCSV(data);
          const upcomingMatches = filterNextSevenDays(matches);
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

function filterNextSevenDays(matches) {

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const sevenDays = new Date(today);
    sevenDays.setDate(today.getDate() + 7);

    return matches.filter(match => {

        const parts = match.date.split("/");

        const matchDate = new Date(
            parts[2],          // Year
            parts[0] - 1,      // Month (0-11)
            parts[1]           // Day
        );

        return matchDate >= today && matchDate <= sevenDays;

    });

}

function renderMatches(matches) {

    const grouped = {};

    matches.forEach(match => {

        if (!grouped[match.date]) {

            grouped[match.date] = {};

        }

        if (!grouped[match.date][match.league]) {

            grouped[match.date][match.league] = [];

        }

        grouped[match.date][match.league].push(match);

    });

    let html = "";

    Object.keys(grouped).forEach(date => {

        html += `<div class="date">${formatDate(date)}</div>`;

        Object.keys(grouped[date]).forEach(league => {

            html += `<div class="league">${league}</div>`;

            grouped[date][league].forEach(match => {

                html += `
                    <div class="match">
                        <div class="time">${match.time}</div>
                        <div class="teams">${match.home} vs ${match.away}</div>
                        <div class="details">${match.venue}</div>
                    </div>
                `;

            });

        });

    });

    return html;

}
