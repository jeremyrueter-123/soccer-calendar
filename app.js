const sheetURL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTMUQiKrsd5pS1Tq7V1Qghgr6E0pCVhQvF7JiHiOgnJ_C_uuxCNljnCMBXWwzHK7WKBbo_x4aopyuJ1/pub?gid=0&single=true&output=csv";

fetch(sheetURL)
  .then(response => response.text())
  .then(data => {
    const rows = data.split("\n");

    let html = "";

    rows.slice(1).forEach(row => {
      const columns = row.split(",");

      if (columns.length > 5) {
        const date = columns[0];
        const time = columns[1];
        const competition = columns[2];
        const home = columns[5];
        const away = columns[6];
        const venue = columns[7];

        html += `
          <div class="match">
            <div class="league">${competition}</div>
            <div class="time">${time}</div>
            <div>${home} vs ${away}</div>
            <div class="details">${venue}</div>
          </div>
        `;
      }
    });

    document.getElementById("matches").innerHTML = html;
  })
  .catch(error => {
    document.getElementById("matches").innerHTML =
      "Unable to load matches.";
    console.error(error);
  });