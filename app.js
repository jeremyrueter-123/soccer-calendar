const sheetURL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTMUQiKrsd5pS1Tq7V1Qghgr6E0pCVhQvF7JiHiOgnJ_C_uuxCNljnCMBXWwzHK7WKBbo_x4aopyuJ1/pub?gid=0&single=true&output=csv";

fetch(sheetURL)
  .then(response => response.text())
  .then(data => {

    const rows = data.split("\n");
    let matches = [];

    rows.slice(1).forEach(row => {

      const columns = row.split(",");

      if (columns.length > 7) {
        matches.push({
          date: columns[0],
          time: columns[1],
          league: columns[2],
          home: columns[5],
          away: columns[6],
          venue: columns[7]
        });
      }

    });

    let grouped = {};

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

      html += `<div class="date">${date}</div>`;

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


    document.getElementById("matches").innerHTML = html;

  })
  .catch(error => {
    document.getElementById("matches").innerHTML =
      "Unable to load matches.";
    console.error(error);
  });
