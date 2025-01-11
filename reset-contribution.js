const table = document.getElementsByClassName('js-calendar-graph-table')[0];
const cells = table.querySelectorAll('[data-date],[data-level]');
const dateAndContribution = {};

cells.forEach(cell => {
    const date = cell.getAttribute('data-date');
    const level = parseInt(cell.getAttribute('data-level'));
    const toolTipId = cell.getAttribute('aria-labelledby');
    const toolTip = document.getElementById(toolTipId);
    const toolTipText = toolTip.textContent;
    if(level > 0) {
        const contribution = parseInt(toolTipText.match(/(\d+) contribution/)[1]);
        dateAndContribution[date] = contribution;
    }
});

const maxContribution = Math.max(...Object.values(dateAndContribution));
const minDate = Object.keys(dateAndContribution).reduce((minDate, date) =>
    date < minDate ? date : minDate, Object.keys(dateAndContribution)[0]);
const year = parseInt(minDate.split('-')[0]);
console.log('Detected year:', year);
console.log('MaxContribution:', maxContribution);
const startDate = new Date(Date.UTC(year, 0, 1));
const endDate = new Date(Date.UTC(year, 11, 31))    ;

function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

let currentDate = startDate;
let fileContent = '';

var commitsToPush = 0

while (currentDate <= endDate) {
    const dateString = currentDate.toISOString().split('T')[0];
    const existingContribution = dateAndContribution[dateString] || 0;
    const moreContribution = maxContribution - existingContribution;
    const isoDateString = currentDate.toISOString()

    for (let i = 0; i < moreContribution; i++) {
        const env_Vars = `GIT_AUTHOR_DATE="${isoDateString}" GIT_COMMITTER_DATE="${isoDateString}"`
        const commit_msg = `Commit ${ existingContribution + i + 1} for day ${dateString}`;
        fileContent += `${env_Vars} git commit --allow-empty -m "${commit_msg}"\n`;
        commitsToPush++
        if (commitsToPush >= 1000) {
            fileContent += 'git push\n';
            commitsToPush = 0;
        }
    }

    currentDate = addDays(currentDate, 1);
}
fileContent += 'git push\n';

// Create a Blob with the file content
const blob = new Blob([fileContent], { type: 'text/plain' });

// Create a temporary URL for the Blob
const url = URL.createObjectURL(blob);

// Create a hidden anchor element
const a = document.createElement('a');
a.style.display = 'none';
a.href = url;
a.download = 'commits.sh'; // Set the desired filename (changed to .sh for shell script)

// Trigger a click on the anchor element to start the download
document.body.appendChild(a);
a.click();

// Clean up
document.body.removeChild(a);
URL.revokeObjectURL(url);